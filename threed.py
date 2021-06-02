import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.widgets import TextBox
import math
import numpy as np
from typing import Final, List, Tuple

SPACIOUS: Final[float] = 1.1

fig: plt.Figure = plt.figure(figsize=(8, 5))
ax: Axes = fig.add_subplot(1, 1, 1, projection='3d')
plt.subplots_adjust(bottom=0.2)

cache: List[str] = ["math.sqrt(x)", "9", "0.3"]

def draw(f: str, bound: float, shift: float) -> None:
    cache[0], cache[1], cache[2] = f, str(bound), str(shift)
    ax.clear()
    x: float = 0
    while (x < bound):
        verts: List[List[Tuple[float,float,float]]]
        verts = [[(x,eval(f)/2,eval(f)/2), (x,0,0), (x,eval(f),0)]]
        coll: Poly3DCollection = Poly3DCollection(verts)
        coll.set_edgecolor("#000000")
        ax.add_collection3d(coll)
        x+=shift
    x_smooth: np.ndarray = np.arange(0,bound*SPACIOUS,0.1)
    y_smooth: List[float] = [eval(f) for x in x_smooth]
    y_max: float = max(y_smooth)
    y_min: float = min(y_smooth)
    ax.plot(x_smooth, y_smooth, label="f(x)")
    ax.plot([bound,bound], [y_min*SPACIOUS if (y_min < 0) else 0, y_max*SPACIOUS], label="bound")
    ax.axes.set_xlim3d(left=0, right=bound*SPACIOUS)
    ax.axes.set_ylim3d(bottom=y_min*SPACIOUS if (y_min < 0) else 0, top=y_max*SPACIOUS)
    ax.axes.set_zlim3d((y_min/2)*SPACIOUS if (y_min < 0) else 0, top=y_max*SPACIOUS)
    ax.legend()
    plt.draw()
    
f_axbox: Axes = plt.axes([0.1, 0.05, 0.8, 0.075])
f_text_box: TextBox = TextBox(f_axbox, 'f(x)', initial="math.sqrt(x)")
f_text_box.on_submit(lambda text: draw(text, float(cache[1]), float(cache[2])))

b_axbox: Axes = plt.axes([0.1, 0.15, 0.1, 0.075])
b_text_box: TextBox = TextBox(b_axbox, 'bound ', initial="9")
b_text_box.on_submit(lambda text: draw(cache[0], float(text), float(cache[2])))

s_axbox: Axes = plt.axes([0.25, 0.15, 0.1, 0.075])
s_text_box: TextBox = TextBox(s_axbox, 'shift ', initial="0.3")
s_text_box.on_submit(lambda text: draw(cache[0], float(cache[1]), float(text)))

draw(cache[0], float(cache[1]), float(cache[2]))
plt.show()

