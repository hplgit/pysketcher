from math import isclose
from typing import List, Tuple

import numpy as np


class Point:
    """
    Simple Point class which implements basic point arithmetic.
    """

    _x: np.float64
    _y: np.float64

    def __init__(self, x: np.float64, y: np.float64):
        """
        Parameters
        ---------
        x: float
            The x co-ordinate
        y: float
            The y co-ordinate
        """
        self._x = np.float64(x)
        self._y = np.float64(y)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other._x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other._x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Point":
        return Point(self.x * scalar, self.y * scalar)

    def __abs__(self) -> np.float64:
        return np.ma.sqrt(self.x * self.x + self.y * self.y)

    def __eq__(self, other):
        return np.isclose(self.x, other.x) and isclose(self.y, other.y)

    def __str__(self):
        return "(%f, %f)" % (self.x, self.y)

    def __repr__(self):
        return "(%f, %f)" % (self.x, self.y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def unit_vector(self) -> "Point":
        if abs(self) == 0:
            raise ZeroDivisionError("Length of Vector cannot be Zero")
        return self * (1 / (abs(self)))

    def angle(self) -> np.float64:
        return np.arctan2(self.y, self.x)

    def radius(self) -> np.float64:
        return abs(self)

    def normal(self) -> "Point":
        uv = self.unit_vector()
        return Point(-uv.y, uv.x)

    def rotate(self, angle: np.float64, center: "Point") -> "Point":
        """Rotate point an `angle` (in radians) around (`x`,`y`)."""
        c = np.cos(angle)
        s = np.sin(angle)
        return Point(
            center.x + (self.x - center.x) * c - (self.y - center.y) * s,
            center.y + (self.x - center.x) * s + (self.y - center.y) * c,
        )

    def scale(self, factor: np.float64) -> "Point":
        """Scale point coordinates by `factor`: ``x = factor*x``, etc."""
        return self * factor

    def translate(self, vec: "Point") -> "Point":
        """Translate point by a vector `vec`."""
        return self + vec

    @staticmethod
    def from_coordinate_lists(
        xs: List[np.float64], ys: List[np.float64]
    ) -> List["Point"]:
        if len(xs) != len(ys):
            raise ValueError("xs and ys must be the same length")
        return [Point(xs[i], ys[i]) for i in range(len(xs))]

    @staticmethod
    def to_coordinate_lists(
        ps: List["Point"]
    ) -> Tuple[List[np.float64], List[np.float64]]:
        xs = [p.x for p in ps]
        ys = [p.y for p in ps]
        return xs, ys
