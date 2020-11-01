from typing import List

import numpy as np
from scipy.interpolate import UnivariateSpline

from pysketcher.curve import Curve
from pysketcher.point import Point


class Spline(Curve):

    _input_points: List[Point]
    _smooth: UnivariateSpline

    # Note: UnivariateSpline interpolation may not work if
    # the x[i] points are far from uniformly spaced
    def __init__(self, points: List[Point], degree: int = 3, resolution: int = 501):
        self._input_points = points
        self._smooth = UnivariateSpline(
            [p.x for p in points], [p.y for p in points], s=0, k=degree
        )
        x_coordinates = np.linspace(points[0].x, points[-1].x, resolution)
        y_coordinates = self._smooth(x_coordinates)
        smooth_points = [Point(p[0], p[1]) for p in zip(x_coordinates, y_coordinates)]
        super().__init__(smooth_points)

    def geometric_features(self):
        return {
            "start": self.points[0],
            "end": self.points[-1],
            "interval": [self.points[0].x, self.points[-1].x],
        }

    def __call__(self, x):
        return self._smooth(x)

    # Can easily find the derivative and the integral as
    # self.smooth.derivative(n=1) and self.smooth.antiderivative()
