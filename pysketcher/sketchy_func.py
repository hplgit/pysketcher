import numpy as np

from .spline import Spline
from .point import Point
from .text import Text


class SketchyFunc1(Spline):
    """
    A typical function curve used to illustrate an "arbitrary" function.
    """

    domain = [1, 6]

    def __init__(self, name=None, name_pos="start", x_min=0, x_max=6, y_min=0, y_max=2):

        x = np.array([0, 2, 3, 4, 5, 6])
        y = np.array([1, 1.8, 1.2, 0.7, 0.8, 0.85])

        def scale_array(min: float, max: float, ps: np.array):
            return min - ps.min() + ps * (max - min) / (ps.max() - ps.min())

        x = scale_array(x_min, x_max, x)
        y = scale_array(y_min, y_max, y)

        points = []
        for i in range(len(x) - 1):
            points += [Point(x[i], y[i])]

        super().__init__(points)
