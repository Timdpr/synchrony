"""
Provides method to get a numpy ndarray of all binary images ([h:w:n]) from
the specified directory. Used to get 'pattern' arrays for driving the network

@author tp275
"""

import os
from scipy.misc import imread
import numpy as np

def getPatternsInDirectory(path, M, N, rotation=False, rot_step=1):
    """
    """
    dirs = os.listdir(path)
    
    if rotation:  # make 3rd dimension  ...  no. images * no. rotations
        patterns = patterns = np.zeros(( M, N, len(dirs)*(N/rot_step) ))
    else:  # otherwise, should just be number of images
        patterns = np.zeros(( M, N, len(dirs) ))
    
    rot_i = 0  # for indexing 3rd dim. when rotating
    for i, item in enumerate(dirs):  # for each image
            # Open image and convert to binary values
            if os.path.isfile(path+item):
                im = imread(path+item, flatten=True, mode='1')
                im[im < 1] = 1
                im[im > 1] = 0
                
                # optionally rotate image, then add to patterns array
                if rotation:
                    for r in range(N/rot_step):  # for no. of rotated images
                        patterns[:,:,rot_i] = im  # add to patterns - this goes before roll so orig. image is first
                        im = np.roll(im, -rot_step, 1)  # 'roll' the image array (left) by given step
                        rot_i += 1
                else:
                    patterns[:,:,i] = im
                
    return patterns
