import numpy as np

from pysketcher.curve import Curve
from pysketcher.point import Point
from pysketcher.spline import Spline
from pysketcher.style import Style


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

        xs = scale_array(x_min, x_max, x)
        ys = scale_array(y_min, y_max, y)
        points = Point.from_coordinate_lists(xs, ys)

        super().__init__(points)


class SketchyFunc2(Curve):
    """
    A typical function curve used to illustrate an "arbitrary" function.
    """

    domain = [0, 2.25]

    def __init__(self, x_min=0, x_max=2.25, y_min=0.046679703125, y_max=1.259375):
        a = 0
        b = 2.25
        resolution = 100
        xs = np.linspace(a, b, resolution + 1)
        ys = self(xs)
        # Scale x and y
        xs = x_min - xs.min() + xs * (x_max - x_min) / (xs.max() - xs.min())
        ys = y_min - ys.min() + ys * (y_max - y_min) / (ys.max() - ys.min())
        points = Point.from_coordinate_lists(xs, ys)

        super().__init__(points)

    def __call__(self, x):
        return 0.5 + x * (2 - x) * (0.9 - x)  # on [0, 2.25]


class SketchyFunc3(Spline):
    """
    A typical function curve used to illustrate an "arbitrary" function.
    """

    domain = [0, 6]

    def __init__(self, x_min=0, x_max=6, y_min=0.5, y_max=3.8):
        xs = np.array([0, 2, 3, 4, 5, 6])
        ys = np.array([0.5, 3.5, 3.8, 2, 2.5, 3.5])
        # Scale x and y
        xs = x_min - xs.min() + xs * (x_max - x_min) / (xs.max() - xs.min())
        ys = y_min - ys.min() + ys * (y_max - y_min) / (ys.max() - ys.min())
        points = Point.from_coordinate_lists(xs, ys)

        super().__init__(points)
        self.style.line_color = Style.Color.BLACK


# class SketchyFunc4(Spline):
#     """
#     A typical function curve used to illustrate an "arbitrary" function.
#     Can be a companion function to SketchyFunc3.
#     """
#     domain = [1, 6]
#
#     def __init__(self, name=None, name_pos='start',
#                  xmin=0, xmax=6, ymin=0.5, ymax=1.8):
#         x = array([0, 2, 3, 4, 5, 6])
#         y = array([1.5, 1.3, 0.7, 0.5, 0.6, 0.8])
#         # Scale x and y
#         x = xmin - x.min() + x * (xmax - xmin) / (x.max() - x.min())
#         y = ymin - y.min() + y * (ymax - ymin) / (y.max() - y.min())
#
#         Spline.__init__(self, x, y)
#         self.shapes['smooth'].set_linecolor('black')
#         if name is not None:
#             self.shapes['name'] = Text(name, self.geometric_features()[name_pos] + point(0, 0.1))
# 1
