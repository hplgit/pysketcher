from .arrow import Arrow
from .point import Point
from .text import Text


class Force(Arrow):
    """
    Indication of a force by an arrow and a text (symbol).  Draw an
    arrow, starting at `start` and with the tip at `end`.  The symbol
    is placed at `text_pos`, which can be 'start', 'end' or the
    coordinates of a point.
    """

    def __init__(self, start: Point, end: Point, text: str, fontsize: float = 0, text_pos: str = 'start',
                 text_alignment: str = 'center', text_spacing: float = 1 / 6.):
        super().__init__(start, end)

        # Two cases: label at bottom of line or top, need more
        # spacing if bottom
        downward = (end - start).y < 0
        upward = not downward  # for easy code reading

        if text_pos == 'start':
            spacing_dir: Point = (self._start - self._end).unit_vector()
            if upward:
                text_spacing *= 1.7
            text_position = start + spacing_dir * text_spacing
        elif text_pos == 'end':
            spacing_dir = (self._end - self._start).unit_vector()
            if downward:
                text_spacing *= 1.7
            text_position = end + spacing_dir * text_spacing
        else:
            raise ValueError("%s is not a valid value for text_pos" % text_pos)
        self._shapes['text'] = Text(text, text_position, fontsize=fontsize,
                                   alignment=text_alignment)

    def geometric_features(self):
        d = super().geometric_features()
        d['symbol_location'] = self._shapes['text'].position
        return d


class Gravity(Force):
    """Downward-pointing gravity arrow with the symbol g."""

    def __init__(self, start, length, text='$g$', fontsize=0):
        Force.__init__(self, start, start + Point(0, -length),
                       text, text_spacing=1. / 60,
                       fontsize=0, text_pos='end')
        self.line_color = 'black'
