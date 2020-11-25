import math
from typing import Callable, List, Tuple

import numpy as np

from pysketcher._curve import Curve
from pysketcher._point import Point


class CubicBezier(Curve):
    """A cubic bezier curve implementation.

    Examples:
        >>> s = ps.CubicBezier(
        ...     ps.Point(0, 0), [(ps.Point(1, 1), ps.Point(2.5, 0.5), ps.Point(2, 2.5))]
        ... )
        >>> fig = ps.Figure(-0.5, 3.0, -0.5, 3.0, backend=MatplotlibBackend)
        >>> fig.add(s)
        >>> fig.save("pysketcher/images/cubic_bezier.png")

        .. figure:: images/cubic_bezier.png
            :alt: An example of a CubicBezier.
            :figclass: align-center

            An example of ``CubicBezier``.
    """

    _input_points: List[Tuple[Point, Point, Point, Point]]
    _segments: List[Callable[[float], Point]]
    _points: List[Point]

    def __init__(
        self,
        start: Point,
        points: List[Tuple[Point, Point, Point]],
        resolution: int = 50,
    ):
        start_point = start
        self._input_points = []
        self._segments = []
        for pts in points:
            self._input_points.append((start_point,) + pts)
            self._segments.append(self._segment(start_point, pts[0], pts[1], pts[2]))
            start_point = pts[2]

        ts = np.linspace(0, len(self._segments), resolution, endpoint=False)
        self._points = [self.__call__(t) for t in ts]
        last_point = points[len(points) - 1][2]
        self._points.append(last_point)
        super().__init__(self._points)

    @staticmethod
    def _segment(
        p0: Point, p1: Point, p2: Point, p3: Point
    ) -> Callable[[float], Point]:
        def _bernstein_cubic(a: List[float], t: float) -> float:
            return (
                (1 - t) ** 3 * a[0]
                + (1 - t) ** 2 * 3 * t * a[1]
                + (1 - t) * 3 * t ** 2 * a[2]
                + t ** 3 * a[3]
            )

        def _segment_function(t: float) -> Point:
            x = _bernstein_cubic([p0.x, p1.x, p2.x, p3.x], t)
            y = _bernstein_cubic([p0.y, p1.y, p2.y, p3.y], t)
            return Point(x, y)

        return _segment_function

    @property
    def start(self) -> Point:
        """The first point of the curve."""
        return self._points[0]

    @property
    def end(self) -> Point:
        """The last point of the curve."""
        return self._points[-1]

    def __call__(self, t: float) -> Point:
        """Given a parameter, ``t``, returns the point on the curve."""
        t, index = math.modf(t)
        if index > len(self._segments) or t < 0:
            raise ValueError(
                (
                    f"Value of t is only valid > 0  and < {len(self._segments)} "
                    f"got {t}."
                )
            )
        return self._segments[int(index)](t)
        pass
