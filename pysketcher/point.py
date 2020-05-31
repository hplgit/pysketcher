from typing import List, Tuple

import numpy as np


class Point:
    """
    Simple Point class which implements basic point arithmetic

    Parameters
    ----------
    x: float
        The x co-ordinate
    y: float
        The y co-ordinate
    """
    _x: float
    _y: float

    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self._x + other._x, self._y + other._y)

    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self._x - other._x, self._y - other._y)

    def __mul__(self, scalar: float) -> 'Point':
        return Point(self._x * scalar, self._y * scalar)

    def __abs__(self) -> float:
        return np.ma.sqrt(self.x ** 2 + self.y ** 2)

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y

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

    def unit_vector(self) -> 'Point':
        if abs(self) == 0:
            raise ZeroDivisionError("Length of Vector cannot be Zero")
        return self * (1 / (abs(self)))

    def angle(self) -> float:
        return np.arctan2(self.y, self.x)

    def radius(self) -> float:
        return abs(self)

    def normal(self) -> 'Point':
        uv = self.unit_vector()
        return Point(-uv.y, uv.x)

    def rotate(self, angle: float, center: 'Point') -> 'Point':
        """Rotate point an `angle` (in radians) around (`x`,`y`)."""
        c = np.cos(angle)
        s = np.sin(angle)
        return Point(center.x + (self.x - center.x) * c - (self.y - center.y) * s,
                     center.y + (self.x - center.x) * s + (self.y - center.y) * c)

    def scale(self, factor: float) -> 'Point':
        """Scale point coordinates by `factor`: ``x = factor*x``, etc."""
        return self * factor

    def translate(self, vec: 'Point') -> 'Point':
        """Translate point by a vector `vec`."""
        return self + vec

    @staticmethod
    def from_coordinate_lists(xs: List[float], ys: List[float]) -> List['Point']:
        if len(xs) != len(ys):
            raise ValueError("xs and ys must be the same length")
        return [Point(xs[i], ys[i]) for i in range(len(xs))]

    @staticmethod
    def to_coordinate_lists(ps: List['Point']) -> Tuple[List[float], List[float]]:
        xs = [p.x for p in ps]
        ys = [p.y for p in ps]
        return xs, ys

