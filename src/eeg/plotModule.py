from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import scipy.interpolate
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt

# plot 2d array image
def show_image(im, color = 'rainbow'):
    fig = plt.imshow(im, cmap = color) #'YlOrRd', 'gray'
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
# =========================================
    
# plot 1d array as a head contour 
def head_plot(values):
    meanR = values
    
    # parameters
    N = 300             # number of points for interpolation
    xy_center = [4,4]
    radius = 5
    
    koord = [[3,8],[5,8],# 2
             [3,7],[5,7],# 2
             [0,6],[2,6],[4,6],[6,6],[8,6], # 5
             [1,5],[3,5],[5,5],[7,5],# 4
             [0,4],[2,4],[4,4],[6,4],[8,4], # 5
             [1,3],[3,3],[5,3],[7,3],# 4
             [0,2],[2,2],[4,2],[6,2],[8,2],# 4
             [3,1],[5,1],
             [3,0],[4,0],[5,0]]
    
    ch = ["FP1", "FP2",
         "AF3", "AF4",
         "F7", "F3", "F2", "F4", "F8",
         "FC5", "FC1", "FC2", "FC6",
         "T7", "C3", "CZ", "C4", "T8",
         "CP5", "CP1", "CP2", "CP6",
         "P7", "P3", "PZ", "P4", "P8",
         "PO3", "PO4",
         "O1", "OZ", "O2"]

    xi = np.linspace(0, 8, N)
    yi = np.linspace(0, 8, N)

    x,y = [],[]
    for i in koord:
        x.append(i[0])
        y.append(i[1])
    z = meanR
    zi = scipy.interpolate.griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')

    # set points > radius to not-a-number. They will not be plotted.
    # the dr/2 makes the edges a bit smoother
    dr = xi[1] - xi[0]
    for i in range(N):
        for j in range(N):
            r = np.sqrt((xi[i] - xy_center[0])**2 + (yi[j] - xy_center[1])**2)
            if (r - dr/2) > radius:
                zi[j,i] = "nan"

    # make figure
    fig = plt.figure()

    # set aspect = 1 to make it a circle
    ax = fig.add_subplot(111, aspect = 1)

    # use different number of levels for the fill and the lines
    #CS = ax.contourf(xi, yi, zi, 60, cmap = plt.cm.jet, zorder = 1)
    CS = ax.contourf(xi, yi, zi, 60, cmap = 'rainbow', zorder = 1)
    
    # hide ==============================================
    # 경계선
    ax.contour(xi, yi, zi, 15, colors = "grey", zorder = 2)
    
    # electrode 위치 
    # ax.scatter(x, y, marker = 'o', c = 'b', s = 15, zorder = 3)
    
    # circle
    # circle = matplotlib.patches.Circle(xy = xy_center, radius = radius, edgecolor = "k", facecolor = "none")
    # ax.add_patch(circle)
    
    # color bar
    #cbar = fig.colorbar(CS, ax=ax)
    
    # axis invisible 
    for loc, spine in ax.spines.items():
        spine.set_linewidth(0)
        
    # remove the ticks
    ax.set_xticks([])
    ax.set_yticks([])
    # ===================================================

    # set axes limits
    #ax.set_xlim(-0.5, 8.5); ax.set_ylim(-0.5, 8.5)

    fig.canvas.draw()
    
    arr = np.array(fig.canvas.renderer._renderer)
    
    #print(arr.shape) # (288, 432, 4)
    
    #plt.savefig('hi2.png')
    plt.show() # ****