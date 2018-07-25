"""
Script initially created by cknd, modified for route navigation etc. by tp275

Samples random spatial networks with strong links clustered in certain random input patterns.
Then, tests synchrony for input patterns that more or less resemble these imprinted patterns.

This script takes a long time to run.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import *
import os,sys
hc_path = "../../navLibHC"
sys.path.append(os.path.realpath(hc_path))
import networkx as nx
import hcLab as lab
import hcNetworks as net
import hcPlotting as plo
import hcUtil as ut
from numpy.random import RandomState
import getPatterns
close('all')

downsample=100

M=7 # network size
N=90 # '' ''
num_patterns_initial = 24660/8 # initial size of pattern pool from which to sample - increases itself as needed:
patterns_per_bin = 1       # pattern pool is increased until this nr of patterns is found in each bin.
num_imprinted=10 # nr of high prior patterns, i.e. number of route images
pattern_b=1 # pattern size: activation probability dropoff rate with distance from pattern center
pattern_c=0.2 # pattern size: activation probability cutoff with distance
conn_b_bck=1 # network connectivity dropoff rate with distance from other cell, for non-coactivated (background) cell pairs
conn_c_bck=0.3 # network connectivity cutoff with distance, for non-coactivated (background) cell pairs
conn_b=1 # dropoff rate for co-activated cells
conn_c=0.15 # relaxed cutoff for co-activated cells. Try 0.1: Stronger sync difference between high and low similarity, but connectivtiy structure seems very dense. Or try 0.2: Rather sparse-looking connectivity and more washed out sync result.

bins = [0.5, 0.6, 0.7, 0.8, 0.9, 1.]#np.arange(0.5,1.1,0.1) #np.arange(0.2,1.1,0.2) # edges of the desired similarity bins
n_samples = 15 # repetitions of the whole sampling procedure (networks & patterns)

experiments = []
def setup(seed,seednr,num_patterns):
    print "sampling network",seednr,"with a pool of",num_patterns,"patterns"
    # Instead of generating patterns, get patterns from 'all_views' folder ## tp275 ##
    patterns = getPatterns.getPatternsInDirectory(
                '/home/ec2-user/environment/synchrony/images/all_views_90x7/', M, N, rotation=True, rot_step=1)
    rng = RandomState(seed)

    # generate the network:
    # import images to generate the network, with distance-dependent connection probability,
    # with stronger links between cells that participate in the first num_imprinted patterns.
    network = net.grid_empty(M,N)
    nodes = network.nodes()
    route_patterns = getPatterns.getPatternsInDirectory(
                '/home/ec2-user/environment/synchrony/images/route_90x7/', M, N)
    
    for i,u in enumerate(nodes):
        for v in nodes[i+1:]:
            # if both nodes participate in the same pattern, make a strong link,
            # with some probability depending on distance
            in_pattern=False
            for pat in range(num_imprinted):
                if route_patterns[u[0],u[1],pat] and route_patterns[v[0],v[1],pat]:
                    in_pattern = True
                    break

            p_connect_pattern    = max(1.0/(conn_b*np.sqrt((u[0]-v[0])**2 + (u[1]-v[1])**2))-conn_c,0)
            p_connect_background = max(1.0/(conn_b_bck*np.sqrt((u[0]-v[0])**2 + (u[1]-v[1])**2))-conn_c_bck,0)
            if in_pattern and rng.rand()<p_connect_pattern:
                network.add_edge(u,v,{"strength":15})
            # fewer and weaker background connections are created where there was no common input.
            elif rng.rand()<p_connect_background:
                network.add_edge(u,v,{"strength":1})

    # create a setup (experiment object) for each pattern to be presented to the network
    experiments_this_net = []
    similarities_this_net = []
    for i in range(num_patterns):
        i = np.random.randint(0, num_patterns)  # Make pattern selection random for more variation (hopefully)
        current = patterns[:,:,i]
        ex = lab.experiment(network,[rng.randint(1,10000)],inputc=current, name="seed "+str(seednr)+" pattern "+str(i), downsample=downsample, verbose=True, con_upstr_exc=2,
                                            measures=[lab.spikey_rsync(roi=current,name="rsync",tau=10.0/downsample),
                                                      lab.mean_spikecount(roi=current,name="spikes"),
                                                      ])
        # calculate this pattern's similarity to imprinted patterns
        # (the fraction of its cells it shares with an imprinted pattern)
        # Change: 'patterns' has been changed to 'route_patterns' where appropriate ## tp275 ##
        overlaps = [np.sum(current*route_patterns[:,:,j])/float(np.sum(current)) for j in range(num_imprinted)]
        nr_active = np.sum(current) # nr of active cells in the pattern (for normalization)
        all_imprinted = np.sum(route_patterns[:,:,0:num_imprinted],axis=2)
        all_imprinted[all_imprinted>1] = 1
        similarity = np.sum(current*all_imprinted)/float(nr_active)

        activated_subnet = network.subgraph([node for node in zip(*np.where(current))])
        edges = [edge for edge in activated_subnet.edges_iter(data=True) if edge[2]["strength"]>1]

        ex.network_match = len(edges)/float(np.sum(current > 0))

        # import ipdb; ipdb.set_trace()

        ex.similarity = similarity
        ex.similar_to = zip(overlaps,[route_patterns[:,:,j].copy() for j in range(num_imprinted)])
        similarities_this_net.append(similarity)
        # if i<num_imprinted:
        #     ex.name+="_imprinted"
        experiments_this_net.append(ex)

    # sort all experiments that use this network by pattern similarity
    sort = np.digitize(similarities_this_net,bins,right=True)
    experiments_binned = [[] for _ in bins]
    similarities_binned = [[] for _ in bins]
    for i,ex in enumerate(experiments_this_net):
        experiments_binned[sort[i]].append(ex)
        similarities_binned[sort[i]].append(ex.similarity)

    # check whether there are enough experiments in each pattern similarity bin
    if np.min([len(s) for s in similarities_binned]) >= patterns_per_bin:
        return np.array([column[0:patterns_per_bin] for column in experiments_binned]).flatten()
    elif num_patterns<num_patterns_initial*100:
        print "seednr "+str(seednr)+": "+str(num_patterns)+" sample patterns not enough, trying with more"
        return setup(seed,seednr,num_patterns*2)
    else:
        raise Exception("couldn't find required number of samples in each bin after "+str(num_patterns)+" patterns")

# repeatedly run the whole sampling procedure
for i in np.arange(n_samples):
    experiments.extend(setup(i,i,num_patterns_initial))

# sort all experiments on all networks, based on pattern similarity
similarities = [ex.similarity for ex in experiments]
experiments_binned = [[] for _ in bins]
sort = np.digitize(similarities,bins,right=True)
similarities_binned = [[] for _ in bins]
for i,ex in enumerate(experiments):
    experiments_binned[sort[i]].append(ex)
    similarities_binned[sort[i]].append(ex.similarity)

experiments_binned.append([e for e in experiments_binned[-1] if e.network_match >= 2])
bins = list(bins)+[1]


def doboxplot(data,xticklabels, do_scatter=False, xtop=False):
    figure(figsize=(5,5))
    if xtop:
        ax = gca()
        ax.xaxis.set_label_position('top')
        tick_params(top=True, labeltop=True, labelbottom=False, right=True, direction='in')
    grid(linestyle='-', which='major', axis='y',color='black',alpha=0.3)
    boxplot(data,notch=True,sym='+',boxprops={'color':'black'},flierprops={'color':'black'},
                    medianprops={'color':'red'},whiskerprops={'color':'black','linestyle':'-'})
    # background scatterplot:
    if do_scatter:
        for i in range(len(data)):
            displacement = np.array([0.97+0.06*np.random.randn() for _ in range(len(data[i]))])
            scatter(i+displacement,data[i],marker='o',s=30,alpha=0.15,c=(0,0.2,0.8),linewidth=0)
    xlim((0,len(data)+1))
    ylim(0,1)
    xlabel("Similarity to imprinted patterns", labelpad=8)
    ylabel(r'$R_{syn}$')
    xticks(np.arange(0.5,len(data)+1.5),xticklabels, rotation=0)
    
    
def do_scatter_plot(experiments):
    figure(figsize=(5,5))
    ax = gca()
    ax.xaxis.set_label_position('top')
    tick_params(top=True, labeltop=True, labelbottom=False, right=True, direction='in')
    grid(linestyle='-', which='major', axis='y',color='black',alpha=0.3)
    x = [ex.similarity for ex in experiments]
    y = [ex.getresults('rsync')[0] for ex in experiments]
    scatter(x, y, marker='o',s=30,alpha=0.2,c=(0,0.2,0.8),linewidth=0)
    xlim(-0.05, 1.05)
    ylim(0,1)
    xlabel("Similarity to imprinted patterns", labelpad=8)
    ylabel(r'$R_{syn}$')
    xticks(np.linspace(0, 1, 11))


def plot_setups(experiments,save=True):
    for i,ex in enumerate(experiments):
        figure(figsize=(25,2))
        plo.eplotsetup(ex,'rsync')
        title("similarity "+str(ex.similarity))
        if save:
            savefig(ex.name+'.pdf', bbox_inches='tight')

			
# plot one example from each similarity category
picture_seed = 0  # remember small seed for when running small # of repetitions ## tp275 ##
plot_setups([column[picture_seed] for column in experiments_binned[:-1]])
# make a video of an example from the highest similarity bin
#last = experiments_binned[-2][picture_seed].saveanimtr(0,10,2,grid_as='graph')

figure(figsize=(25,2))
plo.plotsetup(experiments_binned[0][picture_seed].network,np.zeros((M,N)),np.zeros((M,N)),gca(),grid_as='graph')
title('network')
savefig('network.pdf', bbox_inches='tight')

# fetch synchrony measurements from trials where there was at least 1 spike
# (this triggers the simulation to be run)
rsyncs = [[] for _ in bins]
# spikecounts_ = [[] for _ in bins]
for i,column in enumerate(experiments_binned):
    for j,ex in enumerate(column):
        print "\n bin",i,"ex",j
        spikecount = ex.getresults('spikes')
        if np.mean(spikecount) >= 0.01:
            rsyncs[i].append(ex.getresults('rsync')[0])
            # spikecounts_[i].append(spikecount)

print "nr of samples per bin:", [len(s) for s in rsyncs]


# plot them
#figure(figsize=(5,4))
#doboxplot(spikecounts_,[0]+bins.tolist())
#ylabel("spikecount")
#savefig('spikecount.pdf', bbox_inches='tight')


# Box plot
doboxplot(rsyncs,[0]+bins, xtop=True)
xlabel("Similarity to imprinted patterns", labelpad=8)
ylabel(r'$R_{syn}$')
savefig('rsync_box.pdf', bbox_inches='tight')


# Box plot with (binned) scatter plot in background
doboxplot(rsyncs,[0]+bins,do_scatter=True,xtop=True)
xlabel("Similarity to imprinted patterns", labelpad=8)
ylabel(r'$R_{syn}$')
savefig('rsync_box_scatter.pdf', bbox_inches='tight')


# Scatter plot
do_scatter_plot(experiments)
savefig('rsync_scatter.pdf', bbox_inches='tight')


# Connectivity plot
doboxplot([[e.network_match for e in bin] for bin in experiments_binned], [0]+bins)
title('connectivity of inout-receiving cells')
ylabel("# connections / # input-receiving")
ylim(ymin=-0.1)
xlabel("Similarity index")
savefig('network_sampling_variability.pdf', bbox_inches='tight')


# Low synchrony, high similarity plot
figure(figsize=(25,2))
lowest_sync_highest_similarity = experiments_binned[-2][np.argmin([exp.getresults('rsync') for exp in experiments_binned[-2]])]
plo.eplotsetup(lowest_sync_highest_similarity, measurename='rsync')
title('example of a situation with low sync\ndespite high similarity index')
savefig('low_sync_high_similarity.pdf', bbox_inches='tight')

x = [ex.similarity for ex in experiments]
y = [ex.getresults('rsync')[0] for ex in experiments]
with open('results_4.txt', 'w') as f:
    f.write('similarities_binned:\n' + str(similarities_binned) + '\n\nrsyncs (binned):\n' + str(rsyncs) + '\n\n')
    f.write('similarities:\n' + str(x) + '\n\nrsyncs:\n' + str(y))
    
print('\a')
