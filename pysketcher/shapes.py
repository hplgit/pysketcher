from numpy import linspace, sin, cos, pi, array, asarray, ndarray, sqrt, abs
import pprint, copy, glob, os

from MatplotlibDraw import MatplotlibDraw
drawing_tool = MatplotlibDraw()

def point(x, y, check_inside=False):
    if isinstance(x, (float,int)) and isinstance(y, (float,int)):
        pass
    else:
        raise TypeError('x=%s,y=%s must be float,float, not %s,%s' %
                        (x, y, type(x), type(y)))
    if check_inside:
        ok, msg = drawing_tool.inside((x,y), exception=True)
        if not ok:
            print msg

    return array((x, y), dtype=float)

def arr2D(x, check_inside=False):
    if isinstance(x, (tuple,list,ndarray)):
        if len(x) == 2:
            pass
        else:
            raise ValueError('x=%s has length %d, not 2' % (x, len(x)))
    else:
        raise TypeError('x=%s must be list/tuple/ndarray, not %s' %
                        (x, type(x)))
    if check_inside:
        ok, msg = drawing_tool.inside(x, exception=True)
        if not ok:
            print msg

    return asarray(x, dtype=float)

def _is_sequence(seq, length=None,
                 can_be_None=False, error_message=True):
    if can_be_None:
        legal_types = (list,tuple,ndarray,None)
    else:
        legal_types = (list,tuple,ndarray)

    if isinstance(seq, legal_types):
        if length is not None:
            if length == len(seq):
                return True
            elif error_message:
                raise TypeError('%s is %s; must be %s of length %d' %
                            (str(seq), type(seq),
                            ', '.join([str(t) for t in legal_types]),
                             len(seq)))
            else:
                return False
        else:
            return True
    elif error_message:
        raise TypeError('%s is %s; must be %s' %
                        (str(seq), type(seq),
                        ','.join([str(t)[5:-1] for t in legal_types])))
    else:
        return False

def is_sequence(*sequences, **kwargs):
    length = kwargs.get('length', 2)
    can_be_None = kwargs.get('can_be_None', False)
    error_message = kwargs.get('error_message', True)
    check_inside = kwargs.get('check_inside', False)
    for x in sequences:
        _is_sequence(x, length=length, can_be_None=can_be_None,
                     error_message=error_message)
        if check_inside:
            ok, msg = drawing_tool.inside(x, exception=True)
            if not ok:
                print msg


def animate(fig, time_points, user_action, moviefiles=False,
            pause_per_frame=0.5):
    if moviefiles:
        # Clean up old frame files
        framefilestem = 'tmp_frame_'
        framefiles = glob.glob('%s*.png' % framefilestem)
        for framefile in framefiles:
            os.remove(framefile)

    for n, t in enumerate(time_points):
        drawing_tool.erase()

        user_action(t, fig)
        #could demand returning fig, but in-place modifications
        #are done anyway
        #fig = user_action(t, fig)
        #if fig is None:
        #    raise TypeError(
        #        'animate: user_action returns None, not fig\n'
        #        '(a Shape object with the whole figure)')

        fig.draw()
        drawing_tool.display()

        if moviefiles:
            drawing_tool.savefig('%s%04d.png' % (framefilestem, n))

    if moviefiles:
        return '%s*.png' % framefilestem


class Shape:
    """
    Superclass for drawing different geometric shapes.
    Subclasses define shapes, but drawing, rotation, translation,
    etc. are done in generic functions in this superclass.
    """
    def __init__(self):
        """
        Until new version of shapes.py is ready:
        Never to be called from subclasses.
        """
        raise NotImplementedError(
            'class %s must implement __init__,\nwhich defines '
            'self.shapes as a list of Shape objects\n'
            '(and preferably self._repr string).\n'
            'Do not call Shape.__init__!' % \
            self.__class__.__name__)

    def __iter__(self):
        # We iterate over self.shapes many places, and will
        # get here if self.shapes is just a Shape object and
        # not the assumed list.
        print 'Warning: class %s does not define self.shapes\n'\
              'as a *list* of Shape objects'
        return [self]  # Make the iteration work

    def copy(self):
        return copy.deepcopy(self)

    def __getitem__(self, name):
        """
        Allow indexing like::

           obj1['name1']['name2']

        all the way down to ``Curve`` or ``Point`` (``Text``)
        objects.
        """
        if hasattr(self, 'shapes'):
            if name in self.shapes:
                return self.shapes[name]
            else:
                for shape in self.shapes:
                    if isinstance(self.shapes[shape], (Curve,Point)):
                        # Indexing of Curve/Point/Text is not possible
                        raise TypeError(
                            'Index "%s" (%s) is illegal' %
                            (name, self.__class__.__name__))
                    return self.shapes[shape][name]
        else:
            raise Exception('This is a bug')


    def _for_all_shapes(self, func, *args, **kwargs):
        if not hasattr(self, 'shapes'):
            # When self.shapes is lacking, we either come to
            # a special implementation of func or we come here
            # because Shape.func is just inherited. This is
            # an error if the class is not Curve or Point
            if isinstance(self, (Curve, Point)):
                return  # ok: no shapes and no func
            else:
                raise AttributeError('class %s has no shapes attribute!' %
                                     self.__class__.__name__)

        is_dict = True if isinstance(self.shapes, dict) else False
        for shape in self.shapes:
            if is_dict:
                shape = self.shapes[shape]
            if not isinstance(shape, Shape):
                if isinstance(shape, dict):
                    raise TypeError(
                        'class %s has a shapes attribute that is just\n'
                        'a plain dictionary,\n%s\n'
                        'Did you mean to embed this dict in a Compose\n'
                        'object?' % (self.__class__.__name__,
                        str(shape)))
                elif isinstance(shape, (list,tuple)):
                    raise TypeError(
                        'class %s has a shapes attribute containing\n'
                        'a %s object %s,\n'
                        'Did you mean to embed this list in a Compose\n'
                        'object?' % (self.__class__.__name__,
                        type(shape), str(shape)))
                else:
                    raise TypeError(
                        'class %s has a shapes attribute %s which is not'
                        'a Shape objects\n%s' %
                        (self.__class__.__name__, type(shape),
                         pprint.pformat(self.shapes)))

            getattr(shape, func)(*args, **kwargs)

    def draw(self):
        self._for_all_shapes('draw')
        return self

    def draw_dimensions(self):
        if hasattr(self, 'dimensions'):
            for shape in self.dimensions:
                self.dimensions[shape].draw()
            return self
        else:
            #raise AttributeError('no self.dimensions dict for defining dimensions of class %s' % self.__classname__.__name__)
            return self

    def rotate(self, angle, center):
        is_sequence(center, length=2)
        self._for_all_shapes('rotate', angle, center)
        return self

    def translate(self, vec):
        is_sequence(vec, length=2)
        self._for_all_shapes('translate', vec)
        return self

    def scale(self, factor):
        self._for_all_shapes('scale', factor)
        return self

    def set_linestyle(self, style):
        styles = ('solid', 'dashed', 'dashdot', 'dotted')
        if style not in styles:
            raise ValueError('%s: style=%s must be in %s' %
                             (self.__class__.__name__ + '.set_linestyle:',
                              style, str(styles)))
        self._for_all_shapes('set_linestyle', style)
        return self

    def set_linewidth(self, width):
        if not isinstance(width, int) and width >= 0:
            raise ValueError('%s: width=%s must be positive integer' %
                             (self.__class__.__name__ + '.set_linewidth:',
                              width))
        self._for_all_shapes('set_linewidth', width)
        return self

    def set_linecolor(self, color):
        if color in drawing_tool.line_colors:
            color = drawing_tool.line_colors[color]
        elif color in drawing_tool.line_colors.values():
            pass # color is ok
        else:
            raise ValueError('%s: invalid color "%s", must be in %s' %
                             (self.__class__.__name__ + '.set_linecolor:',
                                 color, list(drawing_tool.line_colors.keys())))
        self._for_all_shapes('set_linecolor', color)
        return self

    def set_arrow(self, style):
        styles = ('->', '<-', '<->')
        if not style in styles:
            raise ValueError('%s: style=%s must be in %s' %
                             (self.__class__.__name__ + '.set_arrow:',
                              style, styles))
        self._for_all_shapes('set_arrow', style)
        return self

    def set_filled_curves(self, color='', pattern=''):
        if color in drawing_tool.line_colors:
            color = drawing_tool.line_colors[color]
        elif color in drawing_tool.line_colors.values():
            pass # color is ok
        else:
            raise ValueError('%s: invalid color "%s", must be in %s' %
                             (self.__class__.__name__ + '.set_filled_curves:',
                              color, list(drawing_tool.line_colors.keys())))
        self._for_all_shapes('set_filled_curves', color, pattern)
        return self

    def show_hierarchy(self, indent=0, format='std'):
        """Recursive pretty print of hierarchy of objects."""
        if not isinstance(self.shapes, dict):
            print 'cannot print hierarchy when %s.shapes is not a dict' % \
                  self.__class__.__name__
        s = ''
        if format == 'dict':
            s += '{'
        for shape in self.shapes:
            if format == 'dict':
                shape_str = repr(shape) + ':'
            elif format == 'plain':
                shape_str = shape
            else:
                shape_str = shape + ':'
            if format == 'dict' or format == 'plain':
                class_str = ''
            else:
                class_str = ' (%s)' % \
                            self.shapes[shape].__class__.__name__
            s += '\n%s%s%s %s' % (
                ' '*indent,
                shape_str,
                class_str,
                self.shapes[shape].show_hierarchy(indent+4, format))

        if format == 'dict':
            s += '}'
        return s

    def __str__(self):
        """Display hierarchy with minimum information (just object names)."""
        return self.show_hierarchy(format='plain')

    def __repr__(self):
        """Display hierarchy as a dictionary."""
        return self.show_hierarchy(format='dict')
        #return pprint.pformat(self.shapes)


