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

    def __init__(self, text: str, position: Point, drawing_tool: MatplotlibDraw, alignment='center', fontsize=0,
                 bgcolor=None, fgcolor=None, fontfamily=None):
        """
                fontfamily can be (e.g.) 'serif' or 'monospace' (for code!).
                """
        super().__init__(drawing_tool)
        self._text = text
        self._position = position
        self._alignment = alignment
        self._fontsize = fontsize
        self._bgcolor = bgcolor
        self._fgcolor = fgcolor
        self._fontfamily = fontfamily

    def draw(self, verbose=0):
        self._drawing_tool.text(
            self._text, self._position,
            self._alignment, self._fontsize,
            arrow_tip=None, bgcolor=self._bgcolor, fgcolor=self._fgcolor,
            fontfamily=self._fontfamily)
        if verbose > 0:
            print('drawing Text "%s"' % self._text)

    def __str__(self):
        return 'text "%s" at (%g,%g)' % (self._text, self._position.x, self._position.y)

    def __repr__(self):
        return repr(str(self))
