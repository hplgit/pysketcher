from enum import Enum, auto

from pysketcher.arrow import DoubleArrow
from pysketcher.arrow_with_text import Text
from pysketcher.composition.composition import ShapeWithText
from pysketcher.point import Point


class DistanceWithText(ShapeWithText):
    """
    Arrow <-> with text (usually a symbol) at the midpoint, used for
    identifying a some distance in a figure.  The text is placed
    slightly to the right of vertical-like arrows, with text displaced
    `text_spacing` times to total distance in x direction of the plot
    area. The text is by default aligned 'left' in this case. For
    horizontal-like arrows, the text is placed the same distance
    above, but aligned 'center' by default (when `alignment` is None).
    """

    class TextPosition(Enum):
        START = auto()
        MIDDLE = auto()
        END = auto()

        def swap(self) -> "TextPosition":
            swap_dict = {
                self.START: self.END,
                self.END: self.START,
                self.MIDDLE: self.MIDDLE,
            }
            return swap_dict[self]

    def __init__(
        self,
        text: str,
        start: Point,
        end: Point,
        spacing: float = 1 / 3.0,
        text_position: TextPosition = TextPosition.MIDDLE,
    ):
        self._start = start
        self._end = end

        # Decide first if we have a vertical or horizontal arrow
        vertical = abs(end.x - start.x) < 2 * abs(end.y - start.y)

        if vertical:
            # Force end above start
            if end.y < start.y:
                start, end = end, start
                text_position = text_position.swap()
        else:  # horizontal arrow
            # Force start to the right of end
            if start.x < end.x:
                start, end = end, start
                text_position = text_position.swap()

        normal = (end - start).normal()

        if text_position == self.TextPosition.MIDDLE:
            # if the text is in the middle of the line, then place it
            # at a point spacing away normal to the midpoint
            mid = (start + end) * 0.5  # midpoint of start-end line
            text_point = mid - normal * spacing
        elif text_position == self.TextPosition.START:
            # if the text is at the start of the line, then place it
            # at a point spacing away normal to the start
            text_point = start - normal * spacing
        elif text_position == self.TextPosition.END:
            # if the text is at the start of the line, then place it
            # at a point spacing away normal to the end
            text_point = end - normal * spacing
        else:
            raise ValueError(
                "The value of `text_position`: %s is not valid", text_position
            )

        text = Text(text, text_point)

        arrow = DoubleArrow(start, end)
        arrow.line_color = "black"
        arrow.line_width = 1
        super().__init__(arrow, text)

    def geometric_features(self):
        d = self._shapes["arrow"].geometric_features()
        d["text_position"] = self._shapes["text"].position
        return d
