"""
Function for creating the quiver plot, including quivers, heatmap and route arrow

@author: tp275
"""

import numpy as np
import matplotlib.pyplot as plt

def quiverPlot(x, y, degrees, rsyncs, missing_image_numbers):
    """
    x: List of (columnwise) image x-coordinates (as [0, 0, 0, 100, 100, 100...etc])
    y: List of (rowwise) image y-coordinates (as [0, 100, 200, 0, 100, 200...etc])
    degrees: List of INVERTED degrees away from the x-axis to face
    rsyncs: List of rsync values corresponding to each 'winning' degree value. Annoyingly, this must be in the form of a 2d array
    missingImageNumbers: List of points (numbered as eg. x indices, 1-484) where the image was missing from the dataset
    """
    
    for i in sorted(missing_image_numbers, reverse=True):
        del x[i]  # delete all x/y elements where images were missing, so as
        del y[i]  # not to plot quivers here
        del degrees[i]  # should be able to delete this in proper run
    
    plt.clf()
    plt.style.use('seaborn-white')
    # Plot heatmap of rsyncs
    plt.imshow(rsyncs, cmap='OrRd', extent=[-50, 2850, -50, 1650], aspect='auto', zorder=0)
    plt.colorbar(label=r'$R_{syn}$')
    plt.axis('scaled')
    plt.xlabel('x (mm)')
    plt.ylabel('y (mm)')
    plt.xlim(-100, 2900)
    plt.ylim(-100, 1700)
    plt.xticks((0, 400, 800, 1200, 1600, 2000, 2400, 2800))
    plt.yticks((0, 200, 400, 600, 800, 1000, 1200, 1400, 1600))
    #    plt.scatter(x, y, s=8)  # optionally plot image locations as points
    
    # Plot route arrow
    plt.arrow(0, 800, 1900, 0, color='b', width=10, head_width=40, length_includes_head=True, zorder=1)
    
    # Create vectors, starting with 50 units in the x direction
    u = [50 for i in range(len(x))]  
    v = [0 for i in range(len(y))]
    # Rotate (with 'degrees') and plot vectors
    plt.quiver(x, y, u, v, angles=degrees, zorder=3)
    
#    plt.show()
    plt.savefig('Unnamed Quiver Plot.svg', dpi=400)
    
    
x = [j for j in range(0, 2900, 100) for i in range(17)]
y = [np.linspace(0, 1600, 17) for i in range(29)]
y = [i for a in y for i in a]

degrees = [25 for i in range(493)]
rsyncs = np.random.rand(17, 29)
missing_img_nums = [slice(37, 42), slice(46, 50), slice(52, 59), slice(61, 76), slice(78, 93),
                    slice(95, 110), slice(112, 125), slice(130, 140),slice(147, 153), slice(165, 170),
                    slice(182, 185), slice(222, 226), slice(238, 244), slice(255, 261), slice(272, 279),
                    slice(289, 296), slice(306, 313), slice(323, 330), slice(334, 339), slice(340, 347),
                    slice(348, 356), slice(358, 362), slice(365, 374), slice(382, 391), slice(399, 408),
                    slice(417, 425), slice(434, 442), slice(451, 458), slice(469, 473)]

quiverPlot(x, y, degrees, rsyncs, missing_img_nums)