class Curve(Shape):
    """General curve as a sequence of (x,y) coordintes."""
    def __init__(self, x, y):
        """
        `x`, `y`: arrays holding the coordinates of the curve.
        """
        self.x = asarray(x, dtype=float)
        self.y = asarray(y, dtype=float)
        #self.shapes must not be defined in this class
        #as self.shapes holds children objects:
        #Curve has no children (end leaf of self.shapes tree)

        self.linestyle = None
        self.linewidth = None
        self.linecolor = None
        self.fillcolor = None
        self.fillpattern = None
        self.arrow = None

    def inside_plot_area(self, verbose=True):
        """Check that all coordinates are within drawing_tool's area."""
        xmin, xmax = self.x.min(), self.x.max()
        ymin, ymax = self.y.min(), self.y.max()
        t = drawing_tool
        inside = True
        if xmin < t.xmin:
            inside = False
            if verbose:
                print 'x_min=%g < plot area x_min=%g' % (xmin, t.xmin)
        if xmax > t.xmax:
            inside = False
            if verbose:
                print 'x_max=%g > plot area x_max=%g' % (xmax, t.xmax)
        if ymin < t.ymin:
            inside = False
            if verbose:
                print 'y_min=%g < plot area y_min=%g' % (ymin, t.ymin)
        if xmax > t.xmax:
            inside = False
            if verbose:
                print 'y_max=%g > plot area y_max=%g' % (ymax, t.ymax)
        return inside

    def draw(self):
        """
        Send the curve to the plotting engine. That is, convert
        coordinate information in self.x and self.y, together
        with optional settings of linestyles, etc., to
        plotting commands for the chosen engine.
        """
        self.inside_plot_area()
        drawing_tool.plot_curve(
            self.x, self.y,
            self.linestyle, self.linewidth, self.linecolor,
            self.arrow, self.fillcolor, self.fillpattern)

    def rotate(self, angle, center):
        """
        Rotate all coordinates: `angle` is measured in degrees and
        (`x`,`y`) is the "origin" of the rotation.
        """
        angle = angle*pi/180
        x, y = center
        c = cos(angle);  s = sin(angle)
        xnew = x + (self.x - x)*c - (self.y - y)*s
        ynew = y + (self.x - x)*s + (self.y - y)*c
        self.x = xnew
        self.y = ynew
        return self

    def scale(self, factor):
        """Scale all coordinates by `factor`: ``x = factor*x``, etc."""
        self.x = factor*self.x
        self.y = factor*self.y
        return self

    def translate(self, vec):
        """Translate all coordinates by a vector `vec`."""
        self.x += vec[0]
        self.y += vec[1]
        return self

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

    def set_name(self, name):
        self.name = name
        return self

    def set_filled_curves(self, color='', pattern=''):
        self.fillcolor = color
        self.fillpattern = pattern
        return self

    def show_hierarchy(self, indent=0, format='std'):
        if format == 'dict':
            return '"%s"' % str(self)
        elif format == 'plain':
            return ''
        else:
            return str(self)

    def __str__(self):
        """Compact pretty print of a Curve object."""
        s = '%d coords' % self.x.size
        if not self.inside_plot_area(verbose=False):
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


