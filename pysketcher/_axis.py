from pysketcher._angle import Angle
from pysketcher._arrow import Arrow
from pysketcher._point import Point
from pysketcher.annotation import LineAnnotation
from pysketcher.composition import Composition


class Axis(Composition):
    """A representation of a axis.

    Draw axis from start with `length` to the right
    (x axis). Place label at the end of the arrow tip.
    Then return `rotation_angle` (in degrees).
    The `label_spacing` denotes the space between the label
    and the arrow tip as a fraction of the length of the plot
    in x direction. A tuple can be given to adjust the position
    in both the x and y directions (with one parameter, the
    x position is adjusted).

    Args:
        start: The start of the ``Axis``.
        length: The length of the ``Axis``.
        label: A text label for the ``Axis``.
        rotation_angle: The ``Angle``
    """

    def __init__(
        self,
        start: Point,
        length: float,
        label: str,
        rotation_angle: Angle = Angle(0.0),  # noqa: B008
    ):
        arrow = Arrow(start, start + Point(length, 0)).rotate(rotation_angle, start)
        # should increase spacing for downward pointing axis
        label = LineAnnotation(label, arrow)

        super().__init__({"arrow": arrow, "label": label})
