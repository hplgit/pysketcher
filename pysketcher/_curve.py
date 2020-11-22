from typing import List

import numpy as np

from pysketcher._angle import Angle
from pysketcher._point import Point
from pysketcher._shape import Shape


class Curve(Shape):
    """General curve as a sequence of (x,y) coordintes.

    Examples:
        >>> code = ps.Curve(
        ...     [
        ...         ps.Point(0, 0),
        ...         ps.Point(1, 1),
        ...         ps.Point(2, 4),
        ...         ps.Point(3, 9),
        ...         ps.Point(4, 16),
        ...     ]
        ... )
        >>> code.style.line_color = ps.Style.Color.BLACK
        >>> model = ps.Composition(dict(text=code))
        >>> fig = ps.Figure(0, 5, 0, 16, backend=MatplotlibBackend)
        >>> fig.add(model)
        >>> fig.save("pysketcher/images/curve.png")


    .. figure:: images/curve.png
        :alt: An example of Curve.
        :figclass: align-center
        :scale: 30%

        An example of ``Curve``.
    """

    def __init__(self, points: List[Point]):
        super().__init__()
        self._points = points
        # self.shapes must not be defined in this class
        # as self.shapes holds children objects:
        # Curve has no children (end leaf of self.shapes tree)

    @property
    def points(self):
        """The points which make up the curve."""
        return self._points

    @property
    def xs(self):
        """The x co-ordinates of the points of the curve."""
        return np.array([p.x for p in self.points])

    @property
    def ys(self):
        """The y co-ordinates of the Points of the curve."""
        return np.array([p.y for p in self.points])

    def rotate(self, angle: Angle, center: Point) -> "Curve":
        """Rotate all coordinates.

        Args:
            angle: The ``Angle`` (in radians) through which the rotation should be
                performed.
            center: The ``Point`` about which the rotation should be performed.

        Returns:
            A copy of the ``Curve`` which has had all points rotated in the
                described manner.
        """
        ret_curve = Curve([p.rotate(angle, center) for p in self.points])
        ret_curve.style = self.style
        return ret_curve

    def scale(self, factor: float) -> "Curve":
        """Scale all coordinates by `factor`: ``x = factor*x``, etc."""
        ret_curve = Curve(
            Point.from_coordinate_lists(factor * self.xs, factor * self.ys)
        )
        ret_curve.style = self.style
        return ret_curve

    def translate(self, vec: Point) -> "Curve":
        """Translate all coordinates by a vector `vec`."""
        ret_curve = Curve([p + vec for p in self.points])
        ret_curve.style = self.style
        return ret_curve

    def __str__(self):
        """Compact pretty print of a Curve object."""
        s = "%d (x,y) coords" % len(self._points)
        return s

    def __repr__(self):
        """An unambiguous string representational of a Curve object."""
        return "Curve(" + ",".join([repr(p) for p in self.points]) + ")"
