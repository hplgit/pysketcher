from pysketcher.arrow_with_text import ArrowWithText
from pysketcher.point import Point
from pysketcher.style import Style


class Force(ArrowWithText):
    """Another name for `ArrowWithText` to make code easier to read"""

    pass


class Gravity(Force):
    """Downward-pointing gravity arrow with the symbol g."""

    def __init__(
        self,
        start,
        length,
        text_position: ArrowWithText.TextPosition = ArrowWithText.TextPosition.START,
        text="$g$",
    ):
        Force.__init__(
            self, text, start, start + Point(0, -length), text_position=text_position
        )
        self.style.line_color = Style.Color.BLACK
