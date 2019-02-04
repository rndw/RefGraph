#GRIPS
#Graph Representation and Interactive Plotting Suite - The companion to DyeDot and Dottler

import matplotlib.pyplot as plt
import matplotlib.colors as cols # needed for RGBA decimal conversion
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np

#data
coor = [[5,12,0.0],[2,8,0.0],[18,150,0.0],[50,155,0.0],[4,15,0.0],[77,100,0.0],[29,110,0.0],[20,54,0.0],[8,11,0.0],[10,21,0.0],[20,28,0.0],[25,41,0.0],[30,51,0.0],[50,80,0.0],[63,77,0.0],[66,70,0.0],[80,100,0.0],[120,135,0.0]]
# Could use zip to read in each value as a list and bind to tuples
coor = sorted(coor)
#mini = min([_[0] for _ in coor])
#maxrange = max([_[1] for _ in coor])

# build base level
builder = []
builder.append(coor[0])
coor.pop(0)
lvl = builder[-1][2]
# Semi-greedy placement of fragments
def tighthierarchy(lvl = lvl, lvlshift = False):

        # While there are blocks left to add, keep loop running
        while coor:
            # Loop controller. Init walker loop after level shift
            # Initialise loop control of new level

            item = [_ for _ in coor if _[0] >= builder[-1][1]][0]
            builder.append(item)
            coor.pop(coor.index(item))
            builder[-1][2] = lvl
            #break back into main worker loop
            lvlshift = False

            # Main walker - places fragments
            while not lvlshift:
                print('Placing fragment blocks in sequence window')
                while [_ for _ in coor if _[0] >= builder[-1][1]]:
                    item = sorted(list([_ for _ in coor if _[0] >= builder[-1][1]]))[0]
                    builder.append(item)
                    coor.pop(coor.index(item))
                    builder[-1][2] = lvl

                # Main level shifter. Initialises new level.
                # Insert starting block for new level
                print('No more space in current level. Shifting levels and initialising walker.')
                lvl = lvl + 0.2
                item = sorted(coor)[0]
                builder.append(item)
                coor.pop(coor.index(item))
                builder[-1][2] = lvl
                lvlshift = True

# Loose layout. More levels and gaps. Tight is default.
def loosehierarchy(coor = coor):
    for i in range(1, len(coor)):

        if coor[i][0] in range(coor[i-1][0], coor[i - 1][1] + 1):  # should make this a sliding window by adding only overlapping areas
            if myarr[i, 2] == myarr[i - 1, 2]:
                myarr[i, 2] = myarr[i, 2] + 0.2
            if myarr[i, 2] < myarr[i - 1, 2]:
                continue
    for lvl in range(0,len(list(set(myarr[:,2])))):
        subarrA = myarr[myarr[:, 2] == list(set(myarr[:, 2]))[lvl]]
        for k in range(1, len(subarrA)):
            if subarrA[k, 0] in range(int(subarrA[k-1, 0]), int((subarrA[k-1, 1] + 1))):
                subarrA[k,2] = subarrA[k,2] + 0.2

        myarr[myarr[:, 2] == list(set(myarr[:, 2]))[lvl]] = subarrA


tighthierarchy()
#loosehierarchy()

def polyplot(coor = (1,5)):
    for i in range(0,len(coor)):
        if i == 0:
            verts = [
                (coor[i][0], 0.0),  # left, bottom
                (coor[i][0], 0.2),  # left, top
                (coor[i][1] - round((coor[i][1] - coor[i][0])*0.1), 0.2),  # right, top
                (coor[i][1], 0.1),  # right, bottom
                (coor[i][1] - round((coor[i][1] - coor[i][0])*0.1), 0.0),
                (0., 0.), ]  # ignored
            codes = [Path.MOVETO,
                     Path.LINETO,
                     Path.LINETO,
                     Path.LINETO,
                     Path.LINETO,
                     Path.CLOSEPOLY,
                     ]
            path = Path(verts, codes)
            patch = patches.PathPatch(path, facecolor=(1.0, 1.0, 0.0, 0.2), lw=0.8, edgecolor=(0, 0, 0, 1), label="testing")
            ax.add_patch(patch)
        else:
            verts = [
                (coor[i][0], coor[i][2]),  # left, bottom
                (coor[i][0], coor[i][2] + 0.2),  # left, top
                (coor[i][1] - round((coor[i][1] - coor[i][0])*0.1), coor[i][2] + 0.2),  # right, top
                (coor[i][1], coor[i][2] + 0.2 - 0.1),  # right, bottom
                (coor[i][1] - round((coor[i][1] - coor[i][0])*0.1), coor[i][2]),
                (coor[i][2], coor[i][2]), ]  # ignored
            codes = [Path.MOVETO,
                     Path.LINETO,
                     Path.LINETO,
                     Path.LINETO,
                     Path.LINETO,
                     Path.CLOSEPOLY,
                     ]
            path = Path(verts, codes)
            patch = patches.PathPatch(path, facecolor=(1.0, 1.0, 0.0, 0.2), lw=0.8, edgecolor=(0, 0, 0, 1), label="testing")
            ax.add_patch(patch)

fig = plt.figure()
ax = fig.add_subplot(111)
polyplot(builder)


plt.autoscale()
#ax.set_xlim(0,140)
#ax.set_ylim(0,0.5)
plt.show()

#check colour values
#cols.to_rgba("yellow",0.4)