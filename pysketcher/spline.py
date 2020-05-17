from typing import List

import numpy as np

from scipy.interpolate import UnivariateSpline

from .shape import Shape
from .curve import Curve
from .point import Point
from .matplotlibdraw import MatplotlibDraw


class Spline(Shape):

    _points: List[Point]
    _smooth: UnivariateSpline

    # Note: UnivariateSpline interpolation may not work if
    # the x[i] points are far from uniformly spaced
    def __init__(self, points: List[Point], degree: int = 3, resolution: int = 501):
        super().__init__()
        self._points = points
        self._smooth = UnivariateSpline([p.x for p in points], [p.y for p in points], s=0, k=degree)
        x_coordinates = np.linspace(points[0].x, points[-1].x, resolution)
        y_coordinates = self._smooth(x_coordinates)
        smooth_points = [Point(p[0], p[1]) for p in zip(x_coordinates, y_coordinates)]
        self._shapes = {'smooth': Curve(smooth_points)}

    def geometric_features(self):
        s = self._shapes['smooth']
        return {'start': s.points[0],
                'end': s.points[-1],
                'interval': [s.points[0].x, s.points[-1].x]}

    def __call__(self, x):
        return self._smooth(x)

    # Can easily find the derivative and the integral as
    # self.smooth.derivative(n=1) and self.smooth.antiderivative()
