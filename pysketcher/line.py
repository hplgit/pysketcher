from .matplotlibdraw import MatplotlibDraw
from .shape import Shape
from .point import Point
from .curve import Curve


class Line(Shape):
    _start: Point
    _end: Point

    def __init__(self, start: Point, end: Point, drawing_tool: MatplotlibDraw, arrow=None):
        super().__init__(drawing_tool)
        self._start = start
        self._end = end
        self._arrow = arrow
        self._shapes = {'line': Curve([self._start, self._end], drawing_tool)}
        self['line'].set_arrow(self._arrow)
        self._a = self._b = self._c = self._d = None
        self._compute_formulas()

    def geometric_features(self):
        return {'start': self._start,
                'end': self._end}

    def _compute_formulas(self):
        # Define equations for line:
        # y = a*x + b,  x = c*y + d
        try:
            self._a = (self._end.y - self._start.y) / (self._end.x - self._start.x)
            self._b = self._start.y - self._a * self._start.x
        except ZeroDivisionError:
            # Vertical line, y is not a function of x
            self._a = None
            self._b = None
        try:
            if self._a is None:
                self._c = 0
            else:
                self._c = 1 / float(self._a)
            if self._b is None:
                self._d = self._end.x
        except ZeroDivisionError:
            # Horizontal line, x is not a function of y
            self._c = None
            self._d = None

    def __call__(self, x=None, y=None):
        """Given x, return y on the line, or given y, return x."""
        self.compute_formulas()
        if x is not None and self._a is not None:
            return self._a * x + self._b
        elif y is not None and self._c is not None:
            return self._c * y + self._d
        else:
            raise ValueError('Line.__call__(x=%s, y=%s) not meaningful' % (x, y))
