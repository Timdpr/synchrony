"""
Function for creating the quiver plot, including quivers, heatmap and route arrow

@author: tp275
"""

import numpy as np
import matplotlib.pyplot as plt

def quiver_plot(degrees, rsyncs, missing_image_numbers):
    """
    degrees: List of INVERTED degrees away from the x-axis to face
    rsyncs: List of rsync values corresponding to each 'winning' degree value. Annoyingly, this must be in the form of a 2d array
    missingImageNumbers: List of points (numbered as eg. x indices, 1-484) where the image was missing from the dataset
    """
    # x: List of (columnwise) image x-coordinates (as [0, 0, 0, 100, 100, 100...etc])
    # y: List of (rowwise) image y-coordinates (as [0, 100, 200, 0, 100, 200...etc])
    x = [j for j in range(0, 2900, 100) for i in range(17)]
    y = [np.linspace(0, 1600, 17) for i in range(29)]
    y = [i for a in y for i in a]
    
    for i in sorted(missing_image_numbers, reverse=True):
        del x[i]  # delete all x/y elements where images were missing, so as
        del y[i]  # not to plot quivers here
        del degrees[i]  # should be able to delete this in proper run
    
    plt.clf()
    plt.style.use('seaborn-white')
    # Plot heatmap of rsyncs
    plt.imshow(rsyncs, cmap='GnBu', extent=[-50, 2850, -50, 1650], aspect='auto', zorder=0)
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
    plt.arrow(0, 800, 1900, 0, color='r', width=10, head_width=40, length_includes_head=True, zorder=1, alpha=0.6)
    
    # Create vectors, starting with 50 units in the x direction
    u = [50 for i in range(len(x))]  
    v = [0 for i in range(len(y))]
    # Rotate (with 'degrees') and plot vectors
    plt.quiver(x, y, u, v, angles=degrees, zorder=3)
    
#    plt.show()
    plt.savefig('Unnamed Quiver Plot.pdf', dpi=400, bbox_inches='tight')
    

def get_rsync_and_rotation(results):
    """
    """
    # Create list containing lists of rsyncs for each similarity
    rsyncs = [[] for l in range(len(results[0]))]
    for i in range(len(results)):
        for j, res in enumerate(results[i]):
            rsyncs[j].append(res[1])
    
    # Create lists of mean rsyncs
    means = [np.mean(rs) for rs in rsyncs]
    max_rsync = max(means)
    rotation_at_max = means.index(max_rsync) * (360/len(means))
    
    return max_rsync, rotation_at_max
    

degrees = [180 for i in range(493)]

rsyncs = np.zeros((17, 29))
for i in range(17):
    for j in range(29):
        rsyncs[i][j] = None

# Row 0:
# Row 1:
degrees[11] = 0
degrees[28] = 0
degrees[45] = -8
degrees[164] = -8
degrees[181] = 24
degrees[198] = 8
degrees[215] = 0
degrees[232] = 40
degrees[249] = -32
degrees[266] = -8
degrees[283] = 16
degrees[300] = -32
degrees[317] = -8

rsyncs[5][0] = 0.5129070004644259
rsyncs[5][1] = 0.5880339047832364
rsyncs[5][2] = 0.634181342870345
rsyncs[5][9] = 0.504115981891652
rsyncs[5][10] = 0.6827783836659811
rsyncs[5][11] = 0.4764924607970681 
rsyncs[5][12] = 0.5207686506060684
rsyncs[5][13] = 0.5975138195403366
rsyncs[5][14] = 0.6403170267078784
rsyncs[5][15] = 0.6411842174943109
rsyncs[5][16] = 0.6502999540852199
rsyncs[5][17] = 0.552700961700731
rsyncs[5][18] = 0.6364704095309562

# Row 1:
degrees[10] = 8 
degrees[27] = 8
degrees[44] = -8
degrees[129] = 8
degrees[146] = 0
degrees[163] = 0
degrees[180] = 24
degrees[197] = -8
degrees[214] = -24
degrees[231] = 16
degrees[248] = 16
degrees[265] = 0
degrees[282] = 32
degrees[299] = -32
degrees[316] = -48
degrees[333] = -8

rsyncs[6][0] = 0.5752872278929857
rsyncs[6][1] = 0.5644070031308875
rsyncs[6][2] = 0.6483035620347336
rsyncs[6][7] = 0.5525163794576562
rsyncs[6][8] = 0.6201984200012501
rsyncs[6][9] = 0.5056851107151907
rsyncs[6][10] = 0.5884659399344887
rsyncs[6][11] = 0.637390783631974
rsyncs[6][12] = 0.6669750623322712
rsyncs[6][13] = 0.6511465377065421
rsyncs[6][14] = 0.6553331171134672
rsyncs[6][15] = 0.6271559725139201
rsyncs[6][16] = 0.7017846608990226
rsyncs[6][17] = 0.6865985177691155
rsyncs[6][18] = 0.5649328717848591
rsyncs[6][19] = 0.6919659474772637

# Row 2:
degrees[9] = -32
degrees[26] = 0
degrees[43] = 0
degrees[60] = -24
degrees[77] = -56
degrees[94] = -8
degrees[111] = -32
degrees[128] = 24
degrees[145] = -16
degrees[162] = 8
degrees[179] = -8
degrees[196] = -8
degrees[213] = -24
degrees[230] = 8
degrees[247] = -40
degrees[264] = 0
degrees[281] = -40
degrees[298] = -40
degrees[315] = 8
degrees[332] = -16

