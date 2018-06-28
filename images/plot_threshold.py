"""
Uses Otsu thresholding to convert all greyscale images in the
specified directory to binary images - ie. black-and-white - and saves them.

@author tp275
"""

import os
import matplotlib.pyplot as plt
from skimage import filters
from skimage import io
from skimage import color

path = ('C:/Users/s/Documents/Masters/Project/images/binarised_rotated/')
dirs = os.listdir(path)

def threshold():
    for item in dirs:  # for each image
        if os.path.isfile(path+item):
            im = io.imread(path+item) # load

            # Convert to binary using skimage filter
            val = filters.threshold_otsu(im)
            im = im < val

            # Save, overwriting existing file
            f, e = os.path.splitext(path+item)
            plt.imsave(f, color.rgb2gray(im), cmap='gray')
			
threshold()