class Point(Shape):
    """A point (x,y) which can be rotated, translated, and scaled."""
    def __init__(self, x, y):
        self.x, self.y = x, y
        #self.shapes is not needed in this class

    def __add__(self, other):
        if isinstance(other, (list,tuple)):
            other = Point(other)
        return Point(self.x+other.x, self.y+other.y)

    # class Point is an abstract class - only subclasses are useful
    # and must implement draw
    def draw(self):
        raise NotImplementedError(
            'class %s must implement the draw method' %
            self.__class__.__name__)

    def rotate(self, angle, center):
        """Rotate point an `angle` (in degrees) around (`x`,`y`)."""
        angle = angle*pi/180
        x, y = center
        c = cos(angle);  s = sin(angle)
        xnew = x + (self.x - x)*c - (self.y - y)*s
        ynew = y + (self.x - x)*s + (self.y - y)*c
        self.x = xnew
        self.y = ynew
        return self

    def scale(self, factor):
        """Scale point coordinates by `factor`: ``x = factor*x``, etc."""
        self.x = factor*self.x
        self.y = factor*self.y
        return self

    def translate(self, vec):
        """Translate point by a vector `vec`."""
        self.x += vec[0]
        self.y += vec[1]
        return self

    def show_hierarchy(self, indent=0, format='std'):
        s = '%s at (%g,%g)' % (self.__class__.__name__, self.x, self.y)
        if format == 'dict':
            return '"%s"' % s
        elif format == 'plain':
            return ''
        else:
            return s

# no need to store input data as they are invalid after rotations etc.
class Rectangle(Shape):
    """
    Rectangle specified by the point `lower_left_corner`, `width`,
    and `height`.

    Recorded geometric features:

    ==================== =============================================
    Attribute            Description
    ==================== =============================================
    lower_left           Lower left corner point.
    upper_left           Upper left corner point.
    lower_right          Lower right corner point.
    upper_right          Upper right corner point.
    lower_mid            Middle point on lower side.
    upper_mid            Middle point on upper side.
    ==================== =============================================
    """
    def __init__(self, lower_left_corner, width, height):
        is_sequence(lower_left_corner)
        p = arr2D(lower_left_corner)  # short form
        x = [p[0], p[0] + width,
             p[0] + width, p[0], p[0]]
        y = [p[1], p[1], p[1] + height,
             p[1] + height, p[1]]
        self.shapes = {'rectangle': Curve(x,y)}

        # Geometric features
        self.lower_left  = lower_left_corner
        self.lower_right = lower_left_corner + point(width,0)
        self.upper_left  = lower_left_corner + point(0,height)
        self.upper_right = lower_left_corner + point(width,height)
        self.lower_mid = 0.5*(self.lower_left + self.lower_right)
        self.upper_mid = 0.5*(self.upper_left + self.upper_right)


class Triangle(Shape):
    """
    Triangle defined by its three vertices p1, p2, and p3.

    Recorded geometric features:

    ==================== =============================================
    Attribute            Description
    ==================== =============================================
    p1, p2, p3           Corners as given to the constructor.
    ==================== =============================================

    """
    def __init__(self, p1, p2, p3):
        is_sequence(p1, p2, p3)
        x = [p1[0], p2[0], p3[0], p1[0]]
        y = [p1[1], p2[1], p3[1], p1[1]]
        self.shapes = {'triangle': Curve(x,y)}

        # Geometric features
        self.p1 = arr2D(p1)
        self.p2 = arr2D(p2)
        self.p3 = arr2D(p3)


class Line(Shape):
    def __init__(self, start, end):
        is_sequence(start, end)
        x = [start[0], end[0]]
        y = [start[1], end[1]]
        self.shapes = {'line': Curve(x, y)}

    def compute_formulas(self):
        x, y = self.shapes['line'].x, self.shapes['line'].y

        # Define equations for line:
        # y = a*x + b,  x = c*y + d
        try:
            self.a = (y[1] - y[0])/(x[1] - x[0])
            self.b = y[0] - self.a*x[0]
        except ZeroDivisionError:
            # Vertical line, y is not a function of x
            self.a = None
            self.b = None
        try:
            if self.a is None:
                self.c = 0
            else:
                self.c = 1/float(self.a)
            if self.b is None:
                self.d = x[1]
        except ZeroDivisionError:
            # Horizontal line, x is not a function of y
            self.c = None
            self.d = None

    def compute_formulas(self):
        x, y = self.shapes['line'].x, self.shapes['line'].y

        tol = 1E-14
        # Define equations for line:
        # y = a*x + b,  x = c*y + d
        if abs(x[1] - x[0]) > tol:
            self.a = (y[1] - y[0])/(x[1] - x[0])
            self.b = y[0] - self.a*x[0]
        else:
            # Vertical line, y is not a function of x
            self.a = None
            self.b = None
        if self.a is None:
            self.c = 0
        elif abs(self.a) > tol:
            self.c = 1/float(self.a)
            self.d = x[1]
        else:  # self.a is 0
            # Horizontal line, x is not a function of y
            self.c = None
            self.d = None

    def __call__(self, x=None, y=None):
        """Given x, return y on the line, or given y, return x."""
        self.compute_formulas()
        if x is not None and self.a is not None:
            return self.a*x + self.b
        elif y is not None and self.c is not None:
            return self.c*y + self.d
        else:
            raise ValueError(
                'Line.__call__(x=%s, y=%s) not meaningful' % \
                (x, y))

# First implementation of class Circle
class Circle(Shape):
    def __init__(self, center, radius, resolution=180):
        self.center, self.radius = center, radius
        self.resolution = resolution

        t = linspace(0, 2*pi, resolution+1)
        x0 = center[0];  y0 = center[1]
        R = radius
        x = x0 + R*cos(t)
        y = y0 + R*sin(t)
        self.shapes = {'circle': Curve(x, y)}

    def __call__(self, theta):
        """
        Return (x, y) point corresponding to angle theta.
        Not valid after a translation, rotation, or scaling.
        """
        return self.center[0] + self.radius*cos(theta), \
               self.center[1] + self.radius*sin(theta)


class Arc(Shape):
    def __init__(self, center, radius,
                 start_angle, arc_angle,
                 resolution=180):
        is_sequence(center)
        self.center = center
        self.radius = radius
        self.start_angle = start_angle*pi/180  # radians
        self.arc_angle = arc_angle*pi/180
        self.resolution = resolution

        t = linspace(self.start_angle,
                     self.start_angle + self.arc_angle,
                     resolution+1)
        x0 = center[0];  y0 = center[1]
        R = radius
        x = x0 + R*cos(t)
        y = y0 + R*sin(t)
        self.shapes = {'arc': Curve(x, y)}

    def __call__(self, theta):
        """
        Return (x,y) point at start_angle + theta.
        Not valid after translation, rotation, or scaling.
        """
        theta = theta*pi/180
        t = self.start_angle + theta
        x0 = self.center[0]
        y0 = self.center[1]
        R = self.radius
        x = x0 + R*cos(t)
        y = y0 + R*sin(t)
        return (x, y)

