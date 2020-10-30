from typing import Callable

from pysketcher.arrow import Arrow
from pysketcher.composition.composition import Composition
from pysketcher.line import Line
from pysketcher.point import Point
from pysketcher.spline import Spline


class VelocityProfile(Composition):
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
            shapes["arrow%d" % i] = Arrow(start_position, end_position)

        shapes["smooth curve"] = Spline(end_points)
        super().__init__(shapes)
