import numpy as np

from pysketcher._curve import Curve
from pysketcher._point import Point
from pysketcher._spline import Spline
from pysketcher._style import Style


def _scale_array(min: float, max: float, ps: np.array):
    return min - ps.min() + ps * (max - min) / (ps.max() - ps.min())


class SketchyFunc1(Spline):
    """A typical function curve used to illustrate an "arbitrary" function.

    Examples:
        >>> f = ps.SketchyFunc1()
        >>> fig = ps.Figure(0.0, 7.0, 0.0, 3.0, backend=MatplotlibBackend)
        >>> fig.add(f)
        >>> fig.save("pysketcher/images/sketchyfunc1.png")

        .. figure:: images/sketchyfunc1.png
            :alt: An example of an SketchyFunc1.
            :figclass: align-center

            An example of ``SketchyFunc1``.
    """

    domain = [1, 6]

    def __init__(self, name=None, name_pos="start", x_min=0, x_max=6, y_min=0, y_max=2):
        xs = np.array([0.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        ys = np.array([1, 1.8, 1.2, 0.7, 0.8, 0.85])

        xs = _scale_array(x_min, x_max, xs)
        ys = _scale_array(y_min, y_max, ys)
        points = Point.from_coordinate_lists(xs, ys)

        super().__init__(points)


class SketchyFunc2(Curve):
    """A typical function curve used to illustrate an "arbitrary" function.

    Examples:
        >>> f = ps.SketchyFunc2()
        >>> fig = ps.Figure(0.0, 3.0, 0.0, 1.5, backend=MatplotlibBackend)
        >>> fig.add(f)
        >>> fig.save("pysketcher/images/sketchyfunc2.png")

        .. figure:: images/sketchyfunc2.png
            :alt: An example of an SketchyFunc1.
            :figclass: align-center

            An example of ``SketchyFunc2``.
    """

    domain = [0, 2.25]

    def __init__(self, x_min=0, x_max=2.25, y_min=0.046679703125, y_max=1.259375):
        a = 0
        b = 2.25
        resolution = 100
        xs = np.linspace(a, b, resolution + 1)
        ys = self.__call__(xs)
        # Scale x and y
        xs = _scale_array(x_min, x_max, xs)
        ys = _scale_array(y_min, y_max, ys)
        points = Point.from_coordinate_lists(xs, ys)

        super().__init__(points)

    def __call__(self, x):
        """Returns the value of the function at a given :math:`x`."""
        return 0.5 + x * (2 - x) * (0.9 - x)  # on [0, 2.25]


class SketchyFunc3(Spline):
    """A typical function curve used to illustrate an "arbitrary" function.

    Examples:
        >>> f = ps.SketchyFunc3()
        >>> fig = ps.Figure(0.0, 7.0, 0.0, 4.5, backend=MatplotlibBackend)
        >>> fig.add(f)
        >>> fig.save("pysketcher/images/sketchyfunc3.png")

        .. figure:: images/sketchyfunc3.png
            :alt: An example of an SketchyFunc3.
            :figclass: align-center

            An example of ``SketchyFunc3``.
    """

    domain = [0, 6]

    def __init__(self, x_min=0, x_max=6, y_min=0.5, y_max=3.8):
        xs = np.array([0.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        ys = np.array([0.5, 3.5, 3.8, 2, 2.5, 3.5])

        # Scale x and y
        xs = _scale_array(x_min, x_max, xs)
        ys = _scale_array(y_min, y_max, ys)
        points = Point.from_coordinate_lists(xs, ys)

        super().__init__(points)
        self.style.line_color = Style.Color.BLACK


class SketchyFunc4(Spline):
    """A typical function curve used to illustrate an "arbitrary" function.

    Can be a companion function to SketchyFunc3.

    Examples:
        >>> f = ps.SketchyFunc4()
        >>> fig = ps.Figure(0.0, 7.0, 0.0, 3.0, backend=MatplotlibBackend)
        >>> fig.add(f)
        >>> fig.save("pysketcher/images/sketchyfunc4.png")

        .. figure:: images/sketchyfunc4.png
            :alt: An example of an SketchyFunc4.
            :figclass: align-center

            An example of ``SketchyFunc4``.
    """

    domain = [1, 6]

    def __init__(self, name_pos="start", x_min=0, x_max=6, y_min=0.5, y_max=1.8):
        xs = np.array([0, 2, 3, 4, 5, 6])
        ys = np.array([1.5, 1.3, 0.7, 0.5, 0.6, 0.8])
        # Scale x and y
        xs = _scale_array(x_min, x_max, xs)
        ys = _scale_array(y_min, y_max, ys)
        points = Point.from_coordinate_lists(xs, ys)

        super().__init__(points)
