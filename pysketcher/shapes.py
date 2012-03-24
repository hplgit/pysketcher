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
    for x in sequences:
        _is_sequence(x, length=length, can_be_None=can_be_None,
                     error_message=error_message)
        ok, msg = drawing_tool.inside(x, exception=True)
        if not ok: print msg


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


    def for_all_shapes(self, func, *args, **kwargs):
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
        self.for_all_shapes('draw')
        return self

    def rotate(self, angle, center):
        is_sequence(center, length=2)
        self.for_all_shapes('rotate', angle, center)
        return self

    def translate(self, vec):
        is_sequence(vec, length=2)
        self.for_all_shapes('translate', vec)
        return self

    def scale(self, factor):
        self.for_all_shapes('scale', factor)
        return self

    def set_linestyle(self, style):
        styles = ('solid', 'dashed', 'dashdot', 'dotted')
        if style not in styles:
            raise ValueError('%s: style=%s must be in %s' %
                             (self.__class__.__name__ + '.set_linestyle:',
                              style, str(styles)))
        self.for_all_shapes('set_linestyle', style)
        return self

    def set_linewidth(self, width):
        if not isinstance(width, int) and width >= 0:
            raise ValueError('%s: width=%s must be positive integer' %
                             (self.__class__.__name__ + '.set_linewidth:',
                              width))
        self.for_all_shapes('set_linewidth', width)
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
        self.for_all_shapes('set_linecolor', color)
        return self

    def set_arrow(self, style):
        styles = ('->', '<-', '<->')
        if not style in styles:
            raise ValueError('%s: style=%s must be in %s' %
                             (self.__class__.__name__ + '.set_arrow:',
                              style, styles))
        self.for_all_shapes('set_arrow', style)
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
        self.for_all_shapes('set_filled_curves', color, pattern)
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

    def rotate(self, angle):
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
    def __init__(self, lower_left_corner, width, height):
        is_sequence(lower_left_corner)
        p = lower_left_corner  # short form
        x = [p[0], p[0] + width,
             p[0] + width, p[0], p[0]]
        y = [p[1], p[1], p[1] + height,
             p[1] + height, p[1]]
        self.shapes = {'rectangle': Curve(x,y)}

class Triangle(Shape):
    """Triangle defined by its three vertices p1, p2, and p3."""
    def __init__(self, p1, p2, p3):
        is_sequence(p1, p2, p3)
        x = [p1[0], p2[0], p3[0], p1[0]]
        y = [p1[1], p2[1], p3[1], p1[1]]
        self.shapes = {'triangle': Curve(x,y)}


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