# Alternative for small arcs: Parabola

class Parabola(Shape):
    def __init__(self, start, mid, stop, resolution=21):
        self.p1, self.p2, self.p3 = start, mid, stop

        # y as function of x? (no point on line x=const?)
        tol = 1E-14
        if abs(self.p1[0] - self.p2[0]) > 1E-14 and \
           abs(self.p2[0] - self.p3[0]) > 1E-14 and \
           abs(self.p3[0] - self.p1[0]) > 1E-14:
            self.y_of_x = True
        else:
            self.y_of_x = False
        # x as function of y? (no point on line y=const?)
        tol = 1E-14
        if abs(self.p1[1] - self.p2[1]) > 1E-14 and \
           abs(self.p2[1] - self.p3[1]) > 1E-14 and \
           abs(self.p3[1] - self.p1[1]) > 1E-14:
            self.x_of_y = True
        else:
            self.x_of_y = False

        if self.y_of_x:
            x = linspace(start[0], end[0], resolution)
            y = self(x=x)
        elif self.x_of_y:
            y = linspace(start[1], end[1], resolution)
            x = self(y=y)
        else:
            raise ValueError(
                'Parabola: two or more points lie on x=const '
                'or y=const - not allowed')
        self.shapes = {'parabola': Curve(x, y)}

    def __call__(self, x=None, y=None):
        if x is not None and self.y_of_x:
            return self._L2x(self.p1, self.p2)*self.p3[1] + \
                   self._L2x(self.p2, self.p3)*self.p1[1] + \
                   self._L2x(self.p3, self.p1)*self.p2[1]
        elif y is not None and self.x_of_y:
            return self._L2y(self.p1, self.p2)*self.p3[0] + \
                   self._L2y(self.p2, self.p3)*self.p1[0] + \
                   self._L2y(self.p3, self.p1)*self.p2[0]
        else:
            raise ValueError(
                'Parabola.__call__(x=%s, y=%s) not meaningful' % \
                (x, y))

    def _L2x(self, x, pi, pj, pk):
        return (x - pi[0])*(x - pj[0])/((pk[0] - pi[0])*(pk[0] - pj[0]))

    def _L2y(self, y, pi, pj, pk):
        return (y - pi[1])*(y - pj[1])/((pk[1] - pi[1])*(pk[1] - pj[1]))


class Circle(Arc):
    def __init__(self, center, radius, resolution=180):
        Arc.__init__(self, center, radius, 0, 360, resolution)


class Wall(Shape):
    def __init__(self, x, y, thickness, pattern='/'):
        is_sequence(x, y, length=len(x))
        if isinstance(x[0], (tuple,list,ndarray)):
            # x is list of curves
            x1 = concatenate(x)
        else:
            x1 = asarray(x, float)
        if isinstance(y[0], (tuple,list,ndarray)):
            # x is list of curves
            y = concatenate(y)
        else:
            y1 = asarray(y, float)

        # Displaced curve (according to thickness)
        x2 = x1
        y2 = y1 + thickness
        # Combine x1,y1 with x2,y2 reversed
        from numpy import concatenate
        x = concatenate((x1, x2[-1::-1]))
        y = concatenate((y1, y2[-1::-1]))
        wall = Curve(x, y)
        wall.set_filled_curves(color='white', pattern=pattern)
        self.shapes = {'wall': wall}


class VelocityProfile(Shape):
    def __init__(self, start, height, profile, num_arrows, scaling=1):
        # vx, vy = profile(y)

        shapes = {}
        # Draw left line
        shapes['start line'] = Line(start, (start[0], start[1]+height))

        # Draw velocity arrows
        dy = float(height)/(num_arrows-1)
        x = start[0]
        y = start[1]
        r = profile(y)  # Test on return type
        if not isinstance(r, (list,tuple,ndarray)) and len(r) != 2:
            raise TypeError('VelocityProfile constructor: profile(y) function must return velocity vector (vx,vy), not %s' % type(r))

        for i in range(num_arrows):
            y = i*dy
            vx, vy = profile(y)
            if abs(vx) < 1E-8:
                continue
            vx *= scaling
            vy *= scaling
            arr = Arrow1((x,y), (x+vx, y+vy), '->')
            shapes['arrow%d' % i] = arr
        # Draw smooth profile
        xs = []
        ys = []
        n = 100
        dy = float(height)/n
        for i in range(n+2):
            y = i*dy
            vx, vy = profile(y)
            vx *= scaling
            vy *= scaling
            xs.append(x+vx)
            ys.append(y+vy)
        shapes['smooth curve'] = Curve(xs, ys)
        self.shapes = shapes


class Arrow1(Shape):
    """Draw an arrow as Line with arrow."""
    def __init__(self, start, end, style='->'):
        arrow = Line(start, end)
        arrow.set_arrow(style)
        self.shapes = {'arrow': arrow}

class Arrow3(Shape):
    """
    Build a vertical line and arrow head from Line objects.
    Then rotate `rotation_angle`.
    """
    def __init__(self, start, length, rotation_angle=0):
        self.bottom = start
        self.length = length
        self.angle = rotation_angle

        top = (self.bottom[0], self.bottom[1] + self.length)
        main = Line(self.bottom, top)
        #head_length = self.length/8.0
        head_length = drawing_tool.xrange/50.
        head_degrees = 30*pi/180
        head_left_pt = (top[0] - head_length*sin(head_degrees),
                        top[1] - head_length*cos(head_degrees))
        head_right_pt = (top[0] + head_length*sin(head_degrees),
                         top[1] - head_length*cos(head_degrees))
        head_left = Line(head_left_pt, top)
        head_right = Line(head_right_pt, top)
        head_left.set_linestyle('solid')
        head_right.set_linestyle('solid')
        self.shapes = {'line': main, 'head left': head_left,
                       'head right': head_right}

        # rotate goes through self.shapes so self.shapes
        # must be initialized first
        self.rotate(rotation_angle, start)


class Text(Point):
    """
    Place `text` at the (x,y) point `position`, with the given
    fontsize. The text is centered around `position` if `alignment` is
    'center'; if 'left', the text starts at `position`, and if
    'right', the right and of the text is located at `position`.
    """
    def __init__(self, text, position, alignment='center', fontsize=14):
        is_sequence(position)
        is_sequence(position, length=2, can_be_None=True)
        self.text = text
        self.position = position
        self.alignment = alignment
        self.fontsize = fontsize
        Point.__init__(self, position[0], position[1])
        #no need for self.shapes here

    def draw(self):
        drawing_tool.text(self.text, (self.x, self.y),
                          self.alignment, self.fontsize)

    def __str__(self):
        return 'text "%s" at (%g,%g)' % (self.text, self.x, self.y)

    def __repr__(self):
        return str(self)


