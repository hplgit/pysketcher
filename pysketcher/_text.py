from pysketcher._angle import Angle
from pysketcher._point import Point
from pysketcher._shape import Shape
from pysketcher._style import TextStyle


class Text(Shape):
    """Some text which appears on the drawing at the specified location.

    Place `text` at the (x,y) point `position`, with the given
    fontsize (0 indicates that the default fontsize set in drawing_tool
    is to be used). The text is centered around `position` if `alignment` is
    'center'; if 'left', the text starts at `position`, and if
    'right', the right and of the text is located at `position`.

    Args:
        text: The text to be displayed.
        position: The position at which the text should be displayed.
        direction: The direction in which the text should flow.

    Examples:
        >>> fig = ps.Figure(0.0, 4.0, 0.0, 4.0, MatplotlibBackend)
        >>> code = ps.Text("This is some left text!", Point(2, 1))
        >>> code.style.alignment = ps.TextStyle.Alignment.LEFT
        >>> code.style.line_color = ps.TextStyle.Color.BLUE
        >>> code.style.font_family = ps.TextStyle.FontFamily.SERIF
        >>> code1 = ps.Text("This is some right text!", Point(2, 2))
        >>> code1.style.alignment = ps.TextStyle.Alignment.RIGHT
        >>> code1.style.line_color = ps.TextStyle.Color.GREEN
        >>> code1.style.font_family = ps.TextStyle.FontFamily.SANS
        >>> code2 = ps.Text("This is some center text!", Point(2, 3))
        >>> code2.style.alignment = ps.TextStyle.Alignment.CENTER
        >>> code2.style.line_color = ps.TextStyle.Color.RED
        >>> code2.style.font_family = ps.TextStyle.FontFamily.MONO
        >>> fig.add(code)
        >>> fig.add(code1)
        >>> fig.add(code2)
        >>> fig.save("pysketcher/images/text.png")

        .. figure:: images/text.png
            :alt: An example of some text.
            :figclass: align-center

            An example of some ``Text``.
    """

    _style: TextStyle

    def __init__(
        self, text: str, position: Point, direction: Point = Point(1, 0)  # noqa: B008
    ):
        super().__init__()
        self._text = text
        self._position = position
        self._direction = direction
        self._style = TextStyle()

    def rotate(self, angle: float, center: Point) -> "Text":
        """Returns the text rotated through ``angle`` radians about ``centre``."""
        direction = self._direction.rotate(angle, center)
        position = self._position.rotate(angle, center)
        return Text(self._text, position, direction)

    def __str__(self):
        """Provides a string which describes the Text object."""
        return 'text "%s" at (%g,%g)' % (self._text, self._position.x, self._position.y)

    def __repr__(self):
        """Provides a string which describes the Text object."""
        return repr(str(self))

    @property
    def style(self) -> TextStyle:
        """Returns the style of the object so that the style can be altered."""
        return self._style

    @style.setter
    def style(self, text_style: TextStyle):
        self._style = text_style

    @property
    def position(self) -> Point:
        """The ``Point`` at which the text is located."""
        return self._position

    @property
    def direction(self) -> Angle:
        """The direction in which the text flows."""
        return self._direction

    @property
    def text(self) -> str:
        """The text."""
        return self._text

    def set_alignment(self, alignment: TextStyle.Alignment) -> "Text":
        """Sets the alignment of the text.

        Args:
            alignment: The new alignment of the text.

        Returns:
            The original text object with the style modified to the new alignment.
        """
        self.style.alignment = alignment
        return self

    def translate(self, vec: Point) -> "Text":
        """Translates the text through ``vec``."""
        new_text = Text(self.text, self.position, self.direction)
        new_text.style = self._style
        return new_text

    def scale(self, factor: float) -> "Text":
        """Scales the text by a factor of `factor`."""
        raise NotImplementedError
