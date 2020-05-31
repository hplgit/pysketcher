from .arrow_with_text import ArrowWithText
from .point import Point
from .style import Style


class Force(ArrowWithText):
    """Another name for `ArrowWithText` to make code easier to read"""
    pass


class Gravity(Force):
    """Downward-pointing gravity arrow with the symbol g."""

    def __init__(self, start, length, text='$g$'):
        Force.__init__(self, text, start, start + Point(0, -length))
        self.style.line_color = Style.Color.BLACK
