from typing import List, Tuple

import numpy as np

from pysketcher.angle import Angle


class Point:
    """
    Simple Point class which implements basic point arithmetic.
    """

    _x: float
    _y: float

    def __init__(self, x: float, y: float):
        """
        Parameters
        ---------
        x: float
            The x co-ordinate
        y: float
            The y co-ordinate
        """
        self._x = float(x)
        self._y = float(y)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other._x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other._x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Point":
        return Point(self.x * scalar, self.y * scalar)

    def __abs__(self) -> float:
        return np.hypot(self.x, self.y)

    def __eq__(self, other: "Point") -> bool:
        return self._isclose(self.x, other.x) and self._isclose(self.y, other.y)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "P(%s, %s)" % (
            np.format_float_scientific(self.x),
            np.format_float_scientific(self.y),
        )

    @staticmethod
    def _isclose(x: float, y: float) -> bool:
        return np.isclose(x, y, atol=1e-4)

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    def unit_vector(self) -> "Point":
        if self._isclose(abs(self), 0.0):
            raise ZeroDivisionError("Length of Vector cannot be Zero")
        return self * (1 / (abs(self)))

    def angle(self) -> Angle:
        angle = Angle(np.arctan2(self.y, self.x))
        return angle

    def radius(self) -> float:
        return abs(self)

    def normal(self) -> "Point":
        uv = self.unit_vector()
        return Point(-uv.y, uv.x)

    def rotate(self, angle: Angle, center: "Point") -> "Point":
        """Rotate point an `angle` (in radians) around (`x`,`y`)."""

        if not type(angle) == Angle:
            angle = Angle(angle)

        # Check for a few degenerate cases:
        if angle == Angle(0.0):
            p = self
        elif angle == Angle(np.pi / 2):
            p = Point(center.x - self.y + center.y, center.y + self.x - center.x)
        elif angle == Angle(np.pi):
            p = Point(2 * center.x - self.x, 2 * center.y - self.y)
        elif angle == Angle(-np.pi / 2):
            p = Point(center.x + self.y - center.y, center.y - self.x + center.x)
        else:
            c = np.cos(angle)
            s = np.sin(angle)
            p = Point(
                center.x + (self.x - center.x) * c - (self.y - center.y) * s,
                center.y + (self.x - center.x) * s + (self.y - center.y) * c,
            )
        return p

    def scale(self, factor: float) -> "Point":
        """Scale point coordinates by `factor`: ``x = factor*x``, etc."""
        return self * factor

    def translate(self, vec: "Point") -> "Point":
        """Translate point by a vector `vec`."""
        return self + vec

    @staticmethod
    def from_coordinate_lists(xs: List[float], ys: List[float]) -> List["Point"]:
        if len(xs) != len(ys):
            raise ValueError("xs and ys must be the same length")
        return [Point(xs[i], ys[i]) for i in range(len(xs))]

    @staticmethod
    def to_coordinate_lists(ps: List["Point"]) -> Tuple[List[float], List[float]]:
        xs = [p.x for p in ps]
        ys = [p.y for p in ps]
        return xs, ys
