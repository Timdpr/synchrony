"""
Runs the experiment with given parameters and outputs results as a text file

@author tp275
"""
import RIDF
from quiverPlot import quiver_plot, get_rsync_and_rotation
import numpy as np
from individualTests import TestPatternsOnNetwork

import time
start_time = time.time()

def outputResultsTextFile(results, result_num):
    with open('results%i.txt'%(result_num), 'w') as f:
    	f.write(str(results))
        

test = TestPatternsOnNetwork([7, 90], 2, rotation=True, rot_step=10,
                             pattern_dir='/home/ec2-user/environment/synchrony/images/individual_view/',
                             route_pattern_dir='/home/ec2-user/environment/synchrony/images/route_90x7/',
#                             pattern_dir='/mnt/hgfs/Masters/Project/synchrony/images/individual_view/',
#                             route_pattern_dir='/mnt/hgfs/Masters/Project/synchrony/images/route_90x7/',
                             pattern_b=0, pattern_c=0.2, conn_b_bck=1, conn_c_bck=0.3,
                             conn_b=1, conn_c=0.15, downsample=100)

results = test.run()
print("--- %s seconds ---" % (time.time() - start_time))
patterns = test.patterns

for i in range(test.num_unrotated):  # for i = image number
    # Plot RIDF graph (of each rotated image), for each image
    RIDF.plotRIDF(patterns[:,:,test.rotations_per_image*i:(test.rotations_per_image*i)+test.rotations_per_image], i)

rsyncs = np.zeros((17, 29))
rsync_test = []
degrees = [180 for i in range(493)]
degrees_test = []

for i in range(test.num_unrotated):  # for i = image number
    # Create list of results of each sample for the particular image
    results_by_image = [sample[i] for sample in results]
    RIDF.plotRotationSynchrony(results_by_image, i)
    rsync, degree = get_rsync_and_rotation(results_by_image)
#    degrees.append(degree)
    degrees_test.append(degree)
    rsync_test.append(rsync)
    
rsyncs[6][7] = rsync_test[0]
degrees[123] = -(degrees_test[0])

missing_img_nums = [slice(37, 42), slice(46, 50), slice(52, 59), slice(61, 76), slice(78, 93),
                    slice(95, 110), slice(112, 125), slice(130, 140),slice(147, 153), slice(165, 170),
                    slice(182, 185), slice(222, 226), slice(238, 244), slice(255, 261), slice(272, 279),
                    slice(289, 296), slice(306, 313), slice(323, 330), slice(334, 339), slice(340, 347),
                    slice(348, 356), slice(358, 362), slice(365, 374), slice(382, 391), slice(399, 408),
                    slice(417, 425), slice(434, 442), slice(451, 458), slice(469, 473)]
quiver_plot(degrees, rsyncs, missing_img_nums)
    
outputResultsTextFile(results, 1)
