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
        return np.ma.sqrt(self._x ** 2 + self._y ** 2)

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def unit_vector(self) -> 'Point':
        return self * (1 / (abs(self)))

    def rotate(self, angle, center) -> 'Point':
        """Rotate point an `angle` (in radians) around (`x`,`y`)."""
        x, y = center
        c = cos(angle);
        s = sin(angle)
        return Point(x + (self._x - x) * c - (self._y - y) * s,
              y + (self._x - x) * s + (self._y - y) * c)

    def scale(self, factor: float) -> 'Point':
        """Scale point coordinates by `factor`: ``x = factor*x``, etc."""
        return self * factor

    def translate(self, vec: 'Point') -> 'Point':
        """Translate point by a vector `vec`."""
        return self + vec

    def show_hierarchy(self, indent=0, format='std'):
        s = '%s at (%g,%g)' % (self.__class__.__name__, self._x, self._y)
        if format == 'dict':
            return '"%s"' % s
        elif format == 'plain':
            return ''
        else:
            return s
