import copy
from abc import ABC, abstractmethod
from typing import List, Callable

from .drawing_tool import DrawingTool
from .point import Point
from .style import Style


class Shape(ABC):
    """
    Superclass for drawing different geometric shapes.
    Subclasses define shapes, but drawing, rotation, translation,
    etc. are done in generic functions in this superclass.
    """

    _style: Style

    @abstractmethod
    def __init__(self):
        self._name = None
        self._style = Style()

    def __iter__(self):
        return [self]

    def copy(self):
        return copy.deepcopy(self)

    @abstractmethod
    def draw(self, drawing_tool: DrawingTool) -> None:
        pass

    def animate(
        self,
        drawing_tool: DrawingTool,
        time_points: List[float],
        action: Callable[["Shape", float, float], "Shape"],
        pause_per_frame: float = 0.5,
        dt: float = 0.5,
        title=None,
    ):

        for n, t in enumerate(time_points):
            drawing_tool.erase()

            fig: Shape = action(self, t, dt)
            fig.draw(drawing_tool)

    def draw_dimensions(self, drawing_tool: DrawingTool):
        if hasattr(self, "dimensions"):
            for shape in self.dimensions:
                self.dimensions[shape].draw(drawing_tool)
            return self
        else:
            # raise AttributeError('no self.dimensions dict for defining dimensions of class %s' %
            # self.__classname__.__name__)
            return self

    @abstractmethod
    def rotate(self, angle: float, center: Point) -> "Shape":
        pass

    def translate(self, vec) -> "Shape":
        raise NotImplementedError

    def scale(self, factor) -> "Shape":
        raise NotImplementedError

    # def deform(self, displacement_function):
    #     self._for_all_shapes('deform', displacement_function)
    #     return self

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, style: Style):
        self._style = style

    def set_line_width(self, line_width: float) -> "Shape":
        self.style.line_width = line_width
        return self

    def set_line_style(self, line_style: Style.LineStyle) -> "Shape":
        self.style.line_style = line_style
        return self

    def set_line_color(self, line_color: Style.Color) -> "Shape":
        self.style.line_color = line_color
        return self

    def set_fill_pattern(self, fill_pattern: Style.FillPattern) -> "Shape":
        self.style.fill_pattern = fill_pattern
        return self

    def set_fill_color(self, fill_color: Style.Color) -> "Shape":
        self.style.fill_color = fill_color
        return self

    def set_arrow(self, arrow: Style.ArrowStyle) -> "Shape":
        self.style.arrow = arrow
        return self

    def set_shadow(self, shadow: float) -> "Shape":
        self.style.shadow = shadow
        return self
