import numpy as np

from .matplotlibdraw import MatplotlibDraw
from .shape import Shape
from .point import Point
from .curve import Curve


class Arc(Shape):
    def __init__(self, center: Point, radius: float, start_angle: float, arc_angle: float, drawing_tool: MatplotlibDraw,
                 resolution: int = 180):
        # Must record some parameters for __call__
        super().__init__(drawing_tool)
        self._center = center
        self._radius = radius
        self._resolution = resolution
        self._start_angle = start_angle
        self._arc_angle = arc_angle

        ts = np.linspace(self._start_angle,
                         self._start_angle + self._arc_angle,
                         resolution + 1)

        self._points = \
            [Point(center.x + radius * np.cos(t), center.y + radius * np.sin(t)) for t in ts]
        self._shapes = {'circle': Curve(self._points, self._drawing_tool)}

        # Cannot set dimensions (Arc_wText recurses into this
        # constructor forever). Set in test_Arc instead.

    def geometric_features(self):
        m = self._resolution // 2  # mid point in array
        return {'start': self._points[0],
                'end': self._points[-1],
                'mid': self._points[m]}

    def __call__(self, theta):
        """
        Return (x,y) point at start_angle + theta.
        Not valid after translation, rotation, or scaling.
        """
        if self._start_angle + theta > self._arc_angle:
            raise ValueError("Theta is outside the bounds of the arc")

        return Point(self._center.x + self._radius * np.cos(self._start_angle + theta),
                     self._center.x + self._radius * np.sin(self._start_angle + theta))
