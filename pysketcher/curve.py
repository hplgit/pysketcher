import numpy as np
import logging
from typing import List

from .shape import Shape
from .point import Point
from .matplotlibdraw import MatplotlibDraw


class Curve(Shape):
    """General curve as a sequence of (x,y) coordintes."""

    def __init__(self, points: List[Point]):
        """
        `x`, `y`: arrays holding the coordinates of the curve.
        """
        super().__init__()
        self._points = points
        # self.shapes must not be defined in this class
        # as self.shapes holds children objects:
        # Curve has no children (end leaf of self.shapes tree)

    @property
    def points(self):
        return self._points

    @property
    def xs(self):
        return np.array([p.x for p in self.points])

    @property
    def ys(self):
        return np.array([p.y for p in self.points])

    def draw(self, drawing_tool: MatplotlibDraw, verbose=0):
        """
        Send the curve to the plotting engine. That is, convert
        coordinate information in self.x and self.y, together
        with optional settings of linestyles, etc., to
        plotting commands for the chosen engine.
        """
        if drawing_tool.inside_plot_area(self._points):
            raise ValueError("Curve falls outside of plot area.")
        logging.info("Given %i points, line_style: %s, line_width: %s "
                     "line_color: %s, arrow: %s, fill_color: %s, fill_pattern: %s, shadow: %s",
                     len(self._points), self.line_style, self.line_width, self.line_color, self.arrow, self.fill_color,
                     self.fill_pattern, self.shadow)
        drawing_tool.plot_curve(
            self._points,
            self.line_style, self.line_width, self.line_color,
            self.arrow, self.fill_color, self.fill_pattern,
            self.shadow)
        if verbose:
            print('drawing Curve object with %d points' % len(self._points))

    def rotate(self, angle: float, center: Point) -> 'Curve':
        """
        Rotate all coordinates: `angle` is measured in radians
        center is the "origin" of the rotation.
        """
        print("rotating about %s" % center)
        angle = np.radians(angle)
        x, y = center.x, center.y
        c = np.cos(angle)
        s = np.sin(angle)
        return Curve(Point.from_coordinate_lists(x + (self.xs - x) * c - (self.ys - y) * s,
                     y + (self.xs - x) * s + (self.ys - y) * c))

    def scale(self, factor: float) -> 'Curve':
        """Scale all coordinates by `factor`: ``x = factor*x``, etc."""
        return Curve(Point.from_coordinate_lists(factor * self.xs, factor * self.ys))

    def translate(self, vec) -> 'Curve':
        """Translate all coordinates by a vector `vec`."""
        self.x += vec[0]
        self.y += vec[1]
        return self

    def deform(self, displacement_function):
        """Displace all coordinates according to displacement_function(x,y)."""
        for i in range(len(self.x)):
            self.x[i], self.y[i] = displacement_function(self.x[i], self.y[i])
        return self

    def minmax_coordinates(self, minmax=None):
        if minmax is None:
            minmax = {'xmin': [], 'xmax': [], 'ymin': [], 'ymax': []}
        minmax['xmin'] = min(self.x.min(), minmax['xmin'])
        minmax['xmax'] = max(self.x.max(), minmax['xmax'])
        minmax['ymin'] = min(self.y.min(), minmax['ymin'])
        minmax['ymax'] = max(self.y.max(), minmax['ymax'])
        return minmax

    def recurse(self, name, indent=0):
        space = ' ' * indent
        print(space, 'reached "bottom" object %s' % \
              self.__class__.__name__)

    def _object_couplings(self, parent, couplings=[], classname=True):
        return

    def show_hierarchy(self, indent=0, format='std'):
        if format == 'dict':
            return '"%s"' % str(self)
        elif format == 'plain':
            return ''
        else:
            return str(self)

    def __str__(self):
        """Compact pretty print of a Curve object."""
        s = '%d (x,y) coords' % self.x.size
        props = ('line_color', 'line_width', 'line_style', 'arrow', 'shadow',
                 'fill_color', 'fill_pattern')
        for prop in props:
            value = getattr(self, prop)
            if value is not None:
                s += ' %s=%s' % (prop, repr(value))
        return s

    def __repr__(self):
        return str(self)

    def __getitem__(self, item):
        raise NotImplementedError("Curves cannot contain sub-shapes")

    def __setitem__(self, name, value):
        raise NotImplementedError("Curves cannot contain sub-shapes")
