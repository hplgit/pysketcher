import logging
import warnings
from typing import List, Tuple

import numpy as np

from pysketcher.angle import Angle
from pysketcher.warning import LossOfPrecisionWarning


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

    def __mul__(self, scalar: np.float64) -> "Point":
        return Point(self.x * scalar, self.y * scalar)

    def __abs__(self) -> np.float64:
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
    def _isclose(x: np.float64, y: np.float64) -> bool:
        return np.isclose(x, y, atol=1e-4)

    @property
    def x(self) -> np.float64:
        return self._x

    @property
    def y(self) -> np.float64:
        return self._y

    def unit_vector(self) -> "Point":
        if self._isclose(abs(self), 0.0):
            raise ZeroDivisionError("Length of Vector cannot be Zero")
        return self * (1 / (abs(self)))

    def angle(self) -> Angle:
        """

        Returns:
            object:
        """
        logging.debug(abs(self))
        if abs(self.x) <= 1e-160 or abs(self.y) <= 1e-160 or abs(self) < 1e-160:
            warnings.warn(
                "Vert short components will lead to loss of precision.",
                category=LossOfPrecisionWarning,
            )

        if abs(self) == 0:
            return np.nan

        # check for simple degenerate cases:
        if self.x == 0.0:
            if self.y > 0.0:
                return Angle(np.pi / 2)
            else:
                return Angle(-np.pi / 2)
        if self.y == 0.0:
            if self.x > 0.0:
                return Angle(0.0)
            else:
                return Angle(np.pi)

        if abs(self.x / self.y) >= 1e5 or abs(self.y / self.x) >= 1e5:
            warnings.warn(
                "Variation in magnitude of more that 1e6 causes loss of precision.",
                LossOfPrecisionWarning,
            )

        # determine quadrant
        if self.x > 0:
            if self.y > 0:
                quadrant = 0
            else:  # b < 0
                quadrant = -1
        else:  # a < 0
            if self.y > 0:
                quadrant = 1
            else:  # b > 0:
                quadrant = -2

        a = abs(self)
        b = abs(self.x)
        c = abs(self.y)

        u = c - (a - b) if b >= c else b - (a - c)

        angle = 2 * np.arctan(
            np.sqrt((((a - b) + c) * u) / ((a + (b + c)) * ((a - c) + b)))
        )

        if quadrant == 0:
            return Angle(angle)
        elif quadrant == 1:
            return Angle(np.pi - angle)
        elif quadrant == -1:
            return Angle(-angle)
        else:
            return Angle(-np.pi + angle)

    def radius(self) -> np.float64:
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
            return self
        if angle == Angle(np.pi / 2):
            return Point(center.x - self.y + center.y, center.y + self.x - center.x)
        if angle == Angle(np.pi):
            return Point(2 * center.x - self.x, 2 * center.y - self.y)
        if angle == Angle(-np.pi / 2):
            return Point(center.x + self.y - center.y, center.y - self.x + center.x)
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
