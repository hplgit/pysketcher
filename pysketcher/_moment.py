from enum import auto, Enum, unique

import numpy as np

from pysketcher._angle import Angle
from pysketcher._arc import Arc
from pysketcher._style import Style
from pysketcher.annotation import ArcAnnotation
from pysketcher.composition import Composition


class Moment(Composition):
    r"""A symbol which represents a moment.

    This is an ``ArcWithText`` with the ``arc_angle`` fixed at :math:`\pi`.

    Args:
        text: The text to display.
        center: The centre of the moment.
        radius: The radius of the moment.
        start_angle: The angle from the +ve horizontal at which the moment should
            start.
        text_spacing: The spacing of the text.
        resolution: The number of points on the arc.

    Examples:
        >>> moment = ps.Moment("$M$", ps.Point(0, 0), 1.0)
        >>> fig = ps.Figure(-1.2, 1.2, -1.2, 1.2, backend=MatplotlibBackend)
        >>> fig.add(moment)
        >>> fig.save("pysketcher/images/moment.png")

        .. figure:: images/moment.png
            :alt: An example of Moment.
            :figclass: align-center

            An example of ``Moment``.
    """

    @unique
    class Direction(Enum):
        """Indicates the direction of the moment."""

        CLOCKWISE = auto()
        COUNTER_CLOCKWISE = auto()

    @unique
    class Orientation(Enum):
        """Indicated the orientation of the moment."""

        LEFT = auto()
        RIGHT = auto()

    _DEFAULT_DIRECTION: Direction = Direction.COUNTER_CLOCKWISE
    _DEFAULT_ORIENTATION: Orientation = Orientation.LEFT

    def __init__(
        self,
        text,
        center,
        radius,
    ):
        self._direction = self._DEFAULT_DIRECTION
        self._orientation = self._DEFAULT_ORIENTATION

        style = (
            Style.ArrowStyle.END
            if self._direction == self.Direction.COUNTER_CLOCKWISE
            else Style.ArrowStyle.START
        )

        start_angle = (
            np.pi / 2 if self._orientation == self.Orientation.LEFT else -np.pi / 2
        )

        self._arc = Arc(center, radius, start_angle, Angle(np.pi)).set_arrow(style)
        self._label = ArcAnnotation(text, self._arc)
        super().__init__({"arc": self._arc, "label": self._label})
