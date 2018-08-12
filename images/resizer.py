"""
Crops, resizes and saves all images in the specified directory. Used to
downsize simulated ant views.

@author tp275
"""

import os
from PIL import Image

path = ('C:/Users/s/Documents/Masters/Project/images/imdb_boxes_temp/')
dirs = os.listdir(path)

def crop_resize():
    for item in dirs:  # for each image
        if os.path.isfile(path+item):
            im = Image.open(path+item)  # load

            # Adjust this to crop original image.
            # Make sure ratio is correct before resizing!
#            w, h = im.size
#            im = im.crop((0, 9, w, h-9))

            # Resize image and save, overwriting original file
            f, e = os.path.splitext(path+item)
            imResize = im.resize((90,7), Image.ANTIALIAS)
            imResize.save(f + '.png', 'PNG')

crop_resize()
print('Done')
