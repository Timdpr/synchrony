"""
@author tp275 (unless otherwise stated)
"""

from PIL import Image, ImageChops, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import math

def getRootMeanSquareDiff(im1, im2):
    """
    Calculates the root-mean-square difference between two images
    Modified from 'comparing two images' - github.com/ActiveState/code - and used under the MIT licence
    """
    diff = ImageChops.difference(im1, im2)
    h = diff.histogram()
    sq = (value*((idx%256)**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
    return rms

def getImageList(patterns):
    """
    Turns an array of 'patterns' into an array of PIL images (for use with getRootMeanSquareDiff function)
    """
    imageList = []
    for p in range(len(patterns[0,0])):
        img = Image.fromarray((patterns[:,:,p]*255).astype(np.uint8), mode='L')
        img = ImageOps.invert(img)
        imageList.append(img)
    return imageList

def plotRIDF(patterns):
    """
    """
    imageList = getImageList(patterns)

    ridfs = [getRootMeanSquareDiff(imageList[0], im) for im in imageList]
    ridfs = np.roll(ridfs, len(ridfs)/2)  # shift list so 0 rotation is in the centre
    ridfs /= max(ridfs)  # normalise

    # Plotting...
    plt.clf()
    plt.style.use('seaborn-whitegrid')
    fig, ax = plt.subplots()
    ax.spines['right'].set_visible(False)  # remove borders from right...
    ax.spines['top'].set_visible(False)  # ...and top sides
    plt.xlim(-180, 180)
    plt.ylim(0, 1)
    plt.xlabel('angle ($\degree$)')
    plt.ylabel('RIDF (normalised)')
    plt.xticks([-180, -120, -60, 0, 60, 120, 180])
    fix = 180-(360/len(ridfs)) if len(ridfs) % 2 == 0 else 180  # hacky fix to centralise plot
    plt.plot(np.linspace(-180, fix, num=len(ridfs)), ridfs)
    
    plt.show()
#    plt.savefig('RIDF.svg')
    
def plotRotationSynchrony(results):
    """
    """
    rsyncs = [[] for l in range(len(results[0]))]
    for i, res in enumerate(results[0]):
            rsyncs[i] = res[1]
    
    # Plotting...
    plt.clf()
    plt.style.use('seaborn-whitegrid')
    fig, ax = plt.subplots()
    ax.spines['right'].set_visible(False)  # remove borders from right...
    ax.spines['top'].set_visible(False)  # ...and top sides
    plt.xlim(-180, 180)
    plt.ylim(0, 1)
    plt.xlabel('angle ($\degree$)')
    plt.ylabel(r'$R_{syn}$')
    plt.xticks([-180, -120, -60, 0, 60, 120, 180])
    fix = 180-(360/len(rsyncs)) if len(rsyncs) % 2 == 0 else 180  # hacky fix to centralise plot
    plt.plot(np.linspace(-180, fix, num=len(rsyncs)), [np.mean(rs) for rs in rsyncs])
    plt.fill_between(np.linspace(-180, fix, num=len(rsyncs)),
                     [np.min(rs) for rs in rsyncs], [np.max(rs) for rs in rsyncs], alpha=0.2)
    
    plt.show()
#    plt.savefig('rotation_rsync.svg')
