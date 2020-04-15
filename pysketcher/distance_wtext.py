from .matplotlibdraw import MatplotlibDraw
from .point import Point
from .shape import Shape
from .text_warrow import Text
from .arrow import DoubleArrow
from .text_warrow import Text_wArrow


class Distance_wText(Shape):
    """
    Arrow <-> with text (usually a symbol) at the midpoint, used for
    identifying a some distance in a figure.  The text is placed
    slightly to the right of vertical-like arrows, with text displaced
    `text_spacing` times to total distance in x direction of the plot
    area. The text is by default aligned 'left' in this case. For
    horizontal-like arrows, the text is placed the same distance
    above, but aligned 'center' by default (when `alignment` is None).
    """

    def __init__(self, start: Point, end: Point, text: str, drawing_tool: MatplotlibDraw, fontsize=0,
                 text_spacing=1 / 60., alignment=None, text_pos='mid'):
        super().__init__(drawing_tool)
        self._start = start
        self._end = end

        # Decide first if we have a vertical or horizontal arrow
        vertical = abs(end.x - start.x) < 2 * abs(end.y - start.y)

        if vertical:
            # Assume end above start
            if end.y < start.y:
                start, end = end, start
            if alignment is None:
                alignment = 'left'
        else:  # horizontal arrow
            # Assume start to the right of end
            if start.x < end.x:
                start, end = end, start
            if alignment is None:
                alignment = 'center'

        tangent = end - start
        # Tangent goes always to the left and upward
        normal = Point(tangent.y, -tangent.x).unit_vector()
        mid = (start + end) * 0.5  # midpoint of start-end line

        if text_pos == 'mid':
            text_pos = mid + normal * self._drawing_tool.x_range * text_spacing
            text = Text(text, text_pos, self._drawing_tool, fontsize=fontsize,
                        alignment=alignment)
        else:
            text = Text_wArrow(text, text_pos, mid, alignment='left',
                               fontsize=fontsize)
        arrow = DoubleArrow(start, end, self._drawing_tool)
        arrow.set_linecolor('black')
        arrow.set_linewidth(1)
        self._shapes = {'arrow': arrow, 'text': text}

    def geometric_features(self):
        d = self._shapes['arrow'].geometric_features()
        d['text_position'] = self._shapes['text'].position
        return d
