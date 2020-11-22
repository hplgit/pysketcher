from typing import List

import numpy as np
from scipy.interpolate import UnivariateSpline

from pysketcher._curve import Curve
from pysketcher._point import Point


class Spline(Curve):
    """A univariate spline.

    Note: UnivariateSpline interpolation may not work if
        the x[i] points are far from uniformly spaced.

    Examples:
        >>> s = ps.Spline(
        ...     [
        ...         ps.Point(0, 0),
        ...         ps.Point(1, 1),
        ...         ps.Point(2, 4),
        ...         ps.Point(3, 9),
        ...         ps.Point(4, 16),
        ...     ]
        ... )
        >>> fig = ps.Figure(0, 5, 0, 16, backend=MatplotlibBackend)
        >>> fig.add(s)
        >>> fig.save("pysketcher/images/spline.png")

        .. figure:: images/spline.png
            :alt: An example of a Spline.
            :figclass: align-center
            :scale: 30%

            An example of ``Spline``.
    """

    _input_points: List[Point]
    _smooth: UnivariateSpline

    def __init__(self, points: List[Point], degree: int = 3, resolution: int = 501):
        self._input_points = points
        self._smooth = UnivariateSpline(
            [p.x for p in points], [p.y for p in points], s=0, k=degree
        )
        x_coordinates = np.linspace(points[0].x, points[-1].x, resolution)
        y_coordinates = self._smooth(x_coordinates)
        smooth_points = [Point(p[0], p[1]) for p in zip(x_coordinates, y_coordinates)]
        super().__init__(smooth_points)

    def __call__(self, x):
        """Returns the value of the curve at a given x-coordinate."""
        return self._smooth(x)
