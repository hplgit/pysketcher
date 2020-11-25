from enum import auto, Enum

from pysketcher._arrow import DoubleArrow
from pysketcher._arrow_with_text import Text
from pysketcher._point import Point
from pysketcher.composition import ShapeWithText


class DistanceWithText(ShapeWithText):
    """Arrow <-> with text (usually a symbol) at the midpoint.

    Used for identifying a some distance in a figure.  The text is placed
    slightly to the right of vertical-like arrows, with text displaced
    `text_spacing` times to total distance in x direction of the plot
    area. The text is by default aligned 'left' in this case. For
    horizontal-like arrows, the text is placed the same distance
    above, but aligned 'center' by default (when `alignment` is None).

    Args:
        text: The text which will be displayed.
        start: The start of the arrow.
        end: The end of the arrow.
        spacing: The spacing of the text from the arrow position.
        text_position: The position of the text.

    Raises:
        ValueError: when invalid `text_position` is passed.

    Examples:
        >>> distance_with_text = ps.DistanceWithText(
        ...     "$a$", ps.Point(1.0, 1.0), ps.Point(3.0, 1.0)
        ... )
        >>> fig = ps.Figure(0.0, 4.0, 0.0, 2.0, backend=MatplotlibBackend)
        >>> fig.add(distance_with_text)
        >>> fig.save("pysketcher/images/distance_with_text.png")

        .. figure:: images/distance_with_text.png
            :alt: An example of DistanceWithText.
            :figclass: align-center

            An example of ``DistanceWithText``.
    """

    class TextPosition(Enum):
        """Used to show that text should be at the start, end, or middle of an arrow."""

        START = auto()
        MIDDLE = auto()
        END = auto()

        def swap(self) -> "DistanceWithText.TextPosition":
            """Swaps the relative position of text."""
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
        spacing: float = 1 / 6.0,
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