class Text_wArrow(Text):
    """
    As class Text, but an arrow is drawn from the mid part of the text
    to some point `arrow_tip`.
    """
    def __init__(self, text, position, arrow_tip,
                 alignment='center', fontsize=14):
        is_sequence(arrow_tip, length=2, can_be_None=True)
        is_sequence(position)
        self.arrow_tip = arrow_tip
        Text.__init__(self, text, position, alignment, fontsize)

    def draw(self):
        drawing_tool.text(self.text, self.position,
                          self.alignment, self.fontsize,
                          self.arrow_tip)
    def __str__(self):
        return 'annotation "%s" at (%g,%g) with arrow to (%g,%g)' % \
               (self.text, self.x, self.y,
                self.arrow_tip[0], self.arrow_tip[1])

    def __repr__(self):
        return str(self)


class Axis(Shape):
    def __init__(self, start, length, label, below=True,
                 rotation_angle=0, fontsize=14,
                 label_spacing=1./30):
        """
        Draw axis from start with `length` to the right
        (x axis). Place label below (True) or above (False) axis.
        Then return `rotation_angle` (in degrees).
        To make a standard x axis, call with ``below=True`` and
        ``rotation_angle=0``. To make a standard y axis, call with
        ``below=False`` and ``rotation_angle=90``.
        A tilted axis can also be drawn.
        The `label_spacing` denotes the space between the symbol
        and the arrow tip as a fraction of the length of the plot
        in x direction.
        """
        # Arrow is vertical arrow, make it horizontal
        arrow = Arrow3(start, length, rotation_angle=-90)
        arrow.rotate(rotation_angle, start)
        spacing = drawing_tool.xrange*label_spacing
        if below:
            spacing = - spacing
        label_pos = [start[0] + length, start[1] + spacing]
        symbol = Text(label, position=label_pos, fontsize=fontsize)
        symbol.rotate(rotation_angle, start)
        self.shapes = {'arrow': arrow, 'symbol': symbol}

class Gravity(Axis):
    """Downward-pointing gravity arrow with the symbol g."""
    def __init__(self, start, length):
        Axis.__init__(self, start, length, '$g$', below=False,
                      rotation_angle=-90, label_spacing=1./30)

class Force(Arrow1):
    """
    Indication of a force by an arrow and a symbol.
    Draw an arrow, starting at `start` and with the tip at `end`.
    The symbol is placed at the `start` point, in a distance
    `symbol_spacing` times the width of the total plotting area.
    """
    def __init__(self, start, end, symbol, symbol_spacing=1./60,
                 fontsize=14):
        Arrow1.__init__(self, start, end, style='->')
        spacing = drawing_tool.xrange*symbol_spacing
        start, end = arr2D(start), arr2D(end)
        spacing_dir = start - end
        spacing_dir /= sqrt(spacing_dir[0]**2 + spacing_dir[1]**2)
        symbol_pos = start + spacing*spacing_dir
        self.shapes['symbol'] = Text(symbol, symbol_pos, fontsize=fontsize)


class Distance_wText(Shape):
    """
    Arrow <-> with text (usually a symbol) at the midpoint, used for
    identifying a some distance in a figure.  The text is placed
    slightly to the right of vertical-like arrows, with text displaced
    `text_spacing` times to total distance in x direction of the plot
    area. The text is by default aligned 'left' in this case. For
    horizontal-like arrows, the text is placed the same distance
    above, but aligned 'center' by default (when `alignment` is None).
    """
    def __init__(self, start, end, text, fontsize=14, text_spacing=1/60.,
                 alignment=None, text_pos='mid'):
        start = arr2D(start)
        end   = arr2D(end)

        # Decide first if we have a vertical or horizontal arrow
        vertical = abs(end[0]-start[0]) < 2*abs(end[1]-start[1])

        if vertical:
            # Assume end above start
            if end[1] < start[1]:
                start, end = end, start
            if alignment is None:
                alignment = 'left'
        else:  # horizontal arrow
            # Assume start to the right of end
            if start[0] < end[0]:
                start, end = end, start
            if alignment is None:
                alignment = 'center'

        tangent = end - start
        # Tangeng goes always to the left and upward
        normal = arr2D([tangent[1], -tangent[0]])/\
                       sqrt(tangent[0]**2 + tangent[1]**2)
        mid = 0.5*(start + end)  # midpoint of start-end line

        if text_pos == 'mid':
            text_pos = mid + normal*drawing_tool.xrange*text_spacing
            text = Text(text, text_pos, fontsize=fontsize,
                        alignment=alignment)
        else:
            is_sequence(text_pos, length=2)
            text = Text_wArrow(text, text_pos, mid, alignment='left',
                               fontsize=fontsize)
        arrow = Arrow1(start, end, style='<->')
        arrow.set_linecolor('black')
        arrow.set_linewidth(1)
        self.shapes = {'arrow': arrow, 'text': text}


class ArcSymbol(Shape):
    def __init__(self, symbol, center, radius,
                 start_angle, arc_angle, fontsize=14,
                 resolution=180, symbol_spacing=1/60.):
        arc = Arc(center, radius, start_angle, arc_angle,
                  resolution)
        mid = arr2D(arc(arc_angle/2.))
        normal = mid - arr2D(center)
        normal = normal/sqrt(normal[0]**2 + normal[1]**2)
        symbol_pos = mid + normal*drawing_tool.xrange*symbol_spacing
        self.shapes = {'arc': arc,
                       'symbol': Text(symbol, symbol_pos, fontsize=fontsize)}

class Compose(Shape):
    def __init__(self, shapes):
        """shapes: list or dict of Shape objects."""
        self.shapes = shapes


# can make help methods: Line.midpoint, Line.normal(pt, dir='left') -> (x,y)

# list annotations in each class? contains extra annotations for explaining
# important parameters to the constructor, e.g., Line.annotations holds
# start and end as Text objects. Shape.demo calls shape.draw and
# for annotation in self.demo: annotation.draw() YES!
# Can make overall demo of classes by making objects and calling demo
# Could include demo fig in each constructor


class SimplySupportedBeam(Shape):
    def __init__(self, pos, size):
        pos = arr2D(pos)
        P0 = (pos[0] - size/2., pos[1]-size)
        P1 = (pos[0] + size/2., pos[1]-size)
        triangle = Triangle(P0, P1, pos)
        gap = size/5.
        h = size/4.  # height of rectangle
        P2 = (P0[0], P0[1]-gap-h)
        rectangle = Rectangle(P2, size, h).set_filled_curves(pattern='/')
        self.shapes = {'triangle': triangle, 'rectangle': rectangle}

        self.dimensions = {'pos': Text('pos', pos),
                           'size': Distance_wText((P2[0], P2[1]-size),
                                                  (P2[0]+size, P2[1]-size),
                                                  'size')}
        # Geometric features
        self.mid_support = point(P2[0] + size/2., P2[1])  # lower center
        self.top = pos