class Text(Point):
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
    def __init__(self, bottom_point, length, label, below=True,
                 rotation_angle=0, label_spacing=1./30):
        """
        Draw axis from bottom_point with `length` to the right
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
        arrow = Arrow(bottom_point, length, rotation_angle=-90)
        arrow.rotate(rotation_angle, bottom_point)
        spacing = drawing_tool.xrange*label_spacing
        if below:
            spacing = - spacing
        label_pos = [bottom_point[0] + length, bottom_point[1] + spacing]
        symbol = Text(label, position=label_pos)
        symbol.rotate(rotation_angle, bottom_point)
        self.shapes = {'arrow': arrow, 'symbol': symbol}

class Gravity(Axis):
    """Downward-pointing gravity arrow with the symbol g."""
    def __init__(self, start, length):
        Axis.__init__(self, start, length, '$g$', below=False,
                      rotation_angle=-90, label_spacing=1./30)

def test_Axis():
    set_coordinate_system(xmin=0, xmax=15, ymin=0, ymax=15, axis=True)
    x_axis = Axis((7.5,2), 5, 'x', rotation_angle=0)
    y_axis = Axis((7.5,2), 5, 'y', below=False, rotation_angle=90)
    system = Compose({'x axis': x_axis, 'y axis': y_axis})
    system.draw()
    drawing_tool.display()
    set_linestyle('dashed')
    system.shapes['x axis'].rotate(40, (7.5, 2))
    system.shapes['y axis'].rotate(40, (7.5, 2))
    system.draw()
    drawing_tool.display()
    print repr(system)


class Distance_wSymbol(Shape):
    """
    Arrow with symbol at the midpoint,
    for identifying a distance with a symbol.
    """
    def __init__(self, start, end, symbol, symbol_spacing=1/60., fontsize=14):
        start = arr2D(start)
        end   = arr2D(end)
        mid = 0.5*(start + end)  # midpoint of start-end line
        tangent = end - start
        normal = arr2D([-tangent[1], tangent[0]])/\
                       sqrt(tangent[0]**2 + tangent[1]**2)
        symbol_pos = mid + normal*drawing_tool.xrange*symbol_spacing
        arrow = Arrow1(start, end, style='<->')
        arrow.set_linecolor('black')
        arrow.set_linewidth(1)
        self.shapes = {'arrow': arrow,
                       'symbol': Text(symbol, symbol_pos, fontsize=fontsize)}


class ArcSymbol(Shape):
    def __init__(self, symbol, center, radius,
                 start_angle, arc_angle,
                 symbol_spacing=1/60.,
                 resolution=180, fontsize=14):
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
    def __init__(self, bottom_point, length, rotation_angle=0):
        self.bottom = bottom_point
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

        # rotate goes through self.shapes so this must be initialized first
        self.rotate(rotation_angle, bottom_point)


class Wheel(Shape):
    def __init__(self, center, radius, inner_radius=None, nlines=10):
        self.center = center
        self.radius = radius
        if inner_radius is None:
            self.inner_radius = radius/5.0
        else:
            self.inner_radius = inner_radius
        self.nlines = nlines

        outer = Circle(self.center, self.radius)
        inner = Circle(self.center, self.inner_radius)
        lines = []
        # Draw nlines+1 since the first and last coincide
        # (then nlines lines will be visible)
        t = linspace(0, 2*pi, self.nlines+1)

        Ri = self.inner_radius;  Ro = self.radius
        x0 = self.center[0];  y0 = self.center[1]
        xinner = x0 + Ri*cos(t)
        yinner = y0 + Ri*sin(t)
        xouter = x0 + Ro*cos(t)
        youter = y0 + Ro*sin(t)
        lines = [Line((xi,yi),(xo,yo)) for xi, yi, xo, yo in \
                 zip(xinner, yinner, xouter, youter)]
        self.shapes = [outer, inner] + lines

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
    spring_fraction = 1./2  # fraction of total length occupied by spring

    def __init__(self, start, length, tooth_width, num_teeth=8):
        """
        Specify a vertical spring, starting at bottom_point and
        having a specified lengths. In the middle third of the
        spring there are ntooths saw thooth tips.
        """
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

class Spring2(Shape):
    spring_fraction = 1./2  # fraction of total length occupied by spring

    def __init__(self, start, length, width, num_windings=11):
        """
        Specify a vertical spring, starting at bottom_point and
        having a specified lengths. In the middle third of the
        spring there are ntooths saw thooth tips.
        """
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

class Dashpot(Shape):
    dashpot_fraction = 1./2  # fraction of total length occupied by dashpot
    piston_gap_fraction = 1./6
    piston_thickness_fraction = 1./8

    def __init__(self, start, length, width, piston_pos=None):
        """
        Specify a vertical dashpot of height `length`, width `width`,
        and `start` as bottom/starting point. The piston position,
        `piston_pos` can be specified, but default value None places
        it at 1/3 from the bottom of the dashpot.
        """
        B = start
        L = length
        w = width

        # [0, x, L-x, L], f = (L-2*x)/L
        # x = L*(1-f)/2.
        shapes = {}
        f = Dashpot.dashpot_fraction
        s = L*(1-f)/2. # start of dashpot
        P0 = (B[0], B[1]+s)
        P1 = (B[0], B[1]+L-s)
        P2 = (B[0], B[1]+L)
        shapes['line start'] = Line(B, P0)

        shapes['pot'] = Curve([P1[0]-w, P0[0]-w, P0[0]+w, P1[0]+w],
                              [P1[1], P0[1], P0[1], P1[1]])
        piston_thickness = f*L*Dashpot.piston_thickness_fraction
        if piston_pos is None:
            piston_pos = P0[1] + 1/3.*f*L
            print 'Calculated piston position:', piston_pos, P0[1], 1/3.*f*L
        if piston_pos < P0[1]:
            piston_pos = P0[1]
            print 'too small piston position, <', P0[1]
        if piston_pos > P1[1]-piston_thickness:
            print 'too large piston position, >', P1[1]-piston_thickness
            piston_pos = P1[1]-piston_thickness
        gap = w*Dashpot.piston_gap_fraction
        shapes['piston'] = Compose(
            {'line': Line(P2, (B[0], piston_pos + piston_thickness)),
             'rectangle': Rectangle((B[0] - w+gap, piston_pos),
                                    2*w-2*gap, piston_thickness),
             })
        shapes['piston']['rectangle'].set_filled_curves(pattern='X')

        self.shapes = shapes

# COMPOSITE types:
# MassSpringForce: Line(horizontal), Spring, Rectangle, Arrow/Line(w/arrow)
# must be easy to find the tip of the arrow
# Maybe extra dict: self.name['mass'] = Rectangle object - YES!

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


