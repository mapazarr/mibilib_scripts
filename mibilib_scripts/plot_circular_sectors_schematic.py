"""Plot circular sector schematic."""

import matplotlib.pyplot as plt
from matplotlib import patches
import numpy as np

fig, ax = plt.subplots(figsize=(2.5, 2.5))

num_sectors = 8

x = 0.5
y = 0.5
r = 0.2
ang_step = 360./num_sectors
t1 = np.arange(num_sectors)*ang_step
t2 = t1 + ang_step

sectors = []
for i in range(num_sectors):
    sectors.append(patches.Wedge((x, y), r, t1[i], t2[i],
                                 alpha=1, facecolor='none', fill=None, edgecolor='black'))
    ax.add_patch(sectors[i])

# remove plot axes
plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
plt.axis('equal')
plt.axis('off')

plt.show()
