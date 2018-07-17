"""
Runs the experiment with given parameters and outputs results as a text file

@author tp275
"""
import RIDF
import numpy as np
from individualTests import TestPatternsOnNetwork

def outputResultsTextFile(results, result_num):
    with open('results%i.txt'%(result_num), 'w') as f:
    	f.write(str(results))
        

test = TestPatternsOnNetwork([7, 90], 4, rotation=True, rot_step=10,
                             pattern_dir='/home/ec2-user/environment/synchrony/images/individual_view/',
                             route_pattern_dir='/home/ec2-user/environment/synchrony/images/route_90x7/',
#                             pattern_dir='/mnt/hgfs/Masters/Project/synchrony/images/individual_view/',
#                             route_pattern_dir='/mnt/hgfs/Masters/Project/synchrony/images/route_90x7/',
                             pattern_b=0, pattern_c=0.2,
                             conn_b_bck=1, conn_c_bck=0.3,
                             conn_b=1, conn_c=0.15, 
                             downsample=100)

results = test.run()
patterns = test.patterns

for i in range(test.num_unrotated):  # for i = image number
    # Plot RIDF graph (of each rotated image), for each image
    RIDF.plotRIDF(patterns[:,:,test.rotations_per_image*i:(test.rotations_per_image*i)+test.rotations_per_image], i)

for i in range(test.num_unrotated):  # for i = image number
    # Create list of results of each sample for the particular image
    results_by_image = [sample[i] for sample in results]
    RIDF.plotRotationSynchrony(results_by_image, i)

outputResultsTextFile(results, 1)
