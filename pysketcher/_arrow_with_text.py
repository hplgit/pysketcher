from enum import auto, Enum, unique
from typing import Union

from pysketcher._arrow import Arrow
from pysketcher._point import Point
from pysketcher._text import Text
from pysketcher.composition import ShapeWithText


class ArrowWithText(ShapeWithText):
    """An ``Arrow`` with a text label at ``text_position``.

    Args:
        text: The text to be displayed.
        start: The start ``Point`` of the arrow.
        end: The end ``Point`` of the arrow.
        text_position: The position of the text on the arrow.
        spacing: The text spacing.

    Examples:
        >>> arrow_with_text = ps.ArrowWithText(
        ...     "$a$",
        ...     ps.Point(1.0, 1.0),
        ...     ps.Point(
        ...         3.0,
        ...         1.0,
        ...     ),
        ... )
        >>> fig = ps.Figure(0.0, 4.0, 0.0, 2.0, backend=MatplotlibBackend)
        >>> fig.add(arrow_with_text)
        >>> fig.save("pysketcher/images/arrow_with_text.png")

    .. figure:: images/arrow_with_text.png
        :alt: An example of ArrowWithText.
        :figclass: align-center

        An example of ``ArrowWithText``.
    """

    _DEFAULT_SPACING: Point = Point(0.15, 0.15)

    @unique
    class TextPosition(Enum):
        """Specifies the position of the text on the ``Arrow``."""

        START = auto()
        END = auto()

    def __init__(
        self,
        text: str,
        start: Point,
        end: Point,
        text_position: TextPosition = TextPosition.START,
        spacing: Union[float, Point] = None,
    ):

        spacing = spacing if spacing else self._DEFAULT_SPACING
        if not issubclass(spacing.__class__, Point):
            spacing = Point(spacing, spacing)

        if text_position == self.TextPosition.START:
            text = Text(text, start + spacing)
        if text_position == self.TextPosition.END:
            text = Text(text, end + spacing)

        arrow = Arrow(start, end)
        super().__init__(arrow, text)
