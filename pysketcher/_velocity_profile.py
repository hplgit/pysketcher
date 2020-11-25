import logging
from typing import Callable

from pysketcher._arrow import Arrow
from pysketcher._line import Line
from pysketcher._point import Point
from pysketcher._spline import Spline
from pysketcher.composition import Composition

logging.basicConfig(level=logging.DEBUG)


class VelocityProfile(Composition):
    """A representation of the profile of velocity in laminar flow.

    Args:
        start: the point from which the profile should start.
        height: the height of the profile.
        profile: a function which provides the value of the profile at a given point
        num_arrows: the number of arrows to display
        scaling: a scaling factor

    Examples:
        >>> def velocity_profile(y: float) -> ps.Point:
        ...     return ps.Point(y * (8 - y) / 4, 0)
        >>> pr = ps.VelocityProfile(ps.Point(0, 0), 4, velocity_profile, 5)
        >>> fig = ps.Figure(0, 4.1, 0, 4, backend=MatplotlibBackend)
        >>> fig.add(pr)
        >>> fig.save("pysketcher/images/velocity_profile.png")

        .. figure:: images/velocity_profile.png
            :alt: An example of a Velocity Profile.
            :figclass: align-center
            :scale: 50%

            An example of ``VelocityProfile``.
    """

    _start: Point
    _height: float
    _profile: Callable[[float], Point]
    _num_arrows: int
    _scaling: float

    def __init__(
        self,
        start: Point,
        height: float,
        profile: Callable[[float], Point],
        num_arrows: int,
        scaling: float = 1,
    ):

        self._start = start
        self._height = height
        self._profile = profile
        self._num_arrows = num_arrows
        self._scaling = scaling

        shapes = dict()

        # Draw left line
        shapes["start line"] = Line(self._start, (self._start + Point(0, self._height)))

        # Draw velocity arrows
        dy = float(self._height) / (self._num_arrows - 1)

        end_points = []

        for i in range(self._num_arrows):
            start_position = Point(start.x, start.y + i * dy)
            end_position = start_position + profile(start_position.y) * self._scaling
            end_points += [end_position]
            if start_position == end_position:
                continue
            shapes["arrow%d" % i] = Arrow(start_position, end_position)

        shapes["smooth curve"] = Spline(end_points)
        super().__init__(shapes)
