import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import mpl_toolkits.mplot3d.art3d as art3d
from matplotlib.patches import Circle
from matplotlib.widgets import TextBox
from matplotlib.widgets import RadioButtons
import math
import numpy as np
import textwrap
from typing import Final, List, Tuple, Callable, Dict
from enum import Enum

SPACIOUS: Final[float] = 1.1

class Solid: 
    def __init__(self, f: str = "math.sqrt(x)",  bound: str = "0,9", shift: float = 0.3) -> None:
        self.function: str = f
        self.bounds: str = bound
        self.shift: float = shift
        self.cross_section: Callable[[float], Poly3DCollection] = None
        self.set_cross_section("Isosceles") 

        self.fig: plt.Figure = plt.figure(figsize=(10, 6.8))
        self.ax: Axes = self.fig.add_subplot(1, 1, 1, projection='3d')
        plt.subplots_adjust(bottom=0.25)
        plt.subplots_adjust(top=1)        
        self.__draw()

        f_axbox: Axes = plt.axes([0.1, 0.05, 0.63, 0.075])
        f_text_box: TextBox = TextBox(f_axbox, 'f(x)', initial="math.sqrt(x)")
        f_text_box.on_submit(lambda x: self.update(self.set_function, x))
        
        b_axbox: Axes = plt.axes([0.1, 0.15, 0.1, 0.075])
        b_text_box: TextBox = TextBox(b_axbox, 'bound ', initial="0,9")
        b_text_box.on_submit(lambda x: self.update(self.set_bounds, x))
        
        s_axbox: Axes = plt.axes([0.25, 0.15, 0.1, 0.075])
        s_text_box: TextBox = TextBox(s_axbox, 'shift ', initial="0.3")
        s_text_box.on_submit(lambda x: self.update(self.set_spacing, x))

        r_axbox: Axes = plt.axes([0.75, 0.05, 0.15, 0.170], facecolor='#f4f4f4')
        radio: RadioButtons = RadioButtons(r_axbox, ('Isosceles', 'Rectangle', 'Equilateral'), activecolor="#428abd")
        radio.on_clicked(lambda x: self.update(self.set_cross_section, x))

        self.fig.text(0.01,0.7, "\n".join(textwrap.wrap("Hello! You can swivel the graph with the mouse. Set the bounds by writing two numbers and separating them wit a comma. You can write any function that's a valid python expression (we've imported the math library for your convienience). Setting a value for 'shift' will control the spacing of the cross-sections. Finally, the radio buttons on the right can be used to choose which type of cross-sections to graph.", 30)), fontsize="small")
        
        plt.show()

    @staticmethod
    def create_polygon(verts: List[Tuple]) -> Poly3DCollection:
        coll: Poly3DCollection = Poly3DCollection(verts)
        coll.set_edgecolor("#000000")
        return coll

    @staticmethod
    def create_curve() -> None:
        raise NotImplementedError

    def update(self, setter: Callable[[str], None], text: str) -> None:
        setter(text)
        self.__draw()
    
    def set_bounds(self, bound: str) -> None:
        self.bounds = bound

    def set_function(self, func: str) -> None:
        self.function = func

    def set_spacing(self, interval: str) -> None:
        self.shift = float(interval)

    def set_cross_section(self, cross: str) -> None:
        if cross == "Isosceles":
            self.cross_section = lambda x: self.create_polygon(
                [(x,eval(self.function)/2,eval(self.function)/2), (x,0.0,0.0), (x,eval(self.function),0)])
            self.__max_z_multiplier = 0.5
        elif cross == "Rectangle":
            self.cross_section = lambda x: self.create_polygon(
            [(x,eval(self.function),eval(self.function)*2), (x,0,eval(self.function)*2), (x,0.0,0.0), (x,eval(self.function),0.0)])
            self.__max_z_multiplier = 2
        elif cross == "Semicircle":
            raise NotImplementedError
        elif cross == "Equilateral":
            self.cross_section = lambda x: self.create_polygon(
                [(x,eval(self.function)/2,eval(self.function)*math.sqrt(3)/2), (x,0.0,0.0), (x,eval(self.function),0)])
            self.__max_z_multiplier = math.sqrt(3)/2
        else: 
            raise RuntimeError("Invalid cross section!")

    def __draw(self) -> None: 
        self.ax.clear()
        bounds: List[float] = [float(x) for x in self.bounds.split(",")] 
        x: float = bounds[0]
        while (x < bounds[1]):
            self.ax.add_collection3d(self.cross_section(x))          
            x+=self.shift
        x_smooth: np.ndarray = np.arange(bounds[0],bounds[1]*SPACIOUS,0.1)
        y_smooth: List[float] = [eval(self.function) for x in x_smooth]
        y_max: float = max(y_smooth)
        y_min: float = min(y_smooth)
        self.ax.plot(x_smooth, y_smooth, label="f(x)")
        self.ax.plot([bounds[1],bounds[1]], [y_min*SPACIOUS if (y_min < 0) else 0, y_max*SPACIOUS], label="bound")
        self.ax.axes.set_xlim3d(left=bounds[0], right=bounds[1]*SPACIOUS)
        self.ax.axes.set_ylim3d(bottom=y_min*SPACIOUS if (y_min < 0) else 0, top=y_max*SPACIOUS)
        self.ax.axes.set_zlim3d((y_min*self.__max_z_multiplier)*SPACIOUS if (y_min < 0) else 0,      
                                top=y_max*self.__max_z_multiplier*SPACIOUS if self.__max_z_multiplier > 1 else y_max*SPACIOUS)
        self.ax.legend()
        plt.draw()
    
s = Solid()
