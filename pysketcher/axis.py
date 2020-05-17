from .composition import Composition
from .arrow import Arrow
from .point import Point
from .text import Text


class Axis(Composition):
    def __init__(self, start: Point, length: float, label: str, rotation_angle=0, fontsize=0, label_spacing=1. / 4.5):
        """
        Draw axis from start with `length` to the right
        (x axis). Place label at the end of the arrow tip.
        Then return `rotation_angle` (in degrees).
        The `label_spacing` denotes the space between the label
        and the arrow tip as a fraction of the length of the plot
        in x direction. A tuple can be given to adjust the position
        in both the x and y directions (with one parameter, the
        x position is adjusted).
        With `label_alignment` one can place
        the axis label text such that the arrow tip is to the 'left',
        'right', or 'center' with respect to the text field.
        The `label_spacing` and `label_alignment`parameters can
        be used to fine-tune the location of the label.
        """
        arrow = Arrow(start, start + Point(length, 0)).rotate(rotation_angle, start)
        # should increase spacing for downward pointing axis
        label_pos = Point(start.x + length + label_spacing, start.y)
        label = Text(label, position=label_pos, fontsize=fontsize).rotate(rotation_angle, start)
        shapes = {'arrow': arrow, 'label': label}
        super().__init__(shapes)

    def geometric_features(self):
        return self._shapes['arrow'].geometric_features()
