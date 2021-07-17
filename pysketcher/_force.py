from pysketcher._arrow import Arrow
from pysketcher._point import Point
from pysketcher._style import Style
from pysketcher.annotation import LineAnnotation, TextPosition
from pysketcher.composition import Composition


class Force(Composition):
    """A composition of Arrow and LinearAnnotation."""

    def __init__(
        self,
        text: str,
        start: Point,
        end: Point,
        text_position: TextPosition = TextPosition.MIDDLE,
    ):
        self._text = text
        self._start = start
        self._end = end

        self._arrow = Arrow(start, end)
        self._label = LineAnnotation(text, self._arrow, text_position)
        super().__init__({"arrow": self._arrow, "label": self._label})


class Gravity(Force):
    """Downward-pointing gravity arrow with the symbol g."""

    # TODO: add the g

    def __init__(
        self,
        start,
        length,
    ):
        Force.__init__(self, "$g$", start, start + Point(0, -length))
        self.style.line_color = Style.Color.BLACK
