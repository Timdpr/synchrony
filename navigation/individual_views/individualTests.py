"""
Outputs a synchrony measure for a single view. Partially based on cknd's original 'familiarity.py'

@author tp275
"""

import numpy as np
import os, sys
hc_path = "../../navLibHC"
sys.path.append(os.path.realpath(hc_path))
import hcLab as lab
import hcNetworks as net
from numpy.random import RandomState
import getPatterns

class TestPatternsOnNetwork:
    def __init__(self, network_dimensions, num_samples, rotation=False, rot_step=1,
                 pattern_dir='/home/ec2-user/environment/synchrony/images/exp_rotation_plants/',
                 route_pattern_dir='/home/ec2-user/environment/synchrony/images/routes/route_plants_90x7/',
                 pattern_b=0, pattern_c=0.2, conn_b_bck=1, conn_c_bck=0.3, conn_b=1, conn_c=0.15, downsample=100):
        """
        network_dimensions: [M, N], the network size
        num_samples: repetitions of the whole sampling procedure (networks & patterns)
        rotation: whether to include rotated versions of each image
        rot_step: the 'step' by which to rotate the image, by number of pixels. Must be a multiple of 'N'
        pattern_dir: path to folder containing images to present to the network
        route_pattern_dir: path to folder containing images to imprint/encode in the network
        
        pattern_b: pattern size: activation probability dropoff rate with distance from pattern center
        pattern_c: pattern size: activation probability cutoff with distance
        conn_b_bck: network connectivity dropoff rate with distance from other cell, for non-coactivated (background) cell pairs
        conn_c_bck: network connectivity cutoff with distance, for non-coactivated (background) cell pairs
        conn_b: dropoff rate for co-activated cells
        conn_c: relaxed cutoff for co-activated cells. Try 0.1: Stronger sync difference between high and low similarity, but
                connectivtiy structure seems very dense. Or try 0.2: Rather sparse-looking connectivity and more washed out sync result.
        """
        self.M = network_dimensions[0]
        self.N = network_dimensions[1]
        self.num_samples = num_samples
        self.pattern_b = pattern_b
        self.pattern_c = pattern_c
        self.conn_b_bck = conn_b_bck
        self.conn_c_bck = conn_c_bck
        self.conn_b = conn_b
        self.conn_c = conn_c
        self.downsample = downsample
        self.patterns = getPatterns.getPatternsInDirectoryForQuiver(pattern_dir, self.M, self.N)
        self.route_patterns = getPatterns.getPatternsInDirectory(route_pattern_dir, self.M, self.N)
        self.num_imprinted = len(self.route_patterns[0][0])

        self.rotations_per_image = self.N / rot_step if rotation else 1
        self.num_unrotated = None  # no. images in folder
        self.network = None
        self.experiments = []
        self.similarities = []
        self.results = []


    def setup_network(self, rng):
        """
        Creates the network and imprints given (route) images, with distance-dependent
        connection probability and stronger links between cells that participate in the route patterns
        """
        print("Creating network from " + str(self.num_imprinted) + " route images")
        self.network = None
        
        # Generate the network using route images
        self.network = net.grid_empty(self.M, self.N)
        nodes = self.network.nodes()
        for i, u in enumerate(nodes):
            for v in nodes[i+1:]:
                # Check if both nodes participate in the same pattern
                in_pattern = False 
                for pat in range(self.num_imprinted):
                    if self.route_patterns[u[0],u[1],pat] and self.route_patterns[v[0],v[1],pat]:
                        in_pattern = True
                        break
                # if so, make a strong link with some probability depending on distance
                p_connect_pattern    = max(1.0/(self.conn_b*np.sqrt((u[0]-v[0])**2 + (u[1]-v[1])**2))-self.conn_c,0)
                p_connect_background = max(1.0/(self.conn_b_bck*np.sqrt((u[0]-v[0])**2 + (u[1]-v[1])**2))-self.conn_c_bck,0)
                if in_pattern and rng.rand()<p_connect_pattern:
                    self.network.add_edge(u,v,{"strength":15})
                # fewer and weaker background connections are created where there was no common input.
                elif rng.rand()<p_connect_background:
                    self.network.add_edge(u,v,{"strength":1})
        print("Done")
                    
        
    def setup_experiments(self, rng):
        """
        Creates a setup (experiment object) for each pattern to be presented to the network
        """
        # no. images in folder = no. patterns / no. rotations
        self.num_unrotated = int(len(self.patterns[0][0]) / self.rotations_per_image)
        # populate experiments list with same no. lists as number of images in folder
        self.experiments = [[] for i in range(self.num_unrotated)]
        self.similarities = [[] for i in range(self.num_unrotated)]
        for i in range(len(self.patterns[0][0])): # for each pattern
            current = self.patterns[:,:,i]
            ex = lab.experiment(self.network, [rng.randint(1,10000)],
                                inputc=current, name="pattern "+str(i),
                                downsample=self.downsample, verbose=True, con_upstr_exc=2,
                                measures=[lab.spikey_rsync(roi=current, name="rsync", tau=10.0/self.downsample),
                                          lab.mean_spikecount(roi=current, name="spikes")])
    
            # Calculate this pattern's similarity to imprinted route patterns
            # (the fraction of its cells it shares with an imprinted pattern)
            overlaps = [np.sum(current*self.route_patterns[:,:,j])/float(np.sum(current)) for j in range(self.num_imprinted)]
            nr_active = np.sum(current) # nr of active cells in the pattern (for normalization)
            all_imprinted = np.sum(self.route_patterns[:,:,0:self.num_imprinted],axis=2)
            all_imprinted[all_imprinted>1] = 1
            similarity = np.sum(current*all_imprinted)/float(nr_active)
            
            activated_subnet = self.network.subgraph([node for node in zip(*np.where(current))])
            edges = [edge for edge in activated_subnet.edges_iter(data=True) if edge[2]["strength"]>1]

            ex.network_match = len(edges)/float(np.sum(current > 0))
            ex.similarity = similarity
            ex.similar_to = zip(overlaps,[self.route_patterns[:,:,j].copy() for j in range(self.num_imprinted)])
        
            self.experiments[int(np.floor(i/self.rotations_per_image))].append(ex)
            self.similarities[int(np.floor(i/self.rotations_per_image))].append(similarity)
            
            
    def run(self):
        current = 1
        for s in range(self.num_samples):
            rng = RandomState(s)
            self.setup_network(rng)
            self.setup_experiments(rng)
            
            
            # fetch synchrony measurements (this triggers the simulation to be run)
            sample_result = []
            for ie, image_experiments in enumerate(self.experiments):
                image_result = []
                for re, rotation_experiment in enumerate(image_experiments):
                    
                    print("\n### Experiment %i/%i for image %i/%i in sample %i/%i ###\n(%i/%i)"
                          %(re+1, len(image_experiments), ie+1, len(self.experiments), s+1, self.num_samples,
                          current, (len(image_experiments)*len(self.experiments))*self.num_samples))
                    
                    current += 1
                    image_result.append([self.similarities[ie][re], rotation_experiment.getresults('rsync')[0]])
                sample_result.append(image_result)
            self.results.append(sample_result)
            
        return self.results
