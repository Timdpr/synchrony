"""
@author tp275 (unless otherwise stated)
"""

from PIL import Image, ImageChops, ImageOps
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import numpy as np
import math
import os, sys
hc_path = "../../navLibHC"
sys.path.append(os.path.realpath(hc_path))
import getPatterns

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

def plotRIDF(patterns, image_num, use_single_comparison=False, original_image=None):
    """
    """
    imageList = getImageList(patterns)
    if use_single_comparison:
        ridfs = [getRootMeanSquareDiff(original_image, im) for im in imageList]
    else:
        ridfs = [getRootMeanSquareDiff(imageList[0], im) for im in imageList]
    
    ridfs = np.roll(ridfs, len(ridfs)/2)  # shift list so 0 rotation is in the centre
    ridfs /= max(ridfs)  # normalise
    print(str(image_num) + ':')
    print(str(ridfs))
    print()
    # Plotting...
    plt.clf()
    plt.style.use('seaborn-whitegrid')
    fig, ax = plt.subplots(figsize=(5.5,3.66))
    ax.spines['right'].set_visible(False)  # remove borders from right...
    ax.spines['top'].set_visible(False)  # ...and top sides
    plt.xlim(-180, 180)
    plt.ylim(0, 1.005)
    plt.xlabel('angle ($\degree$)')
    plt.ylabel('RIDF (normalised)')
    plt.xticks([-180, -120, -60, 0, 60, 120, 180])
    fix = 180-(360/len(ridfs)) if len(ridfs) % 2 == 0 else 180  # hacky fix to centralise plot
    print('\n\n\n' + str(np.linspace(-180, fix, num=len(ridfs))) + '\n\n\n')
    plt.plot(np.linspace(-180, fix, num=len(ridfs)), ridfs)
    
    plt.savefig('RIDF_%i.pdf'%(image_num))
    
def plotRotationSynchrony(results, experiment_num):
    """
    """
    # Create list containing lists of rsyncs for each similarity
    rsyncs = [[] for l in range(len(results[0]))]
    for i in range(len(results)):
        for j, res in enumerate(results[i]):
            rsyncs[j].append(res[1])        
    rsyncs = np.roll(rsyncs, len(rsyncs)/2, axis=0)
    
    # Create lists of mean and standard error rsyncs
    means = [np.mean(rs) for rs in rsyncs]
    stds_above = [np.std(rs) for rs in rsyncs]
    stds_below = [np.std(rs) for rs in rsyncs]
    for i in range(len(means)):
        stds_above[i] = means[i] + stds_below[i]
        stds_below[i] = means[i] - stds_below[i]
    
    # Plotting...
    plt.clf()
    plt.style.use('seaborn-whitegrid')
    fig, ax = plt.subplots(figsize=(5.5,3.66))
    ax.spines['right'].set_visible(False)  # remove borders from right...
    ax.spines['top'].set_visible(False)  # ...and top sides
    plt.xlim(-180, 180)
    plt.ylim(0, 1)
    plt.xlabel('angle ($\degree$)')
    plt.ylabel(r'$R_{syn}$')
    plt.xticks([-180, -120, -60, 0, 60, 120, 180])
    
#    fix = 180-(360/len(rsyncs)) if len(rsyncs) % 2 == 0 else 180  # hacky fix to centralise plot
#    x_axis = np.linspace(-180, fix, num=len(rsyncs))
    x_axis = np.linspace(-176, 176, 45) # use with rot_step of 2
#    x_axis = np.linspace(-180, 160, 18) # use with rot_step of 5
    
    plt.plot(x_axis, means)
    plt.fill_between(x_axis, stds_above, stds_below, alpha=0.2)
    plt.plot(x_axis, stds_above, alpha=0.3, color='#1f77b4', linewidth=1)
    plt.plot(x_axis, stds_below, alpha=0.3, color='#1f77b4', linewidth=1)
    plt.show()
#    plt.savefig('rsync_exp%i.pdf'%(experiment_num))
    plt.gca().invert_yaxis()
    
    plt.savefig('rsync_invert_exp%i.pdf'%(experiment_num))
