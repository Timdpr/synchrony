"""
Runs the experiment with given parameters and outputs results as a text file

@author tp275
"""
import RIDF
import numpy as np
from individualTests import TestPatternsOnNetwork

def outputResultsTextFile(results):
    text = ("similarity, rsync\n\n")
    for s in range(len(results)):
        text += "Sample " + str(s)
        for sim, rsync in results[s]:
            temp = '\n' + str(sim) + ', ' + str(rsync)
            text += temp
        text += '\n\n'
    text += 'Mean rsync for each similarity:\n'
    for i in range(6):
        text += str(np.mean([results[0][i][1], results[1][i][1], results[2][i][1]]))
        text += '\n'
    with open('latest_result.txt', 'w') as f:
    	f.write(text)
        

test = TestPatternsOnNetwork([7, 90], 1,
                             rotation=True, rot_step=30,
                             pattern_dir='/synchrony/images/individual_view',
                             route_pattern_dir='/synchrony/images/route_90x7/',
#                             pattern_dir='/mnt/hgfs/Masters/Project/synchrony/images/individual_view/',
#                             route_pattern_dir='/mnt/hgfs/Masters/Project/synchrony/images/route_90x7/',
                             pattern_b=0, pattern_c=0.2,
                             conn_b_bck=1, conn_c_bck=0.3,
                             conn_b=1, conn_c=0.15, 
                             downsample=100)

results = test.run()
patterns = test.patterns

RIDF.plotRIDF(patterns)
RIDF.plotRotationSynchrony(results)

outputResultsTextFile(results)