class ConstantBeamLoad(Shape):
    """
    Downward-pointing arrows indicating a vertical load.
    The arrows are of equal length and filling a rectangle
    specified as in the :class:`Rectangle` class.

    Recorded geometric features:

    ==================== =============================================
    Attribute            Description
    ==================== =============================================
    mid_point            Middle point at the top of the row of
                         arrows (often used for positioning a text).
    ==================== =============================================
    """
    def __init__(self, lower_left_corner, width, height, num_arrows=10):
        box = Rectangle(lower_left_corner, width, height)
        self.shapes = {'box': box}
        dx = float(width)/(num_arrows-1)
        y_top = lower_left_corner[1] + height
        y_tip = lower_left_corner[1]
        for i in range(num_arrows):
            x = lower_left_corner[0] + i*dx
            self.shapes['arrow%d' % i] = Arrow1((x, y_top), (x, y_tip))

        # Geometric features
        self.mid_top = arr2D(lower_left_corner) + point(width/2., height)

class Moment(ArcSymbol):
    def __init__(self, symbol, center, radius,
                 left=True, counter_clockwise=True,
                 fontsize=14, symbol_spacing=1/60.):
        style = '->' if counter_clockwise else '<-'
        start_angle = 90 if left else -90
        ArcSymbol.__init__(self, symbol, center, radius,
                           start_angle=start_angle,
                           arc_angle=180, fontsize=fontsize,
                           symbol_spacing=symbol_spacing,
                           resolution=180)
        self.shapes['arc'].set_arrow(style)


class Wheel(Shape):
    def __init__(self, center, radius, inner_radius=None, nlines=10):
        if inner_radius is None:
            inner_radius = radius/5.0

        outer = Circle(center, radius)
        inner = Circle(center, inner_radius)
        lines = []
        # Draw nlines+1 since the first and last coincide
        # (then nlines lines will be visible)
        t = linspace(0, 2*pi, self.nlines+1)

        Ri = inner_radius;  Ro = radius
        x0 = center[0];  y0 = center[1]
        xinner = x0 + Ri*cos(t)
        yinner = y0 + Ri*sin(t)
        xouter = x0 + Ro*cos(t)
        youter = y0 + Ro*sin(t)
        lines = [Line((xi,yi),(xo,yo)) for xi, yi, xo, yo in \
                 zip(xinner, yinner, xouter, youter)]
        self.shapes = {'inner': inner, 'outer': outer,
                       'spokes': Compose(
                           {'spoke%d' % i: lines[i]
                            for i in range(len(lines))})}

class SineWave(Shape):
    def __init__(self, xstart, xstop,
                 wavelength, amplitude, mean_level):
        self.xstart = xstart
        self.xstop = xstop
        self.wavelength = wavelength
        self.amplitude = amplitude
        self.mean_level = mean_level

        npoints = (self.xstop - self.xstart)/(self.wavelength/61.0)
        x = linspace(self.xstart, self.xstop, npoints)
        k = 2*pi/self.wavelength # frequency
        y = self.mean_level + self.amplitude*sin(k*x)
        self.shapes = {'waves': Curve(x,y)}



class Spring1(Shape):
    """
    Specify a vertical spring, starting at `start`, with
    given vertical `length`. In the middle of the
    spring there are `num_teeth` saw teeth.

    Recorded geometric features:

    ==================== =============================================
    Attribute            Description
    ==================== =============================================
    start                Start point of spring.
    end                  End point of spring.
    ==================== =============================================
    """
    spring_fraction = 1./2  # fraction of total length occupied by spring

    def __init__(self, start, length, tooth_width, num_teeth=8):
        B = start
        n = num_teeth - 1  # n counts teeth intervals
        # n must be odd:
        if n % 2 == 0:
            n = n+1
        L = length
        w = tooth_width

        # [0, x, L-x, L], f = (L-2*x)/L
        # x = L*(1-f)/2.
        shapes = {}
        f = Spring1.spring_fraction
        t = f*L/n      # distance between teeth
        s = L*(1-f)/2. # start of spring
        P0 = (B[0], B[1]+s)
        shapes['line start'] = Line(B, P0)
        T1 = P0
        T2 = (T1[0] + w, T1[1] + t/2.0)
        k = 1
        shapes['line%d' % k] = Line(T1,T2)
        T1 = T2[:]  # copy
        for i in range(2*n-3):
            T2 = (T1[0] + (-1)**(i+1)*2*w, T1[1] + t/2.0)
            k += 1
            shapes['line%d' % k] = Line(T1, T2)
            T1 = (T2[0], T2[1])
        T2 = (T1[0] + w, T1[1] + t/2.0)
        k += 1
        shapes['line%d' % k] = Line(T1,T2)

        P2 = (B[0], B[1]+L)
        shapes['line end'] = Line(T2, P2)
        self.shapes = shapes

        # Dimensions
        start = Text_wArrow('start', (B[0]-1.5*w,B[1]-1.5*w), B)
        width = Distance_wText((B[0]-w, B[1]-3.5*w), (B[0]+w, B[1]-3.5*w),
                               'tooth_width')
        length = Distance_wText((B[0]+3*w, B[1]), (B[0]+3*w, B[1]+L),
                                'length')
        num_teeth = Text_wArrow('num_teeth',
                                (B[0]+2*w,P2[1]+w),
                                (B[0]+1.2*w, B[1]+L/2.))
        dims = {'start': start, 'width': width, 'length': length,
                'num_teeth': num_teeth}
        self.dimensions = dims

        # Geometric features
        self.start = B
        self.end = point(B[0], B[1]+L)


