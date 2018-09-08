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
        

test = TestPatternsOnNetwork([7, 90], 1, rotation=False, rot_step=2,
                             pattern_dir='/home/ec2-user/environment/synchrony/images/exp_quiver/',
                             route_pattern_dir='/home/ec2-user/environment/synchrony/images/routes/route_boxes_90x7/',
#                             pattern_dir='/mnt/hgfs/Masters/Project/synchrony/images/exp_rotation_rsync/',
#                             route_pattern_dir='/mnt/hgfs/Masters/Project/synchrony/images/routes/route_boxes_90x7/',
                             pattern_b=0, pattern_c=0.2, conn_b_bck=1, conn_c_bck=0.3,
                             conn_b=1, conn_c=0.15, downsample=100)

results = test.run()
print("--- %s seconds ---" % (time.time() - start_time))
patterns = test.patterns

"""
i = 0
original_image = RIDF.getImageList(patterns[:,:,test.rotations_per_image*i:(test.rotations_per_image*i)+test.rotations_per_image])[0]

for i in range(2):  # for i = image number
    # Plot RIDF graph (of each rotated image), for each image
    RIDF.plotRIDF(patterns[:,:,test.rotations_per_image*i:(test.rotations_per_image*i)+test.rotations_per_image], i,
                  use_single_comparison=True, original_image=original_image)
"""


"""
for i in range(2):  # for i = image number
    # Create list of results of each sample for the particular image
    results_by_image = [sample[i] for sample in results]
    RIDF.plotRotationSynchrony(results_by_image, i)
#    rsync, degree = get_rsync_and_rotation(results_by_image)
#    degrees.append(degree)
#    degrees_test.append(degree)
#    rsync_test.append(rsync)
"""
    
outputResultsTextFile(results, 0)

index_rsyn = []
for im in results:
    temp = []
    for rot in range(len(im)):
        temp.append(im[rot][0][1])
        
    index_rsyn.append([np.argmax(temp), np.max(temp)])
    
print(index_rsyn)
