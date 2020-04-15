import numpy as np
from typing import List

from .shape import Shape
from .point import Point
from .matplotlibdraw import MatplotlibDraw


class Curve(Shape):
    """General curve as a sequence of (x,y) coordintes."""

    _points: List[Point]
    _drawing_tool: MatplotlibDraw

    def __init__(self, points: List[Point], drawing_tool: MatplotlibDraw):
        """
        `x`, `y`: arrays holding the coordinates of the curve.
        """
        super().__init__(drawing_tool)
        self._points = points
        # self.shapes must not be defined in this class
        # as self.shapes holds children objects:
        # Curve has no children (end leaf of self.shapes tree)

        self._drawing_tool = drawing_tool
        self.linestyle = None
        self.linewidth = None
        self.linecolor = None
        self.fillcolor = None
        self.fillpattern = None
        self.arrow = None
        self.shadow = False

    def inside_plot_area(self, verbose=True):
        """Check that all coordinates are within drawing_tool's area."""
        for point in self._points:
            if not self._drawing_tool.inside(point):
                return False
        return True

    def draw(self, verbose=0):
        """
        Send the curve to the plotting engine. That is, convert
        coordinate information in self.x and self.y, together
        with optional settings of linestyles, etc., to
        plotting commands for the chosen engine.
        """
        self.inside_plot_area()
        self._drawing_tool.plot_curve(
            self._points,
            self.linestyle, self.linewidth, self.linecolor,
            self.arrow, self.fillcolor, self.fillpattern,
            self.shadow)
        if verbose:
            print('drawing Curve object with %d points' % len(self.x))

    def rotate(self, angle, center):
        """
        Rotate all coordinates: `angle` is measured in degrees and
        (`x`,`y`) is the "origin" of the rotation.
        """
        angle = np.radians(angle)
        x, y = center
        c = np.cos(angle);
        s = np.sin(angle)
        xnew = x + (self.x - x) * c - (self.y - y) * s
        ynew = y + (self.x - x) * s + (self.y - y) * c
        self.x = xnew
        self.y = ynew
        return self

    def scale(self, factor):
        """Scale all coordinates by `factor`: ``x = factor*x``, etc."""
        self.x = factor * self.x
        self.y = factor * self.y
        return self

    def translate(self, vec):
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

    def set_linecolor(self, color):
        self.linecolor = color
        return self

    def set_linewidth(self, width):
        self.linewidth = width
        return self

    def set_linestyle(self, style):
        self.linestyle = style
        return self

    def set_arrow(self, style=None):
        self.arrow = style
        return self

    def set_filled_curves(self, color='', pattern=''):
        self.fillcolor = color
        self.fillpattern = pattern
        return self

    def set_shadow(self, pixel_displacement=3):
        self.shadow = pixel_displacement
        return self

    def show_hierarchy(self, indent=0, format='std'):
        if format == 'dict':
            return '"%s"' % str(self)
        elif format == 'plain':
            return ''
        else:
            return str(self)

    @property
    def points(self):
        return _points

    def __str__(self):
        """Compact pretty print of a Curve object."""
        s = '%d (x,y) coords' % self.x.size
        inside = self.inside_plot_area(verbose=False)
        if inside is None:
            pass  # no info about the plotting area
        elif not inside:
            s += ', some coordinates are outside plotting area!\n'
        props = ('linecolor', 'linewidth', 'linestyle', 'arrow',
                 'fillcolor', 'fillpattern')
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
