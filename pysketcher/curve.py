from typing import List

import numpy as np

from pysketcher.angle import Angle
from pysketcher.point import Point
from pysketcher.shape import Shape


class Curve(Shape):
    """General curve as a sequence of (x,y) coordintes."""

    def __init__(self, points: List[Point]):
        """
        `x`, `y`: arrays holding the coordinates of the curve.
        """
        super().__init__()
        self._points = points
        # self.shapes must not be defined in this class
        # as self.shapes holds children objects:
        # Curve has no children (end leaf of self.shapes tree)

    @property
    def points(self):
        return self._points

    @property
    def xs(self):
        return np.array([p.x for p in self.points])

    @property
    def ys(self):
        return np.array([p.y for p in self.points])

    def rotate(self, angle: Angle, center: Point) -> "Curve":
        """
        Rotate all coordinates: `angle` is measured in radians
        center is the "origin" of the rotation.
        """
        return Curve([p.rotate(angle, center) for p in self.points])

    def scale(self, factor: np.float64) -> "Curve":
        """Scale all coordinates by `factor`: ``x = factor*x``, etc."""
        return Curve(Point.from_coordinate_lists(factor * self.xs, factor * self.ys))

    def translate(self, vec: Point) -> "Curve":
        """Translate all coordinates by a vector `vec`."""
        return Curve([p + vec for p in self.points])

    def __str__(self):
        """Compact pretty print of a Curve object."""
        s = "%d (x,y) coords" % len(self._points)
        s += " %s" % self.style
        return s

    def __repr__(self):
        return str(self)