class Spring2(Shape):
    """
    Specify a vertical spring, starting at `start` and,
    with vertical `length`. In the middle of the
    spring there are `num_windings` circular windings to illustrate
    the spring.

    Recorded geometric features:

    ==================== =============================================
    Attribute            Description
    ==================== =============================================
    start                Start point of spring.
    end                  End point of spring.
    ==================== =============================================

    """
    spring_fraction = 1./2  # fraction of total length occupied by spring

    def __init__(self, start, length, width, num_windings=11):
        B = start
        n = num_windings - 1  # n counts teeth intervals
        if n <= 6:
            n = 7
        # n must be odd:
        if n % 2 == 0:
            n = n+1
        L = length
        w = width

        # [0, x, L-x, L], f = (L-2*x)/L
        # x = L*(1-f)/2.
        shapes = {}
        f = Spring2.spring_fraction
        t = f*L/n      # must be better worked out
        s = L*(1-f)/2. # start of spring
        P0 = (B[0], B[1]+s)
        shapes['line start'] = Line(B, P0)
        q = linspace(0, n, n*180 + 1)
        x = P0[0] + w*sin(2*pi*q)
        y = P0[1] + q*t
        shapes['sprial'] = Curve(x, y)
        P1 = (B[0], L-s)
        P2 = (B[0], B[1]+L)
        shapes['line end'] = Line(P1,P2)
        self.shapes = shapes

        # Dimensions
        start = Text_wArrow('start', (B[0]-1.5*w,B[1]-1.5*w), B)
        width = Distance_wText((B[0]-w, B[1]-3.5*w), (B[0]+w, B[1]-3.5*w),
                               'width')
        length = Distance_wText((B[0]+3*w, B[1]), (B[0]+3*w, B[1]+L),
                                'length')
        num_windings = Text_wArrow('num_windings',
                                   (B[0]+2*w,P2[1]+w),
                                   (B[0]+1.2*w, B[1]+L/2.))
        spring_length = Distance_wText((B[0]-2*w, P0[1]), (B[0]-2*w, P1[1]),
                                       'Spring2.spring_fraction*length',
                                       text_pos=(B[0]-6*w, P2[1]+2.5*w))
        dims = {'start': start, 'width': width, 'length': length,
                'num_windings': num_windings, 'spring_length': spring_length}
        self.dimensions = dims

        # Geometric features
        self.start = B
        self.end = point(B[0], B[1]+L)

class Dashpot(Shape):
    """
    Specify a vertical dashpot of height `total_length` and
    `start` as bottom/starting point. The rectangular dashpot part
    has width `width` and height `dashpot_length`.  If the latter
    is not given (None), it becomes
    ``Dashpot.dashpot_fraction*total_length`` (default
    ``total_length/2```).  The piston position inside the
    rectangular dashpot, can be specified as `piston_pos`, (the
    default value None places it at 1/3 from the bottom of the
    dashpot).

    Recorded geometric features:

    ==================== =============================================
    Attribute            Description
    ==================== =============================================
    start                Start point of dashpot.
    end                  End point of dashpot.
    ==================== =============================================
    """
    dashpot_fraction = 1./2
    piston_gap_fraction = 1./6
    piston_thickness_fraction = 1./8

    def __init__(self, start, total_length,
                 width, dashpot_length=None, piston_pos=None):
        B = start
        L = total_length
        w = width

        # [0, x, L-x, L], f = (L-2*x)/L
        # x = L*(1-f)/2.

        shapes = {}
        # dashpot is P0-P1 in y and width 2*w
        if dashpot_length is None:
            f = Dashpot.dashpot_fraction
            s = L*(1-f)/2. # start of dashpot
            P1 = (B[0], B[1]+L-s)
            dashpot_length = f*L
        else:
            f = 1./2
            s = f*dashpot_length # start of dashpot
            P1 = (B[0], B[1]+s+dashpot_length)
        P0 = (B[0], B[1]+s)
        P2 = (B[0], B[1]+L)
        shapes['line start'] = Line(B, P0)

        shapes['pot'] = Curve([P1[0]-w, P0[0]-w, P0[0]+w, P1[0]+w],
                              [P1[1], P0[1], P0[1], P1[1]])
        piston_thickness = f*L*Dashpot.piston_thickness_fraction
        if piston_pos is None:
            piston_pos = P0[1] + 1/3.*dashpot_length
        if piston_pos < P0[1]:
            piston_pos = P0[1]
        if piston_pos > P1[1]-piston_thickness:
            piston_pos = P1[1]-piston_thickness
        gap = w*Dashpot.piston_gap_fraction
        shapes['piston'] = Compose(
            {'line': Line(P2, (B[0], piston_pos + piston_thickness)),
             'rectangle': Rectangle((B[0] - w+gap, piston_pos),
                                    2*w-2*gap, piston_thickness),
             })
        shapes['piston']['rectangle'].set_filled_curves(pattern='X')

        self.shapes = shapes

        # Dimensions
        start = Text_wArrow('start', (B[0]-1.5*w,B[1]-1.5*w), B)
        width = Distance_wText((B[0]-w, B[1]-3.5*w), (B[0]+w, B[1]-3.5*w),
                               'width')
        dplength = Distance_wText((B[0]+2*w, P0[1]), (B[0]+2*w, P1[1]),
                               'dashpot_length', text_pos=(B[0]+w,B[1]-w))
        tlength = Distance_wText((B[0]+4*w, B[1]), (B[0]+4*w, B[1]+L),
                                 'total_length',
                                 text_pos=(B[0]+4.5*w, B[1]+L-2*w))
        line = Line((B[0]+w, piston_pos), (B[0]+7*w, piston_pos)).set_linestyle('dotted').set_linecolor('black').set_linewidth(1)
        pp = Text('piston_pos', (B[0]+7*w, piston_pos), alignment='left')
        dims = {'start': start, 'width': width, 'dashpot_length': dplength,
                'total_length': tlength,
                'piston_pos': Compose({'line': line, 'text': pp})}
        self.dimensions = dims

        # Geometric features
        self.start = B
        self.end = point(B[0], B[1]+L)

# COMPOSITE types:
# MassSpringForce: Line(horizontal), Spring, Rectangle, Arrow/Line(w/arrow)
# must be easy to find the tip of the arrow
# Maybe extra dict: self.name['mass'] = Rectangle object - YES!

def test_Axis():
    set_coordinate_system(xmin=0, xmax=15, ymin=0, ymax=15, axis=True)
    x_axis = Axis((7.5,2), 5, 'x', rotation_angle=0)
    y_axis = Axis((7.5,2), 5, 'y', below=False, rotation_angle=90)
    system = Compose({'x axis': x_axis, 'y axis': y_axis})
    system.draw()
    drawing_tool.display()
    set_linestyle('dashed')
    #system.shapes['x axis'].rotate(40, (7.5, 2))
    #system.shapes['y axis'].rotate(40, (7.5, 2))
    system.rotate(40, (7.5,2))
    system.draw()
    drawing_tool.display('Axis')
    drawing_tool.savefig('tmp_Axis.png')
    print repr(system)

