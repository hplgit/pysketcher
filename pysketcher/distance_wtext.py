from .point import Point
from .text_warrow import Text
from .composition import Composition
from .arrow import DoubleArrow
from .text_warrow import Text_wArrow


class Distance_wText(Composition):
    """
    Arrow <-> with text (usually a symbol) at the midpoint, used for
    identifying a some distance in a figure.  The text is placed
    slightly to the right of vertical-like arrows, with text displaced
    `text_spacing` times to total distance in x direction of the plot
    area. The text is by default aligned 'left' in this case. For
    horizontal-like arrows, the text is placed the same distance
    above, but aligned 'center' by default (when `alignment` is None).
    """

    def __init__(self, start: Point, end: Point, text: str, fontsize=0,
                 text_spacing=1 / 6., alignment=None, text_pos='mid'):
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

        if text_pos == 'mid':
            mid = (start + end) * 0.5  # midpoint of start-end line
            text_point = mid + normal * text_spacing
        elif text_pos == 'start':
            text_point = start + normal * text_spacing
        elif text_pos == 'end':
            text_point = end + normal * text_spacing
        else:
            raise ValueError("text_pos should be 'mid', 'start', or 'end'")

        text = Text(text, text_point, fontsize=fontsize, alignment=alignment)

        arrow = DoubleArrow(start, end)
        arrow.line_color = 'black'
        arrow.line_width = 1
        super().__init__({'arrow': arrow, 'text': text})

    def geometric_features(self):
        d = self._shapes['arrow'].geometric_features()
        d['text_position'] = self._shapes['text'].position
        return d
