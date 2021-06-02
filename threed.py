import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import math
import numpy as np

X_BOUND = 10
Y_BOUND = 4
Z_BOUND = 5

shift = 0.3

fig = plt.figure()
ax = Axes3D(fig)

i = 0
while (i < 9):
  verts = [[(i,math.sqrt(i)/2,math.sqrt(i)/2), (i,0,0), (i,math.sqrt(i),0)]]
  coll = Poly3DCollection(verts)
  coll.set_edgecolor("#000000")
  ax.add_collection3d(coll)
  i+=shift

x = np.arange(0,X_BOUND,0.1)
ax.plot(x, np.sqrt(x), label="y=sqrt(x)")
ax.plot([9,9], [0,Y_BOUND], label="x=9")

ax.axes.set_xlim3d(left=0, right=X_BOUND)
ax.axes.set_ylim3d(bottom=0, top=Y_BOUND)
ax.axes.set_zlim3d(bottom=0, top=Z_BOUND)
plt.legend()
plt.show()

