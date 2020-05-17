import numpy as np

from .spline import Spline
from .point import Point
from .text import Text


class SketchyFunc1(Spline):
    """
    A typical function curve used to illustrate an "arbitrary" function.
    """
    domain = [1, 6]

    def __init__(self, name=None, name_pos='start',
                 x_min=0, x_max=6, y_min=0, y_max=2):

        x = np.array([0, 2, 3, 4, 5, 6])
        y = np.array([1, 1.8, 1.2, 0.7, 0.8, 0.85])
        x = x_min - x.min() + x * (x_max - x_min) / (x.max() - x.min())
        y = y_min - y.min() + y * (y_max - y_min) / (y.max() - y.min())

        points = []
        for i in range(len(x) - 1):
            points += [Point(x[i], y[i])]

        super().__init__(points)
        self._shapes['smooth'].set_line_color('black')
        if name is not None:
            self._shapes['name'] = Text(name, self.geometric_features()[name_pos] + Point(0, 0.1))
