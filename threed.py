import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.widgets import TextBox
import math
import numpy as np
from typing import Final, List, Tuple, Callable, Dict
from enum import Enum

SPACIOUS: Final[float] = 1.1

# fig: plt.Figure = plt.figure(figsize=(8, 5))
# ax: Axes = fig.add_subplot(1, 1, 1, projection='3d')
# plt.subplots_adjust(bottom=0.25)
# plt.subplots_adjust(top=1)

# cache: List[str] = ["math.sqrt(x)", "0-9", "0.3"]

class CrossSection(Enum):
    isosceles = 0.5
    rectangle = 2
    semicircle = 1
    equilateral = math.sqrt(3)/2

class Graph: 
    def __init__(self, f: str = "math.sqrt(x)",  bound: str = "0-9", shift: float = 0.3) -> None:
        self.function: str = f
        self.bounds: str = bound
        self.shift: float = shift
        self.cross_section: Callable[[float], List[Tuple]] = None
        self.set_cross_section(CrossSection.rectangle)      
        self.fig: plt.Figure = plt.figure(figsize=(8, 5))
        self.ax: Axes = self.fig.add_subplot(1, 1, 1, projection='3d')

        plt.subplots_adjust(bottom=0.25)
        plt.subplots_adjust(top=1)

        self.__draw()
        plt.show()

    def set_cross_section(self, cross: CrossSection):
        if cross == CrossSection.isosceles:
            self.cross_section = lambda x: [(x,eval(self.function)/2,eval(self.function)/2), (x,0.0,0.0), (x,eval(self.function),0)]
        elif cross == CrossSection.rectangle:
            self.cross_section = lambda x: [(x,eval(self.function),eval(self.function)*2), (x,0,eval(self.function)*2), (x,0.0,0.0), (x,eval(self.function),0.0)]
        elif cross == CrossSection.semicircle:
            pass
        elif cross == CrossSection.equilateral:
            pass
        else: 
            raise RuntimeError("Invalid cross section!")
        self.__max_z_multiplier = cross.value

    def __draw(self) -> None: 
        self.ax.clear()
        bounds: List[float] = [float(x) for x in self.bounds.split("-")] 
        x: float = bounds[0]
        while (x < bounds[1]):
            verts: List[Tuple]
            verts = self.cross_section(x)
            print(len(verts))
            coll: Poly3DCollection = Poly3DCollection(verts)
            coll.set_edgecolor("#000000")
            self.ax.add_collection3d(coll) 
            x+=self.shift
        x_smooth: np.ndarray = np.arange(bounds[0],bounds[1]*SPACIOUS,0.1)
        y_smooth: List[float] = [eval(self.function) for x in x_smooth]
        y_max: float = max(y_smooth)
        y_min: float = min(y_smooth)
        self.ax.plot(x_smooth, y_smooth, label="f(x)")
        self.ax.plot([bounds[1],bounds[1]], [y_min*SPACIOUS if (y_min < 0) else 0, y_max*SPACIOUS], label="bound")
        self.ax.axes.set_xlim3d(left=bounds[0], right=bounds[1]*SPACIOUS)
        self.ax.axes.set_ylim3d(bottom=y_min*SPACIOUS if (y_min < 0) else 0, top=y_max*SPACIOUS)
        self.ax.axes.set_zlim3d((y_min*self.__max_z_multiplier)*SPACIOUS if (y_min < 0) else 0, top=y_max*self.__max_z_multiplier*SPACIOUS)
        self.ax.legend()
        plt.draw()
    
# axbox: Axes = plt.axes([0.1, 0.03, 0.8, 0.075])
# f_text_box: TextBox = TextBox(axbox, 'f(x)', initial="math.sqrt(x)")
# f_text_box.on_submit(lambda text: draw(text, float(cache[1]), float(cache[2])))

# b_axbox: Axes = plt.axes([0.1, 0.13, 0.35, 0.075])
# b_text_box: TextBox = TextBox(b_axbox, 'bounds', initial="0-9")
# b_text_box.on_submit(lambda text: draw(cache[0], text, float(cache[2])))

# sxbox: Axes = plt.axes([0.55, 0.13, 0.35, 0.075])
# s_text_box: TextBox = TextBox(sxbox, 'step', initial="0.3")
# s_text_box.on_submit(lambda text: draw(cache[0], float(cache[1]), text))

# draw(cache[0], cache[1], float(cache[2]))
# plt.show()



g = Graph()
