"""
@author tp275 (unless otherwise stated)
"""

from PIL import Image, ImageChops, ImageOps
 
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


def getIDF(dataset, distance):
    patterns = getPatterns.getPatternsInDirectory(
                'C:/Users/s/Documents/Masters/Project/images/exp_distance/' + dataset + '/' + str(distance) + '/', 7, 90, rotation=False)
    image_list = getImageList(patterns)
    
    route_patterns = getPatterns.getPatternsInDirectory(
                'C:/Users/s/Documents/Masters/Project/images/exp_distance/' + dataset + '_to_compare/' + str(distance) + '/', 7, 90, rotation=False)
    route_image_list = getImageList(route_patterns)
    
    idfs = []
    for i in range(len(image_list)):
        idfs.append(getRootMeanSquareDiff(route_image_list[i], image_list[i]))
    
    return(idfs)
    
    
def get_average_IDF(dataset, distance):
    patterns = getPatterns.getPatternsInDirectory(
                'C:/Users/s/Documents/Masters/Project/images/exp_distance/' + dataset + '/' + str(distance) + '/', 7, 90, rotation=False)
    image_list = getImageList(patterns)
    
    route_patterns = getPatterns.getPatternsInDirectory(
                'C:/Users/s/Documents/Masters/Project/synchrony/images/routes/route_' + dataset + '_90x7/', 7, 90, rotation=False)
    route_image_list = getImageList(route_patterns)
    
    mean_idfs = []
    for image in image_list:
        idfs = []
        for route_image in route_image_list:
            idfs.append(getRootMeanSquareDiff(image, route_image))
        mean_idfs.append(np.mean(idfs))
    
    return(mean_idfs)


def do_scatter_plot(x, y):
    plt.figure(figsize=(5,5))
    ax = plt.gca()
    ax.xaxis.set_label_position('top')
    plt.tick_params(top=True, labeltop=True, labelbottom=False, right=True, direction='in')
    plt.grid(linestyle='-', which='major', axis='y',color='black',alpha=0.3)
    plt.scatter(x, y, marker='o',s=30,alpha=0.2,c=(0,0.2,0.8),linewidth=0)
    plt.xlim(-33, 833)
    plt.ylim(0,1)
    plt.xlabel("Distance from route (mm)", labelpad=8)
    plt.ylabel('IDF (normalised)')


x = []
y = []
y_lists = []
for i in range(9):
    y.extend(get_average_IDF('plants', i))
    y_lists.append(get_average_IDF('plants', i))
    x.extend([i*100 for j in range(len(y_lists[i]))])

max_y = np.max(y)
y = y/max_y
y_lists = [l/max_y for l in y_lists]
    
do_scatter_plot(x, y)



par = np.polyfit(x, y, 1, full=True)

slope = par[0][0]
intercept = par[0][1]
xl = [min(x), max(x)]
yl = [slope*xx + intercept for xx in xl]

# Calculate coefficient of determination and print or plot
variance = np.var(y)
residuals = np.var([(slope*xx + intercept - yy)  for xx,yy in zip(x,y)])
Rsqr = np.round(1-residuals/variance, decimals=2)
#text(.9*max(xd)+.1*min(xd),.9*max(yd)+.1*min(yd),'$R^2 = %0.2f$'% Rsqr, fontsize=5)
print('R^2 = ' + str(Rsqr))

# Calculate error bounds
yerr = [abs(slope*xx + intercept - yy)  for xx,yy in zip(x,y)]
par = np.polyfit(x, yerr, 2, full=True)
yerrUpper = [(xx*slope+intercept)+(par[0][0]*xx**2 + par[0][1]*xx + par[0][2]) for xx,yy in zip(x,y)]
yerrLower = [(xx*slope+intercept)-(par[0][0]*xx**2 + par[0][1]*xx + par[0][2]) for xx,yy in zip(x,y)]

# Plot best fit and error lines
#plt.plot(xl, yl, '-r')
#plt.plot(x, yerrLower, '--r', linewidth=1.2)
#plt.plot(x, yerrUpper, '--r', linewidth=1.2)

new_means = [np.mean(yl) for yl in y_lists]
stds_above = [np.std(yl) for yl in y_lists]
stds_below = [np.std(yl) for yl in y_lists]
#for i in range(len(new_means)):
#    stds_above[i] = new_means[i] + stds_below[i]
#    stds_below[i] = new_means[i] - stds_below[i]
#    
(_, caps, _) = plt.errorbar(np.linspace(0, 800, 9), new_means, yerr=np.vstack([stds_below, stds_above]), color='k', fmt='none', capsize=4, elinewidth=2)
for cap in caps:
    cap.set_markeredgewidth(1.5)
   
plt.plot(np.linspace(0, 800, 9), new_means, '-r')
#plt.fill_between(np.linspace(0, 800, 9), stds_above, stds_below, alpha=0.2)
#plt.plot(np.linspace(0, 800, 9), stds_above, alpha=0.3, color='#1f77b4', linewidth=1)
#plt.plot(np.linspace(0, 800, 9), stds_below, alpha=0.3, color='#1f77b4', linewidth=1)


x = []
y = []
y_lists = []
for i in range(9):
    y.extend(getIDF('plants', i))
    y_lists.append(getIDF('plants', i))
    x.extend([i*100 for j in range(len(y_lists[i]))])

max_y = np.max(y)
y = y/max_y
y_lists = [l/max_y for l in y_lists]
new_means = [np.mean(yl) for yl in y_lists]
plt.plot(np.linspace(0, 800, 9), new_means, c=(0,0.2,0.8), zorder=0)


plt.savefig('ext_idf_.pdf', bbox_inches='tight')