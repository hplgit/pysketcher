from typing import List

from pysketcher._curve import Curve
from pysketcher._point import Point
from pysketcher._style import Style


class Wall(Curve):
    """A representation of a wall.

    Args:
        points: a ``List`` of ``Point`` through which the wall should pass.
        thickness: the thickness of the wall.

    Examples:
        >>> model = ps.Wall(
        ...     [
        ...         ps.Point(1, 1),
        ...         ps.Point(2, 2),
        ...         ps.Point(3, 2.5),
        ...         ps.Point(4, 2),
        ...         ps.Point(5, 1),
        ...     ],
        ...     0.1,
        ... )
        >>> fig = ps.Figure(0, 6, 0, 3, backend=MatplotlibBackend)
        >>> fig.add(model)
        >>> fig.save("pysketcher/images/wall.png")

        .. figure:: images/wall.png
            :alt: An example of a Wall.
            :figclass: align-center

            An example ``Wall``.
    """

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
