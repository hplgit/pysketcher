from .line import Line
from .matplotlibdraw import MatplotlibDraw
from .point import Point
from .style import Style


class Arrow(Line):
    """Draw an arrow as Line with arrow pointing towards end."""

    def __init__(self, start: Point, end: Point):
        super().__init__(start, end)
        self.style.arrow = Style.ArrowStyle.END


class DoubleArrow(Line):
    """Draw an arrow as Line with arrow pointing towards start and end."""

    def __init__(self, start: Point, end: Point):
        super().__init__(start, end)
        self.style.arrow = Style.ArrowStyle.DOUBLE
