from enum import Enum, auto, unique

from .text import Text
from .arrow import Arrow
from .composition import ShapeWithText
from .point import Point


class ArrowWithText(ShapeWithText):
    """
    As class Text, but an arrow is drawn from the mid part of the text
    to some point `arrow_tip`.
    """

    _DEFAULT_SPACING: float = 0.15

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
        spacing: float = None,
        start_spacing: float = None,
        end_spacing: float = None,
    ):

        if spacing is not None:
            if start_spacing:
                raise ValueError("Cannot set spacing and start_spacing")
            if end_spacing:
                raise ValueError("Cannot set spacing and end_spacing")

        if text_position == self.TextPosition.START:
            text = Text(text, start)
        if text_position == self.TextPosition.END:
            text = Text(text, end)

        spacing = spacing if spacing else self._DEFAULT_SPACING
        if end_spacing is None:
            if text_position == self.TextPosition.END:
                end_spacing = spacing
            else:
                end_spacing = 0
        if start_spacing is None:
            if text_position == self.TextPosition.START:
                start_spacing = spacing
            else:
                start_spacing = 0

        arrow_start = start + (end - start) * start_spacing
        arrow_end = end - (end - start) * end_spacing
        arrow = Arrow(arrow_start, arrow_end)
        super().__init__(arrow, text)
