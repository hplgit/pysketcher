import warnings
from copy import copy
from typing import Tuple

import numpy as np

from .curve import Curve
from .point import Point


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
        if start == end:
            raise ValueError("Cannot specify a line with two equal points.")
        self._start = start
        self._end = end
        self._a = self._b = self._c = self._d = None
        super().__init__([self._start, self._end])
        self._compute_formulas()

    def set_line_width(self, line_width: float) -> "Line":
        return self

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    def geometric_features(self):
        return {"start": self._start, "end": self._end}

    def interval(
        self, x_range: Tuple[float, float] = None, y_range: Tuple[float, float] = None
    ):
        """Return part of the line defined either by the x_range or the y_range"""
        if x_range is not None:
            return Line(
                Point(x_range[0], self(x_range[0])), Point(x_range[1], self(x_range[1]))
            )
        elif y_range is not None:
            return Line(
                Point(self(y_range[0]), y_range[0]), Point(self(y_range[1]), y_range[1])
            )

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

    def __call__(self, x=None, y=None):
        """Given x, return y on the line, or given y, return x."""
        self._compute_formulas()
        if x is not None and self._a is not None:
            return self._a * x + self._b
        elif y is not None and self._c is not None:
            return self._c * y + self._d
        else:
            raise ValueError("Line.__call__(x=%s, y=%s) not meaningful" % (x, y))

    def rotate(self, angle: float, center: Point) -> "Line":
        """
        Rotate all coordinates: `angle` is measured in radians
        center is the "origin" of the rotation.
        """
        print("rotating about %s" % center)
        start = self._start.rotate(angle, center)
        end = self._end.rotate(angle, center)
        line = Line(start, end)
        line.style = copy(self.style)
        return line
