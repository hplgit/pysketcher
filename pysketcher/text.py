from .matplotlibdraw import MatplotlibDraw
from .shape import Shape
from .point import Point


class Text(Shape):
    """
        Place `text` at the (x,y) point `position`, with the given
        fontsize (0 indicates that the default fontsize set in drawing_tool
        is to be used). The text is centered around `position` if `alignment` is
        'center'; if 'left', the text starts at `position`, and if
        'right', the right and of the text is located at `position`.
        """

    def __init__(self, text: str, position: Point, alignment='center', fontsize=0,
                 bgcolor=None, fgcolor=None, fontfamily=None, direction: Point = Point(1, 0)):
        """
                fontfamily can be (e.g.) 'serif' or 'monospace' (for code!).
                """
        super().__init__()
        self._text = text
        self._position = position
        self._alignment = alignment
        self._fontsize = fontsize
        self._bgcolor = bgcolor
        self._fgcolor = fgcolor
        self._fontfamily = fontfamily
        self._direction = direction

    def draw(self, drawing_tool: MatplotlibDraw, verbose=0):
        drawing_tool.text(
            self._text, self._position,
            self._alignment, self._fontsize,
            arrow_tip=None, bgcolor=self._bgcolor, fgcolor=self._fgcolor,
            direction=self._direction,
            fontfamily=self._fontfamily)
        if verbose > 0:
            print('drawing Text "%s"' % self._text)

    def rotate(self, angle: float, center: Point):
        direction = self._direction.rotate(angle, center)
        position = self._position.rotate(angle, center)
        return Text(self._text, position, self._alignment, self._fontsize,
                    self._bgcolor, self._fgcolor, self._fontfamily, direction)

    def __str__(self):
        return 'text "%s" at (%g,%g)' % (self._text, self._position.x, self._position.y)

    def __repr__(self):
        return repr(str(self))
