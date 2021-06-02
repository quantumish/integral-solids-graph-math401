import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.widgets import TextBox
import math
import numpy as np

SPACIOUS = 1.1

shift = 0.3

fig = plt.figure()

ax = fig.add_subplot(1, 1, 1, projection='3d')
plt.subplots_adjust(bottom=0.2)

def draw(f="math.sqrt(x)", bound=9):
    ax.clear()
    x = 0
    while (x < 9):
        verts = [[(x,eval(f)/2,eval(f)/2), (x,0,0), (x,eval(f),0)]]
        coll = Poly3DCollection(verts)
        coll.set_edgecolor("#000000")
        ax.add_collection3d(coll)
        x+=shift
    x_smooth = np.arange(0,bound*SPACIOUS,0.1)
    y_smooth = [eval(f) for x in x_smooth]
    y_max = max(y_smooth)
    y_min = min(y_smooth)
    ax.plot(x_smooth, y_smooth, label="y=%s"%f)
    ax.plot([bound,bound], [y_min*SPACIOUS if (y_min < 0) else 0, y_max], label="x=%d"%bound)
    ax.axes.set_xlim3d(left=0, right=bound*SPACIOUS)
    ax.axes.set_ylim3d(bottom=y_min*SPACIOUS if (y_min < 0) else 0, top=y_max*SPACIOUS)
    ax.axes.set_zlim3d((y_min/2)*SPACIOUS if (y_min < 0) else 0, top=y_max*SPACIOUS)
    plt.draw()

def f_submit(func):
    draw(func)

axbox = plt.axes([0.1, 0.05, 0.8, 0.075])
f_text_box = TextBox(axbox, 'f(x)', initial="math.sqrt(x)")
f_text_box.on_submit(f_submit)
draw()
plt.show()

