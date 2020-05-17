from typing import List

from .point import Point
from .shape import Shape
from .curve import Curve


class Wall(Shape):
    _start: Point
    _end: Point
    _thickness: float
    _points: List[Point]

    def __init__(self, points: List[Point], thickness: float, pattern='/'):
        super().__init__()
        self._points = points
        self._start = points[0]
        self._end = points[-1]
        self._thickness = thickness

        def _displace(point: Point, point_before: Point, point_after: Point):
            # Displaces a point on our curve by thickness.
            # find a normal to the line between the point_before and the point_after
            # then displace by thickness from point in the direction of that normal
            return point + ((point_after - point_before).normal() * self._thickness)

        # at the start, there isn't a point_before, so use the start point
        new_points: List[Point] = [_displace(self._points[0], self._points[0], self._points[1])]

        for i in range(1, len(self._points) - 1):
            new_points += [_displace(self._points[i], self._points[i - 1], self._points[i + 1])]

        # and at the end there isn't a point_after, so use the end point
        new_points += [_displace(self._points[-1], self._points[-2], self._points[-1])]

        self._points = self._points + new_points[-1::-1]
        self._points += [self._start]

        self._shapes['wall'] = Curve(self._points).set_fill_pattern(pattern)

    def geometric_features(self):
        d = {'start': self._start,
             'end': self._end}
        return d
