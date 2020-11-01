from pysketcher.line import Line
from pysketcher.point import Point
from pysketcher.style import Style


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
