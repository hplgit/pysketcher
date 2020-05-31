from .text import Text
from .arrow import Arrow
from .composition import ShapeWithText
from .point import Point


class ArrowWithText(ShapeWithText):
    """
    As class Text, but an arrow is drawn from the mid part of the text
    to some point `arrow_tip`.
    """

    _DEFAULT_SPACING: float = 0.1

    def __init__(self, text: str, position: Point, arrow_tip: Point, spacing: float = None,
                 start_spacing: float = None, end_spacing: float = None):
        text = Text(text, position)

        if spacing is not None:
            if start_spacing:
                raise ValueError("Cannot set spacing and start_spacing")
            if end_spacing:
                raise ValueError("Cannot set spacing and end_spacing")
            start_spacing = end_spacing = spacing

        if end_spacing is None:
            end_spacing = self._DEFAULT_SPACING
        if start_spacing is None:
            start_spacing = self._DEFAULT_SPACING

        arrow_start = position + (arrow_tip - position) * start_spacing
        arrow_end = arrow_tip - (arrow_tip - position) * end_spacing
        arrow = Arrow(arrow_start, arrow_end)
        super().__init__(arrow, text)
        self._arrow_tip = arrow_tip

