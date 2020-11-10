from pysketcher.angle import Angle
from pysketcher.point import Point
from pysketcher.shape import Shape
from pysketcher.style import Style, TextStyle


class Text(Shape):
    """
    Place `text` at the (x,y) point `position`, with the given
    fontsize (0 indicates that the default fontsize set in drawing_tool
    is to be used). The text is centered around `position` if `alignment` is
    'center'; if 'left', the text starts at `position`, and if
    'right', the right and of the text is located at `position`.
    """

    _style: TextStyle

    def __init__(self, text: str, position: Point, direction: Point = Point(1, 0)):
        super().__init__()
        self._text = text
        self._position = position
        self._direction = direction
        self._style = TextStyle()

    def rotate(self, angle: float, center: Point) -> "Text":
        direction = self._direction.rotate(angle, center)
        position = self._position.rotate(angle, center)
        return Text(self._text, position, direction)

    def __str__(self):
        return 'text "%s" at (%g,%g)' % (self._text, self._position.x, self._position.y)

    def __repr__(self):
        return repr(str(self))

    @property
    def style(self) -> TextStyle:
        return self._style

    @property
    def position(self) -> Point:
        return self._position

    @property
    def direction(self) -> Angle:
        return self._direction

    @property
    def text(self) -> str:
        return self._text

    @style.setter
    def style(self, text_style: TextStyle):
        self._style = text_style

    def set_alignment(self, alignment: TextStyle.Alignment) -> "Text":
        self.style.alignment = alignment
        return self

    def translate(self, vec: Point) -> "Text":
        new_text = Text(self.text, self.position, self.direction)
        new_text.style = self._style
        return new_text

    def scale(self, factor: float) -> "Text":
        raise NotImplementedError
