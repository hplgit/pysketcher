import warnings
from copy import copy
from typing import Tuple

import numpy as np

from pysketcher.curve import Curve
from pysketcher.point import Point


class Line(Curve):

    _start: Point
    _end: Point
    _a: np.float64
    _b: np.float64
    _c: np.float64
    _d: np.float64
    _vertical: bool
    _horizontal: bool

    def __init__(self, start: Point, end: Point):
        """ A representation of a line primitive.

        Args:
            start: The starting point of the line.
            end: The end point of the line.

        Example:
            >>> a = Line(Point(1.,2.), Point(4.,3.))
            >>> b = a.rotate(np.pi / 2, Point(1.,2.))
        """
        if start == end:
            raise ValueError("Cannot specify a line with two equal points.")
        self._start = start
        self._end = end
        self._horizontal = False
        self._vertical = False
        self._a = self._b = self._c = self._d = None
        super().__init__([self._start, self._end])
        self._compute_formulas()

    def _compute_formulas(self):
        # Define equations for line:
        # y = a*x + b,  x = c*y + d
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore", "divide by zero encountered in double_scalars"
            )
            warnings.filterwarnings(
                "ignore", "invalid value encountered in double_scalars"
            )
            warnings.filterwarnings("ignore", "overflow encountered in double_scalars")
            self._a = (self._end.y - self._start.y) / (self._end.x - self._start.x)
            self._b = self._start.y - self._a * self._start.x
            if np.isnan(self._a) or np.isinf(self._a):
                # Vertical line, y is not a function of x
                self._vertical = True
                self._c = 0.0
                self._d = self._end.x
            else:
                self._c = 1.0 / self._a
                self._d = self._b / self._a
                if np.isnan(self._c) or np.isinf(self._c):
                    self._horizontal = True

    @property
    def start(self):
        """The starting point of the line."""
        return self._start

    @property
    def end(self):
        """The end point of the line."""
        return self._end

    def __call__(self, x: np.float64 = None, y: np.float64 = None):
        """Given x, return y on the line, or given y, return x.

        Args:
            x: the value of x for which a value of y should be calculated
            y: the value of y for which a value of x should be calculated

        Returns:
            the appropriate value of either y or x.

        Raises:
            ValueError: If the line is horizontal and y is provided, or if
            the line is vertical and x is provided.
        """
        self._compute_formulas()
        if self._horizontal and y:
            raise ValueError("Value of x is not dependent on the value of y.")
        if self._vertical and x:
            raise ValueError("Value of y is not dependent on the value of x.")
        return self._a * x + self._b if x else self._c * y + self._d

    def interval(
        self,
        x_range: Tuple[np.float64, np.float64] = None,
        y_range: Tuple[np.float64, np.float64] = None,
    ):
        """Returns a smaller portion of a line.

        Args:
            x_range: The range of x-coordinates which should be used to obtain the segment
            y_range: The range of y-coordinates which should be used to obtain the segment

        """
        if x_range and y_range:
            raise ValueError("Cannot specify both x_range and y_range.")
        if x_range is not None:
            return Line(
                Point(x_range[0], self(x_range[0])), Point(x_range[1], self(x_range[1]))
            )
        elif y_range is not None:
            return Line(
                Point(self(y_range[0]), y_range[0]), Point(self(y_range[1]), y_range[1])
            )

    def rotate(self, angle: np.float64, center: Point) -> "Line":
        """Returns a copy of a line rotated through an angle about a point.

        Args:
            angle:
            center:
        """
        start = self._start.rotate(angle, center)
        end = self._end.rotate(angle, center)
        line = Line(start, end)
        line.style = copy(self.style)
        return line
