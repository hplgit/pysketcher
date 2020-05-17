from .text import Text
from .point import Point
from .matplotlibdraw import MatplotlibDraw


class Text_wArrow(Text):
    """
    As class Text, but an arrow is drawn from the mid part of the text
    to some point `arrow_tip`.
    """

    def __init__(self, text: str, position: Point, arrow_tip: Point, alignment='center',
                 fontsize=0):
        super().__init__(text, position, alignment, fontsize)
        self.arrow_tip = arrow_tip

    def draw(self, drawing_tool: MatplotlibDraw, verbose=0):
        drawing_tool.text(
            self._text, self._position,
            self._alignment, self._fontsize,
            arrow_tip=self.arrow_tip,
            bgcolor=self._bgcolor, fgcolor=self._fgcolor,
            fontfamily=self._fontfamily)
        if verbose > 0:
            print('drawing Text_wArrow "%s"' % self._text)

    def __str__(self):
        return 'annotation "%s" at (%g,%g) with arrow to (%g,%g)' % \
               (self._text, self._position.x, self._position.y,
                self.arrow_tip.x, self.arrow_tip.y)

    def __repr__(self):
        return repr(str(self))
