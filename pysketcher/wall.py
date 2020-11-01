from typing import List

from pysketcher.curve import Curve
from pysketcher.point import Point
from pysketcher.style import Style


class Wall(Curve):
    _start: Point
    _end: Point
    _thickness: float

    def __init__(self, points: List[Point], thickness: float):
        self._start = points[0]
        self._end = points[-1]
        self._thickness = thickness

        def _displace(point: Point, point_before: Point, point_after: Point):
            # Displaces a point on our curve by thickness.
            # find a normal to the line between the point_before and the point_after
            # then displace by thickness from point in the direction of that normal
            return point + ((point_after - point_before).normal() * self._thickness)

        # at the start, there isn't a point_before, so use the start point
        new_points: List[Point] = [_displace(points[0], points[0], points[1])]

        for i in range(1, len(points) - 1):
            new_points += [_displace(points[i], points[i - 1], points[i + 1])]

        # and at the end there isn't a point_after, so use the end point
        new_points += [_displace(points[-1], points[-2], points[-1])]

        points = points + new_points[-1::-1]
        points += [self._start]

        super().__init__(points)
        self.style.fill_pattern = Style.FillPattern.CROSS

    def geometric_features(self):
        d = {"start": self._start, "end": self._end}
        return d
