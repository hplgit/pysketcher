from enum import Enum, auto, unique
from typing import Tuple, Union

from pysketcher.arrow import Arrow
from pysketcher.composition import ShapeWithText
from pysketcher.point import Point
from pysketcher.text import Text


class ArrowWithText(ShapeWithText):
    """
    As class Text, but an arrow is drawn from the mid part of the text
    to some point `arrow_tip`.
    """

    _DEFAULT_SPACING: Point = Point(0.15, 0.15)

    @unique
    class TextPosition(Enum):
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
