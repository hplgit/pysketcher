from pysketcher._line import Line
from pysketcher._point import Point
from pysketcher._style import TextStyle
from pysketcher._text import Text
from pysketcher.annotation._text_position import TextPosition


class LineAnnotation(Text):
    """Annotates a line with the provided text."""

    # TODO: Write a LineAnnotation Example
    _DEFAULT_SPACING: Point = Point(0.15, 0.15)

    def __init__(
        self, text: str, line: Line, text_position: TextPosition = TextPosition.MIDDLE
    ):

        spacing = self._DEFAULT_SPACING

        if text_position == TextPosition.START:
            position = line.start + spacing
            alignment = TextStyle.Alignment.LEFT
        elif text_position == TextPosition.END:
            position = line.end + spacing
            alignment = TextStyle.Alignment.RIGHT
        elif text_position == TextPosition.MIDDLE:
            position = line.start + (line.end - line.start) * 0.5 + spacing
            alignment = TextStyle.Alignment.CENTER
        else:
            raise RuntimeError(f"Invalid value of text_position: {text_position}.")

        super().__init__(text, position)
        self.style.alignment = alignment
