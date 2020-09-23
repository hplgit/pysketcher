import copy
from abc import ABC, abstractmethod
from typing import Callable, List

from .drawing_tool import DrawingTool
from .point import Point
from .style import Style


class Stylable(ABC):

    _style: Style

    @abstractmethod
    def __init__(self):
        self._style = Style()

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, style: Style):
        self._style = style

    def set_line_width(self, line_width: float) -> "Stylable":
        self.style.line_width = line_width
        return self

    def set_line_style(self, line_style: Style.LineStyle) -> "Stylable":
        self.style.line_style = line_style
        return self

    def set_line_color(self, line_color: Style.Color) -> "Stylable":
        self.style.line_color = line_color
        return self

    def set_fill_pattern(self, fill_pattern: Style.FillPattern) -> "Stylable":
        self.style.fill_pattern = fill_pattern
        return self

    def set_fill_color(self, fill_color: Style.Color) -> "Stylable":
        self.style.fill_color = fill_color
        return self

    def set_arrow(self, arrow: Style.ArrowStyle) -> "Stylable":
        self.style.arrow = arrow
        return self

    def set_shadow(self, shadow: float) -> "Stylable":
        self.style.shadow = shadow
        return self


class Shape(Stylable):
    """
    Superclass for drawing different geometric shapes.
    Subclasses define shapes, but drawing, rotation, translation,
    etc. are done in generic functions in this superclass.
    """

    @abstractmethod
    def __init__(self):
        super().__init__()
        self._name = None

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

    @abstractmethod
    def rotate(self, angle: float, center: Point) -> "Shape":
        raise NotImplementedError

    def translate(self, vec) -> "Shape":
        raise NotImplementedError

    def scale(self, factor) -> "Shape":
        raise NotImplementedError