def test_Distance_wText():
    drawing_tool.set_coordinate_system(xmin=0, xmax=10,
                                       ymin=0, ymax=6,
                                       axis=True,
                                       instruction_file='tmp_mpl.py')
    #drawing_tool.arrow_head_width = 0.1
    fontsize=14
    t = r'$ 2\pi R^2 $'
    dims2 = Compose({
        'a0': Distance_wText((4,5), (8, 5), t, fontsize),
        'a6': Distance_wText((4,5), (4, 4), t, fontsize),
        'a1': Distance_wText((0,2), (2, 4.5), t, fontsize),
        'a2': Distance_wText((0,2), (2, 0), t, fontsize),
        'a3': Distance_wText((2,4.5), (0, 5.5), t, fontsize),
        'a4': Distance_wText((8,4), (10, 3), t, fontsize,
                             text_spacing=-1./60),
        'a5': Distance_wText((8,2), (10, 1), t, fontsize,
                             text_spacing=-1./40, alignment='right'),
        'c1': Text_wArrow('text_spacing=-1./60',
                          (4, 3.5), (9, 3.2),
                          fontsize=10, alignment='left'),
        'c2': Text_wArrow('text_spacing=-1./40, alignment="right"',
                          (4, 0.5), (9, 1.2),
                          fontsize=10, alignment='left'),
        })
    dims2.draw()
    drawing_tool.display('Distance_wText and text positioning')
    drawing_tool.savefig('tmp_Distance_wText.png')

def test_Springs():
    L = 5
    W = 2

    drawing_tool.set_coordinate_system(xmin=0, xmax=7*W,
                                       ymin=-2, ymax=L+2,
                                       axis=True)
    drawing_tool.set_linecolor('blue')
    drawing_tool.set_grid(True)

    xpos = W
    s1 = Spring1((W,0), L, W/4.)
    s1.draw()
    s1.draw_dimensions()
    xpos += 3*W
    s2 = Spring2((xpos,0), L, W/4.)
    s2.draw()
    s2.draw_dimensions()
    drawing_tool.display('Spring1 (left) and Spring2 (right)')
    drawing_tool.savefig('tmp_springs.png')


def test_Dashpot():
    L = 5
    W = 2

    drawing_tool.set_coordinate_system(xmin=xpos, xmax=xpos+5*W,
                                       ymin=-2, ymax=L+2,
                                       axis=True)
    drawing_tool.set_linecolor('blue')
    drawing_tool.set_grid(True)

    # Default (simple) dashpot
    xpos = 2
    d1 = Dashpot(start=(xpos,0), total_length=L, width=W/4.)
    text1 = Text('Dashpot (default)', (xpos, 1.1*L))
    d1.draw()
    text1.draw()

    # Dashpot for animation with fixed dashpot_length and
    # prescribed piston_pos
    xpos += 1.5*W
    d2 = Dashpot(start=(xpos,0), total_length=L+1.5, width=W/4.,
                 dashpot_length=2.5, piston_pos=L/2.)
    d2.draw()
    d2.draw_dimensions()

    drawing_tool.display('Dashpot')
    drawing_tool.savefig('tmp_dashpot.png')


def _test1():
    set_coordinate_system(xmin=0, xmax=10, ymin=0, ymax=10)
    l1 = Line((0,0), (1,1))
    l1.draw()
    input(': ')
    c1 = Circle((5,2), 1)
    c2 = Circle((6,2), 1)
    w1 = Wheel((7,2), 1)
    c1.draw()
    c2.draw()
    w1.draw()
    hardcopy()
    display()  # show the plot

def _test2():
    set_coordinate_system(xmin=0, xmax=10, ymin=0, ymax=10)
    l1 = Line((0,0), (1,1))
    l1.draw()
    input(': ')
    c1 = Circle((5,2), 1)
    c2 = Circle((6,2), 1)
    w1 = Wheel((7,2), 1)
    filled_curves(True)
    set_linecolor('blue')
    c1.draw()
    set_linecolor('aqua')
    c2.draw()
    filled_curves(False)
    set_linecolor('red')
    w1.draw()
    hardcopy()
    display()  # show the plot

def _test3():
    """Test example from the book."""
    set_coordinate_system(xmin=0, xmax=10, ymin=0, ymax=10)
    l1 = Line(start=(0,0), stop=(1,1))  # define line
    l1.draw()        # make plot data
    r1 = Rectangle(lower_left_corner=(0,1), width=3, height=5)
    r1.draw()
    Circle(center=(5,7), radius=1).draw()
    Wheel(center=(6,2), radius=2, inner_radius=0.5, nlines=7).draw()
    hardcopy()
    display()

def _test4():
    """Second example from the book."""
    set_coordinate_system(xmin=0, xmax=10, ymin=0, ymax=10)
    r1 = Rectangle(lower_left_corner=(0,1), width=3, height=5)
    c1 = Circle(center=(5,7), radius=1)
    w1 = Wheel(center=(6,2), radius=2, inner_radius=0.5, nlines=7)
    c2 = Circle(center=(7,7), radius=1)
    filled_curves(True)
    c1.draw()
    set_linecolor('blue')
    r1.draw()
    set_linecolor('aqua')
    c2.draw()
    # Add thick aqua line around rectangle:
    filled_curves(False)
    set_linewidth(4)
    r1.draw()
    set_linecolor('red')
    # Draw wheel with thick lines:
    w1.draw()
    hardcopy('tmp_colors')
    display()


def _test5():
    set_coordinate_system(xmin=0, xmax=10, ymin=0, ymax=10)
    c = 6.  # center point of box
    w = 2.  # size of box
    L = 3
    r1 = Rectangle((c-w/2, c-w/2), w, w)
    l1 = Line((c,c-w/2), (c,c-w/2-L))
    linecolor('blue')
    filled_curves(True)
    r1.draw()
    linecolor('aqua')
    filled_curves(False)
    l1.draw()
    hardcopy()
    display()  # show the plot

def rolling_wheel(total_rotation_angle):
    """Animation of a rotating wheel."""
    set_coordinate_system(xmin=0, xmax=10, ymin=0, ymax=10)

    import time
    center = (6,2)
    radius = 2.0
    angle = 2.0
    pngfiles = []
    w1 = Wheel(center=center, radius=radius, inner_radius=0.5, nlines=7)
    for i in range(int(total_rotation_angle/angle)):
        w1.draw()
        print 'XXXXXXXXXXXXXXXXXXXXXX BIG PROBLEM WITH ANIMATE!!!'
        display()


        filename = 'tmp_%03d' % i
        pngfiles.append(filename + '.png')
        hardcopy(filename)
        time.sleep(0.3)  # pause

        L = radius*angle*pi/180  # translation = arc length
        w1.rotate(angle, center)
        w1.translate((-L, 0))
        center = (center[0] - L, center[1])

        erase()
    cmd = 'convert -delay 50 -loop 1000 %s tmp_movie.gif' \
          % (' '.join(pngfiles))
    print 'converting PNG files to animated GIF:\n', cmd
    import commands
    failure, output = commands.getstatusoutput(cmd)
    if failure:  print 'Could not run', cmd


if __name__ == '__main__':
    #rolling_wheel(40)
    #_test1()
    #_test3()
    funcs = [
        #test_Axis,
        test_inclined_plane,
        ]
    for func in funcs:
        func()
        raw_input('Type Return: ')