row2 = [[12, 0.5912847927642939], [8, 0.5665644544618238], [8, 0.6679110848671184], [11, 0.6438241293071777], [15, 0.502715708767938], [9, 0.6022554613010315], [12, 0.5109824454605343], [5, 0.5079421496230386], [10, 0.5094359788160513], [8, 0.5279369219630198], [9, 0.6059707392838073], [9, 0.6082564034076249], [11, 0.7111900564891748], [7, 0.5620000189526974], [13, 0.683308333967619], [8, 0.687727636549487], [13, 0.541644405574927], [13, 0.5749037360303046], [7, 0.7108281419125057], [10, 0.6860398487953692]]
for i in range(20):
    rsyncs[7][i] = row2[i][1]
    
# Row 3:
degrees[8] = -16
degrees[25] = -16
degrees[42] = -32
degrees[59] = 0
degrees[76] = -24
degrees[93] = 0
degrees[110] = 16
degrees[127] = -8
degrees[144] = 8
degrees[161] = -24
degrees[178] = -8
degrees[195] = 0
degrees[212] = -56
degrees[229] = -56
degrees[246] = -16
degrees[263] = 0
degrees[280] = 0
degrees[297] = 8
degrees[314] = 0
degrees[331] = -8
    
row3 = [[10, 0.6113110166199388], [10, 0.6027148263722508], [12, 0.6470821960438291], [8, 0.613287065697927], [11, 0.5576724973586925], [8, 0.6131568356265611], [6, 0.6464509429945722], [9, 0.6594453378610121], [7, 0.5672833211709803], [11, 0.6508669510004705], [9, 0.6032644856429038], [9, 0.6576833190130104], [15, 0.46973167898425977], [15, 0.40685870593529966], [10, 0.5585722503100459], [8, 0.5339785070535736], [8, 0.6458424764352233], [7, 0.5443499376204833], [8, 0.6695310221682336], [9, 0.5050374218074382]]
for i in range(20):
    rsyncs[8][i] = row3[i][1]

# Row 4:
degrees[7] = -56
degrees[24] = -8
degrees[126] = -48
degrees[143] = -8
degrees[160] = 0
degrees[177] = 0
degrees[194] = -16
degrees[211] = -32
degrees[228] = -16
degrees[245] = -16
degrees[262] = -8
degrees[279] = 8
degrees[296] = -24
degrees[313] = -8
degrees[330] = -8

rsyncs[9][0] = 0.38109465976689283
rsyncs[9][1] = 0.5277432986544254
rsyncs[9][7] = 0.44299066257097575
rsyncs[9][8] = 0.36270447262357236
rsyncs[9][9] = 0.5876336141682909
rsyncs[9][10] = 0.41483815555147874
rsyncs[9][11] = 0.5590726650579119
rsyncs[9][12] = 0.6259670125062795
rsyncs[9][13] = 0.6270416901941908
rsyncs[9][14] = 0.5851098103344459
rsyncs[9][15] = 0.5925131062625023
rsyncs[9][16] = 0.4924802672942673
rsyncs[9][17] = 0.6305706004945238
rsyncs[9][18] = 0.6325106932252237
rsyncs[9][19] = 0.5710040830311484

## Row 5:
degrees[6] = -8
degrees[23] = 0
degrees[125] = 0
degrees[142] = 0
degrees[159] = -8
degrees[176] = -8
degrees[193] = -8
degrees[210] = -32
degrees[227] = -16
degrees[244] = 0
degrees[261] = 0

rsyncs[10][0] = 0.40273214958373976
rsyncs[10][1] = 0.4198434211281956
rsyncs[10][7] = 0.5790814035288718
rsyncs[10][8] = 0.5742089847966251
rsyncs[10][9] = 0.42308547151951054
rsyncs[10][10] = 0.5826359442842088
rsyncs[10][11] = 0.5477126074032987
rsyncs[10][12] = 0.660099265212578
rsyncs[10][13] = 0.5965751490869053
rsyncs[10][14] = 0.4023084537789005
rsyncs[10][15] = 0.502438953460441

# Row 6:

degrees[5] = -8
degrees[22] = -8
degrees[141] = 32
degrees[158] = -8
degrees[175] = 0
degrees[192] = 24
degrees[209] = 0
degrees[226] = 0

rsyncs[11][0] = 0.6117959187348126
rsyncs[11][1] = 0.5711135796288239
rsyncs[11][8] = 0.32957571999864704
rsyncs[11][9] = 0.5591528754554438
rsyncs[11][10] = 0.5599770707655568 
rsyncs[11][11] = 0.33362787605542854
rsyncs[11][12] = 0.4881597168977805
rsyncs[11][13] = 0.641267878035405



missing_img_nums = [slice(37, 42), slice(46, 50), slice(52, 59), slice(61, 76), slice(78, 93),
                    slice(95, 110), slice(112, 125), slice(130, 140),slice(147, 153), slice(165, 170),
                    slice(182, 185), slice(222, 226), slice(238, 244), slice(255, 261), slice(272, 279),
                    slice(289, 296), slice(306, 313), slice(323, 330), slice(334, 339), slice(340, 347),
                    slice(348, 356), slice(358, 362), slice(365, 374), slice(382, 391), slice(399, 408),
                    slice(417, 425), slice(434, 442), slice(451, 458), slice(469, 473)]

quiver_plot(degrees, rsyncs, missing_img_nums)
