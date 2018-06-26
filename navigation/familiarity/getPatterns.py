"""
Provides method to get a numpy ndarray of all binary images ([h:w:n]) from
the specified directory. Used to get 'pattern' arrays for familiarity.py.

@author tp275
"""

import os
from scipy.misc import imread
import numpy as np

def getPatternsInDirectory(path, M, N):
    dirs = os.listdir(path)
    
    patterns = np.zeros((M, N, len(dirs)))
    
    for i, item in enumerate(dirs):  # for each image
            if os.path.isfile(path+item):
                im = imread(path+item, flatten=True, mode='L')
                im[im < 1] = 1
                im[im > 1] = 0
                patterns[:,:,i] = im
                
    return patterns
