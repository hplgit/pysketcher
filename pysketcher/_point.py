from typing import List, Tuple

import numpy as np

from pysketcher._angle import Angle


class Point:
    """Immutable Point class which implements basic point arithmetic.

    Args:
        x: float
            The x co-ordinate
        y: float
            The y co-ordinate
    """

    _x: float
    _y: float

    def __init__(self, x: float, y: float):
        self._x = float(x)
        self._y = float(y)

    def __add__(self, other: "Point") -> "Point":
        """Sums the co-ordinates of the two points.

        Args:
            other: the point to add to ``self``.

        Returns:
            The sum of ``self`` and ``other``.
        """
        return Point(self.x + other._x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        """Subtracts the co-ordinates of the two points.

        Args:
            other: the point to subtract from ``self``.

        Returns:
            The difference between ``self`` and ``other``.
        """
        return Point(self.x - other._x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Point":
        """Multiplies ``self`` by ``scalar``.

        Args:
            scalar: the factor to scale ``self`` by.

        Returns:
            A point with each co-ordinate scaled from ``self`` by ``scalar``.
        """
        return Point(self.x * scalar, self.y * scalar)

    def __abs__(self) -> float:
        """The pythagorean length of ``self``.

        Returns:
            The cartesian distance from ``Point(0,0)`` to ``self``.
        """
        return np.hypot(self.x, self.y)

    def __eq__(self, other: "Point") -> bool:
        """Implementation of point equality.

        Note that owing to the vagaries of floating point arithmetic
        two points which have co-ordinates within 1e-4 will be
        considered equal.

        Args:
            other: the ``Point`` to compare to ``self``.

        Returns:
            True if ``Point`` is equal to ``self``.
        """
        return self._is_close(self.x, other.x) and self._is_close(self.y, other.y)

    def __str__(self):
        """A string representation of ``self``."""
        return self.__repr__()

    def __repr__(self):
        """An unambiguous string representation of ``self``."""
        return "P(%s, %s)" % (
            np.format_float_scientific(self.x),
            np.format_float_scientific(self.y),
        )

    @staticmethod
    def _is_close(x: float, y: float) -> bool:
        return np.isclose(x, y, atol=1e-4)

    @property
    def x(self) -> float:
        """The x co-ordinate of the Point."""
        return self._x

    @property
    def y(self) -> float:
        """The y co-ordinate of the Point."""
        return self._y

    # TODO: These should all be properties
    def unit_vector(self) -> "Point":
        """Returns a ``Point`` of length 1 in the direction of the ``Point``."""
        if self._is_close(abs(self), 0.0):
            raise ZeroDivisionError("Length of Vector cannot be Zero")
        return self * (1 / (abs(self)))

    def angle(self) -> Angle:
        """Returns the ``Angle`` the ``Point`` makes to the +ve horizontal."""
        angle = Angle(np.arctan2(self.y, self.x))
        return angle

    def radius(self) -> float:
        """Returns the distance from ``Point(0.,0.)`` to this point."""
        return abs(self)

    def normal(self) -> "Point":
        r"""Returns a ``Point`` of length 1, :math:``$\frac{\pi}{2}$`` from ``self``."""
        uv = self.unit_vector()
        return Point(-uv.y, uv.x)

    def rotate(self, angle: Angle, center: "Point") -> "Point":
        """Returns a ``Point``, ``angle`` (in radians) around (`x`,`y`).

        Args:
            angle: The angle through which the rotation should be made.
            center: The point about which the rotation should be made.

        Returns:
            The rotated point.
        """
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
        """Scale point coordinates by `factor`: ``x = factor*x``, etc.

        Args:
            factor: the amount the ``Point`` should be scaled by.

        Returns:
            The scaled point.
        """
        return self * factor

    def translate(self, vec: "Point") -> "Point":
        """Translate point by a vector `vec`.

        Args:
            vec: The vector (``Point``) through which the point should be
                translated.

        Returns:
            The translated vector.
        """
        return self + vec

    @staticmethod
    def from_coordinate_lists(xs: List[float], ys: List[float]) -> List["Point"]:
        """Generates points from lists of co-ordinates.

        Args:
            xs: the x co-ordinates
            ys: the y co-ordinates

        Returns:
            A list of ``Point`` made up of the respective co-ordinates.

        Raises:
            ValueError: When the co-ordinates lists are of different lengths.
        """
        if len(xs) != len(ys):
            raise ValueError("xs and ys must be the same length")
        return [Point(xs[i], ys[i]) for i in range(len(xs))]

    @staticmethod
    def to_coordinate_lists(ps: List["Point"]) -> Tuple[List[float], List[float]]:
        """Generates lists of co-ordinates from points."""
        xs = [p.x for p in ps]
        ys = [p.y for p in ps]
        return xs, ys
