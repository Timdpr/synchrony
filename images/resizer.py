"""
Crops, resizes and saves all images in the specified directory. Used to
downsize simulated ant views.

@author tp275
"""

import os
from PIL import Image

path = ('C:/Users/s/Documents/Masters/Project/images/binarised_rotated/')
dirs = os.listdir(path)

def crop_resize():
    for item in dirs:
        if os.path.isfile(path+item):
            im = Image.open(path+item)
			
#            w, h = im.size
#            im = im.crop((0, 9, w, h-9))
			
            f, e = os.path.splitext(path+item)
            imResize = im.resize((90,7), Image.ANTIALIAS)
            imResize.save(f + '.png', 'PNG')

crop_resize()
