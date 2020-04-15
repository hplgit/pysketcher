from .matplotlibdraw import MatplotlibDraw
from .point import Point
from .line import Line


class Arrow(Line):
    """Draw an arrow as Line with arrow pointing towards end."""

    def __init__(self, start: Point, end: Point, drawing_tool: MatplotlibDraw):
        super().__init__(start, end, drawing_tool, arrow='->')


class DoubleArrow(Line):
    """Draw an arrow as Line with arrow pointing towards start and end."""

    def __init__(self, start: Point, end: Point, drawing_tool: MatplotlibDraw):
        super().__init__(start, end, drawing_tool, arrow='<->')
