from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import input
from builtins import zip
from builtins import str
from builtins import range
from builtins import *
from builtins import object
from numpy import linspace, sin, cos, pi, array, asarray, ndarray, sqrt, abs
import pprint, copy, glob, os
from math import radians

from .MatplotlibDraw import MatplotlibDraw
drawing_tool = MatplotlibDraw()

def point(x, y, check_inside=False):
    for obj, name in zip([x, y], ['x', 'y']):
        if isinstance(obj, (float,int)):
            pass
        elif isinstance(obj, ndarray):
            if obj.size == 1:
                pass
            else:
                raise TypeError('%s=%s of type %d has length=%d > 1' %
                                (name, obj, type(obj), obj.size))
        else:
            raise TypeError('%s=%s is of wrong type %d' %
                            (name, obj, type(obj)))
    if check_inside:
        ok, msg = drawing_tool.inside((x,y), exception=True)
        if not ok:
            print(msg)

    return array((x, y), dtype=float)

def distance(p1, p2):
    p1 = arr2D(p1);  p2 = arr2D(p2)
    d = p2 - p1
    return sqrt(d[0]**2 + d[1]**2)

def unit_vec(x, y=None):
    """Return unit vector of the vector (x,y), or just x if x is a 2D point."""
    if isinstance(x, (float,int)) and isinstance(y, (float,int)):
        x = point(x, y)
    elif isinstance(x, (list,tuple,ndarray)) and y is None:
        return arr2D(x)/sqrt(x[0]**2 + x[1]**2)
    else:
        raise TypeError('x=%s is %s, must be float or ndarray 2D point' %
                        (x, type(x)))

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
            print(msg)

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
                raise TypeError('sequence %s is not a sequence but %s; must be %s of length %d' %
                            (str(seq), type(seq),
                            ', '.join([str(t) for t in legal_types]),
                             len(seq)))
            else:
                return False
        else:
            return True
    elif error_message:
        raise TypeError('sequence %s is not a sequence but %s, %s; must be %s' %
                        (str(seq), seq.__class__.__name__, type(seq),
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
                print(msg)


def animate(fig, time_points, action, moviefiles=False,
            pause_per_frame=0.5, show_screen_graphics=True,
            title=None,
            **action_kwargs):
    if moviefiles:
        # Clean up old frame files
        framefilestem = 'tmp_frame_'
        framefiles = glob.glob('%s*.png' % framefilestem)
        for framefile in framefiles:
            os.remove(framefile)

    for n, t in enumerate(time_points):
        drawing_tool.erase()

        action(t, fig, **action_kwargs)
        #could demand returning fig, but in-place modifications
        #are done anyway
        #fig = action(t, fig)
        #if fig is None:
        #    raise TypeError(
        #        'animate: action returns None, not fig\n'
        #        '(a Shape object with the whole figure)')

        fig.draw()
        drawing_tool.display(title=title, show=show_screen_graphics)

        if moviefiles:
            drawing_tool.savefig('%s%04d.png' % (framefilestem, n))

    if moviefiles:
        return '%s%%04d.png' % framefilestem


class Shape(object):
    """
    Superclass for drawing different geometric shapes.
    Subclasses define shapes, but drawing, rotation, translation,
    etc. are done in generic functions in this superclass.
    """
    def __init__(self):
        """
        Never to be called from subclasses.
        """
        raise NotImplementedError(
            'class %s must implement __init__,\nwhich defines '
            'self.shapes as a dict (or list) of Shape objects\n'
            'Do not call Shape.__init__!' % \
            self.__class__.__name__)

    def set_name(self, name):
        self.name = name
        return self

    def get_name(self):
        return self.name if hasattr(self, 'name') else 'no_name'

    def __iter__(self):
        # We iterate over self.shapes many places, and will
        # get here if self.shapes is just a Shape object and
        # not the assumed dict/list.
        print('Warning: class %s does not define self.shapes\n'\
              'as a dict of Shape objects')
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
            raise Exception('This is a bug in __getitem__')

    def __setitem__(self, name, value):
        """
        Allow assignment like::

           obj1['name1']['name2'] = value

        all the way down to ``Curve`` or ``Point`` (``Text``)
        objects.
        """
        if hasattr(self, 'shapes'):
            self.shapes[name] = value
        else:
            raise Exception('Cannot assign')


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
        for k, shape in enumerate(self.shapes):
            if is_dict:
                shape_name = shape
                shape = self.shapes[shape]
            else:
                shape_name = k  # use index as name if list (not dict)

            if not isinstance(shape, Shape):
                if isinstance(shape, dict):
                    raise TypeError(
                        'class %s has a self.shapes member "%s" that is just\n'
                        'a plain dictionary,\n%s\n'
                        'Did you mean to embed this dict in a Composition\n'
                        'object?' % (self.__class__.__name__, shape_name,
                        str(shape)))
                elif isinstance(shape, (list,tuple)):
                    raise TypeError(
                        'class %s has self.shapes member "%s" containing\n'
                        'a %s object %s,\n'
                        'Did you mean to embed this list in a Composition\n'
                        'object?' % (self.__class__.__name__, shape_name,
                        type(shape), str(shape)))
                elif shape is None:
                    raise TypeError(
                        'class %s has a self.shapes member "%s" that is None.\n'
                        'Some variable name is wrong, or some function\n'
                        'did not return the right object...' \
                        % (self.__class__.__name__, shape_name))
                else:
                    raise TypeError(
                        'class %s has a self.shapes member "%s" of %s which '
                        'is not a Shape object\n%s' %
                        (self.__class__.__name__, shape_name, type(shape),
                         pprint.pformat(self.shapes)))

            if isinstance(shape, Curve):
                shape.name = shape_name
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

    def deform(self, displacement_function):
        self._for_all_shapes('deform', displacement_function)
        return self

    def minmax_coordinates(self, minmax=None):
        if minmax is None:
            minmax = {'xmin': 1E+20, 'xmax': -1E+20,
                      'ymin': 1E+20, 'ymax': -1E+20}
        self._for_all_shapes('minmax_coordinates', minmax)
        return minmax

    def recurse(self, name, indent=0):
        if not isinstance(self.shapes, dict):
            raise TypeError('recurse works only with dict self.shape, not %s' %
                            type(self.shapes))
        space = ' '*indent
        print(space, '%s: %s.shapes has entries' % \
              (self.__class__.__name__, name), \
              str(list(self.shapes.keys()))[1:-1])

        for shape in self.shapes:
            print(space, end=' ')
            print('call %s.shapes["%s"].recurse("%s", %d)' % \
                  (name, shape, shape, indent+2))
            self.shapes[shape].recurse(shape, indent+2)

    def graphviz_dot(self, name, classname=True):
        if not isinstance(self.shapes, dict):
            raise TypeError('recurse works only with dict self.shape, not %s' %
                            type(self.shapes))
        dotfile = name + '.dot'
        pngfile = name + '.png'
        if classname:
            name = r"%s:\n%s" % (self.__class__.__name__, name)

        couplings = self._object_couplings(name, classname=classname)
        # Insert counter for similar names
        from collections import defaultdict
        count = defaultdict(lambda: 0)
        couplings2 = []
        for i in range(len(couplings)):
            parent, child = couplings[i]
            count[child] += 1
            parent += ' (%d)' % count[parent]
            child += ' (%d)' % count[child]
            couplings2.append((parent, child))
        print('graphviz', couplings, count)
        # Remove counter for names there are only one of
        for i in range(len(couplings)):
            parent2, child2 = couplings2[i]
            parent, child = couplings[i]
            if count[parent] > 1:
                parent = parent2
            if count[child] > 1:
                child = child2
            couplings[i] = (parent, child)
        print(couplings)
        f = open(dotfile, 'w')
        f.write('digraph G {\n')
        for parent, child in couplings:
            f.write('"%s" -> "%s";\n' % (parent, child))
        f.write('}\n')
        f.close()
        print('Run dot -Tpng -o %s %s' % (pngfile, dotfile))

    def _object_couplings(self, parent, couplings=[], classname=True):
        """Find all couplings of parent and child objects in a figure."""
        for shape in self.shapes:
            if classname:
                childname = r"%s:\n%s" % \
                            (self.shapes[shape].__class__.__name__, shape)
            else:
                childname = shape
            couplings.append((parent, childname))
            self.shapes[shape]._object_couplings(childname, couplings,
                                                 classname)
        return couplings


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
        elif color in list(drawing_tool.line_colors.values()):
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
        elif color in list(drawing_tool.line_colors.values()):
            pass # color is ok
        else:
            raise ValueError('%s: invalid color "%s", must be in %s' %
                             (self.__class__.__name__ + '.set_filled_curves:',
                              color, list(drawing_tool.line_colors.keys())))
        self._for_all_shapes('set_filled_curves', color, pattern)
        return self

    def set_shadow(self, pixel_displacement=3):
        self._for_all_shapes('set_shadow', pixel_displacement)
        return self

    def show_hierarchy(self, indent=0, format='std'):
        """Recursive pretty print of hierarchy of objects."""
        if not isinstance(self.shapes, dict):
            print('cannot print hierarchy when %s.shapes is not a dict' % \
                  self.__class__.__name__)
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
            s += '\n%s%s%s %s,' % (
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
        self.shadow = False
        self.name = None  # name of object that this Curve represents

    def inside_plot_area(self, verbose=True):
        """Check that all coordinates are within drawing_tool's area."""
        xmin, xmax = self.x.min(), self.x.max()
        ymin, ymax = self.y.min(), self.y.max()
        t = drawing_tool
        inside = True
        if not hasattr(t, 'xmin'):
            return None  # drawing area is not defined

        if xmin < t.xmin:
            inside = False
            if verbose:
                print('x_min=%g < plot area x_min=%g' % (xmin, t.xmin))
        if xmax > t.xmax:
            inside = False
            if verbose:
                print('x_max=%g > plot area x_max=%g' % (xmax, t.xmax))
        if ymin < t.ymin:
            inside = False
            if verbose:
                print('y_min=%g < plot area y_min=%g' % (ymin, t.ymin))
        if ymax > t.ymax:
            inside = False
            if verbose:
                print('y_max=%g > plot area y_max=%g' % (ymax, t.ymax))
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
            self.arrow, self.fillcolor, self.fillpattern,
            self.shadow, self.name)

    def rotate(self, angle, center):
        """
        Rotate all coordinates: `angle` is measured in degrees and
        (`x`,`y`) is the "origin" of the rotation.
        """
        angle = radians(angle)
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
        space = ' '*indent
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


class Spline(Shape):
    # Note: UnivariateSpline interpolation may not work if
    # the x[i] points are far from uniformly spaced
    def __init__(self, x, y, degree=3, resolution=501):
        from scipy.interpolate import UnivariateSpline
        self.smooth = UnivariateSpline(x, y, s=0, k=degree)
        self.xcoor = linspace(x[0], x[-1], resolution)
        ycoor = self.smooth(self.xcoor)
        self.shapes = {'smooth': Curve(self.xcoor, ycoor)}

    def geometric_features(self):
        s = self.shapes['smooth']
        return {'start': point(s.x[0], s.y[0]),
                'end': point(s.x[-1], s.y[-1]),
                'interval': [s.x[0], s.x[-1]]}

    def __call__(self, x):
        return self.smooth(x)

    # Can easily find the derivative and the integral as
    # self.smooth.derivative(n=1) and self.smooth.antiderivative()




class SketchyFunc1(Spline):
    """
    A typical function curve used to illustrate an "arbitrary" function.
    """
    domain = [1, 6]
    def __init__(self, name=None, name_pos='start',
                 xmin=1, xmax=6, ymin=2.4, ymax=5):
        x = array([1, 2,   3,   4, 5,   6])
        y = array([5, 3.5, 3.8, 3, 2.5, 2.4])
        # Scale x and y
        x = xmin - x.min() + x*(xmax - xmin)/(x.max()-x.min())
        y = ymin - y.min() + y*(ymax - ymin)/(y.max()-y.min())

        Spline.__init__(self, x, y)
        self.shapes['smooth'].set_linecolor('black')
        if name is not None:
            self.shapes['name'] = Text(name, self.geometric_features()[name_pos] + point(0,0.1))

class SketchyFunc3(Spline):
    """
    A typical function curve used to illustrate an "arbitrary" function.
    """
    domain = [0, 6]
    def __init__(self, name=None, name_pos='start',
                 xmin=0, xmax=6, ymin=0.5, ymax=3.8):
        x = array([0, 2,   3,   4, 5,   6])
        #y = array([2, 3.5, 3.8, 2, 2.5, 2.6])
        y = array([0.5, 3.5, 3.8, 2, 2.5, 3.5])
        # Scale x and y
        x = xmin - x.min() + x*(xmax - xmin)/(x.max()-x.min())
        y = ymin - y.min() + y*(ymax - ymin)/(y.max()-y.min())

        Spline.__init__(self, x, y)
        self.shapes['smooth'].set_linecolor('black')
        if name is not None:
            self.shapes['name'] = Text(name, self.geometric_features()[name_pos] + point(0,0.1))

class SketchyFunc4(Spline):
    """
    A typical function curve used to illustrate an "arbitrary" function.
    Can be a companion function to SketchyFunc3.
    """
    domain = [1, 6]
    def __init__(self, name=None, name_pos='start',
                 xmin=0, xmax=6, ymin=0.5, ymax=1.8):
        x = array([0, 2,   3,   4, 5,   6])
        y = array([1.5, 1.3, 0.7, 0.5, 0.6, 0.8])
        # Scale x and y
        x = xmin - x.min() + x*(xmax - xmin)/(x.max()-x.min())
        y = ymin - y.min() + y*(ymax - ymin)/(y.max()-y.min())

        Spline.__init__(self, x, y)
        self.shapes['smooth'].set_linecolor('black')
        if name is not None:
            self.shapes['name'] = Text(name, self.geometric_features()[name_pos] + point(0,0.1))

class SketchyFunc2(Shape):
    """
    A typical function curve used to illustrate an "arbitrary" function.
    """
    domain = [0, 2.25]
    def __init__(self, name=None, name_pos='end',
                 xmin=0, xmax=2.25, ymin=0.046679703125, ymax=1.259375):

        a = 0; b = 2.25
        resolution = 100
        x = linspace(a, b, resolution+1)
        f = self  # for calling __call__
        y = f(x)
        # Scale x and y
        x = xmin - x.min() + x*(xmax - xmin)/(x.max()-x.min())
        y = ymin - y.min() + y*(ymax - ymin)/(y.max()-y.min())

        self.shapes = {'smooth': Curve(x, y)}
        self.shapes['smooth'].set_linecolor('black')

        pos = point(a, f(a)) if name_pos == 'start' else point(b, f(b))
        if name is not None:
            self.shapes['name'] = Text(name, pos + point(0,0.1))

    def __call__(self, x):
        return 0.5+x*(2-x)*(0.9-x) # on [0, 2.25]

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

    def deform(self, displacement_function):
        """Displace coordinates according to displacement_function(x,y)."""
        for i in range(len(self.x)):
            self.x, self.y = displacement_function(self.x, self.y)
        return self

    def minmax_coordinates(self, minmax=None):
        if minmax is None:
            minmax = {'xmin': [], 'xmax': [], 'ymin': [], 'ymax': []}
        minmax['xmin'] = min(self.x, minmax['xmin'])
        minmax['xmax'] = max(self.x, minmax['xmax'])
        minmax['ymin'] = min(self.y, minmax['ymin'])
        minmax['ymax'] = max(self.y, minmax['ymax'])
        return minmax

    def recurse(self, name, indent=0):
        space = ' '*indent
        print(space, 'reached "bottom" object %s' % \
              self.__class__.__name__)

    def _object_couplings(self, parent, couplings=[], classname=True):
        return

    # No need for set_linecolor etc since self._for_all_shapes, which
    # is always called for these functions, makes a test and stops
    # calls if self.shapes is missing and the object is Point or Curve

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
    """
    def __init__(self, lower_left_corner, width, height):
        is_sequence(lower_left_corner)
        p = arr2D(lower_left_corner)  # short form
        x = [p[0], p[0] + width,
             p[0] + width, p[0], p[0]]
        y = [p[1], p[1], p[1] + height,
             p[1] + height, p[1]]
        self.shapes = {'rectangle': Curve(x,y)}

        # Dimensions
        dims = {
            'width': Distance_wText(p + point(0, -height/5.),
                                    p + point(width, -height/5.),
                                    'width'),
            'height': Distance_wText(p + point(width + width/5., 0),
                                     p + point(width + width/5., height),
                                   'height'),
            'lower_left_corner': Text_wArrow('lower_left_corner',
                                             p - point(width/5., height/5.), p)
            }
        self.dimensions = dims

    def geometric_features(self):
        """
        Return dictionary with

        ==================== =============================================
        Attribute            Description
        ==================== =============================================
        lower_left           Lower left corner point.
        upper_left           Upper left corner point.
        lower_right          Lower right corner point.
        upper_right          Upper right corner point.
        lower_mid            Middle point on lower side.
        upper_mid            Middle point on upper side.
        center               Center point
        ==================== =============================================
        """
        r = self.shapes['rectangle']
        d = {'lower_left': point(r.x[0], r.y[0]),
             'lower_right': point(r.x[1], r.y[1]),
             'upper_right': point(r.x[2], r.y[2]),
             'upper_left': point(r.x[3], r.y[3])}
        d['lower_mid'] = 0.5*(d['lower_left'] + d['lower_right'])
        d['upper_mid'] = 0.5*(d['upper_left'] + d['upper_right'])
        d['left_mid'] = 0.5*(d['lower_left'] + d['upper_left'])
        d['right_mid'] = 0.5*(d['lower_right'] + d['upper_right'])
        d['center'] = point(d['lower_mid'][0], d['left_mid'][1])
        return d

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

        # Dimensions
        self.dimensions = {'p1': Text('p1', p1),
                           'p2': Text('p2', p2),
                           'p3': Text('p3', p3)}

    def geometric_features(self):
        t = self.shapes['triangle']
        return {'p1': point(t.x[0], t.y[0]),
                'p2': point(t.x[1], t.y[1]),
                'p3': point(t.x[2], t.y[2])}

class Line(Shape):
    def __init__(self, start, end):
        is_sequence(start, end, length=2)
        x = [start[0], end[0]]
        y = [start[1], end[1]]
        self.shapes = {'line': Curve(x, y)}

    def geometric_features(self):
        line = self.shapes['line']
        return {'start': point(line.x[0], line.y[0]),
                'end': point(line.x[1], line.y[1]),}

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

    def new_interval(self, x=None, y=None):
        """Redefine current Line to cover interval in x or y."""
        if x is not None:
            is_sequence(x, length=2)
            xL, xR = x
            new_line = Line((xL, self(x=xL)), (xR, self(x=xR)))
        elif y is not None:
            is_sequence(y, length=2)
            yL, yR = y
            new_line = Line((xL, self(y=xL)), (xR, self(y=xR)))
        self.shapes['line'] = new_line['line']
        return self


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

        # Must record some parameters for __call__
        self.center = arr2D(center)
        self.radius = radius
        self.start_angle = radians(start_angle)
        self.arc_angle = radians(arc_angle)

        t = linspace(self.start_angle,
                     self.start_angle + self.arc_angle,
                     resolution+1)
        x0 = center[0];  y0 = center[1]
        R = radius
        x = x0 + R*cos(t)
        y = y0 + R*sin(t)
        self.shapes = {'arc': Curve(x, y)}

        # Cannot set dimensions (Arc_wText recurses into this
        # constructor forever). Set in test_Arc instead.

    def geometric_features(self):
        a = self.shapes['arc']
        m = len(a.x)//2  # mid point in array
        d = {'start': point(a.x[0], a.y[0]),
             'end': point(a.x[-1], a.y[-1]),
             'mid': point(a.x[m], a.y[m])}
        return d

    def __call__(self, theta):
        """
        Return (x,y) point at start_angle + theta.
        Not valid after translation, rotation, or scaling.
        """
        theta = radians(theta)
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
    def __init__(self, x, y, thickness, pattern='/', transparent=False):
        is_sequence(x, y, length=len(x))
        if isinstance(x[0], (tuple,list,ndarray)):
            # x is list of curves
            x1 = concatenate(x)
        else:
            x1 = asarray(x, float)
        if isinstance(y[0], (tuple,list,ndarray)):
            # x is list of curves
            y1 = concatenate(y)
        else:
            y1 = asarray(y, float)
        self.x1 = x1;  self.y1 = y1

        # Displaced curve (according to thickness)
        x2 = x1
        y2 = y1 + thickness
        # Combine x1,y1 with x2,y2 reversed
        from numpy import concatenate
        x = concatenate((x1, x2[-1::-1]))
        y = concatenate((y1, y2[-1::-1]))
        wall = Curve(x, y)
        wall.set_filled_curves(color='white', pattern=pattern)
        x = [x1[-1]] + x2[-1::-1].tolist() + [x1[0]]
        y = [y1[-1]] + y2[-1::-1].tolist() + [y1[0]]
        self.shapes = {'wall': wall}

        from collections import OrderedDict
        self.shapes = OrderedDict()
        self.shapes['wall'] = wall
        if transparent:
            white_eraser = Curve(x, y)
            white_eraser.set_linecolor('white')
            self.shapes['eraser'] = white_eraser

    def geometric_features(self):
        d = {'start': point(self.x1[0], self.y1[0]),
             'end': point(self.x1[-1], self.y1[-1])}
        return d

class Wall2(Shape):
    def __init__(self, x, y, thickness, pattern='/'):
        is_sequence(x, y, length=len(x))
        if isinstance(x[0], (tuple,list,ndarray)):
            # x is list of curves
            x1 = concatenate(x)
        else:
            x1 = asarray(x, float)
        if isinstance(y[0], (tuple,list,ndarray)):
            # x is list of curves
            y1 = concatenate(y)
        else:
            y1 = asarray(y, float)

        self.x1 = x1;  self.y1 = y1

        # Displaced curve (according to thickness)
        x2 = x1.copy()
        y2 = y1.copy()

        def displace(idx, idx_m, idx_p):
            # Find tangent and normal
            tangent = point(x1[idx_m], y1[idx_m]) - point(x1[idx_p], y1[idx_p])
            tangent = unit_vec(tangent)
            normal = point(tangent[1], -tangent[0])
            # Displace length "thickness" in "positive" normal direction
            displaced_pt = point(x1[idx], y1[idx]) + thickness*normal
            x2[idx], y2[idx] = displaced_pt

        for i in range(1, len(x1)-1):
            displace(i-1, i+1, i)  # centered difference for normal comp.
        # One-sided differences at the end points
        i = 0
        displace(i, i+1, i)
        i = len(x1)-1
        displace(i-1, i, i)

        # Combine x1,y1 with x2,y2 reversed
        from numpy import concatenate
        x = concatenate((x1, x2[-1::-1]))
        y = concatenate((y1, y2[-1::-1]))
        wall = Curve(x, y)
        wall.set_filled_curves(color='white', pattern=pattern)
        x = [x1[-1]] + x2[-1::-1].tolist() + [x1[0]]
        y = [y1[-1]] + y2[-1::-1].tolist() + [y1[0]]
        self.shapes['wall'] = wall

    def geometric_features(self):
        d = {'start': point(self.x1[0], self.y1[0]),
             'end': point(self.x1[-1], self.y1[-1])}
        return d


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
            y = start[1] + i*dy
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
            y = start[1] + i*dy
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
        # Note:
        self.shapes = {'arrow': arrow}

    def geometric_features(self):
        return self.shapes['arrow'].geometric_features()

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
        head_degrees = radians(30)
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

    def geometric_features(self):
        return self.shapes['line'].geometric_features()


class Text(Point):
    """
    Place `text` at the (x,y) point `position`, with the given
    fontsize (0 indicates that the default fontsize set in drawing_tool
    is to be used). The text is centered around `position` if `alignment` is
    'center'; if 'left', the text starts at `position`, and if
    'right', the right and of the text is located at `position`.
    """
    def __init__(self, text, position, alignment='center', fontsize=0):
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
        return repr(str(self))


class Text_wArrow(Text):
    """
    As class Text, but an arrow is drawn from the mid part of the text
    to some point `arrow_tip`.
    """
    def __init__(self, text, position, arrow_tip,
                 alignment='center', fontsize=0):
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
        return repr(str(self))


class Axis(Shape):
    def __init__(self, start, length, label,
                 rotation_angle=0, fontsize=0,
                 label_spacing=1./45, label_alignment='left'):
        """
        Draw axis from start with `length` to the right
        (x axis). Place label at the end of the arrow tip.
        Then return `rotation_angle` (in degrees).
        The `label_spacing` denotes the space between the label
        and the arrow tip as a fraction of the length of the plot
        in x direction. A tuple can be given to adjust the position
        in both the x and y directions (with one parameter, the
        x position is adjusted).
        With `label_alignment` one can place
        the axis label text such that the arrow tip is to the 'left',
        'right', or 'center' with respect to the text field.
        The `label_spacing` and `label_alignment`parameters can
        be used to fine-tune the location of the label.
        """
        # Arrow is vertical arrow, make it horizontal
        arrow = Arrow3(start, length, rotation_angle=-90)
        arrow.rotate(rotation_angle, start)
        if isinstance(label_spacing, (list,tuple)) and len(label_spacing) == 2:
            x_spacing = drawing_tool.xrange*label_spacing[0]
            y_spacing = drawing_tool.yrange*label_spacing[1]
        elif isinstance(label_spacing, (int,float)):
            # just x spacing
            x_spacing = drawing_tool.xrange*label_spacing
            y_spacing = 0
        # should increase spacing for downward pointing axis
        label_pos = [start[0] + length + x_spacing, start[1] + y_spacing]
        label = Text(label, position=label_pos, fontsize=fontsize)
        label.rotate(rotation_angle, start)
        self.shapes = {'arrow': arrow, 'label': label}

    def geometric_features(self):
        return self.shapes['arrow'].geometric_features()

# Maybe Axis3 with label below/above?

class Force(Arrow1):
    """
    Indication of a force by an arrow and a text (symbol).  Draw an
    arrow, starting at `start` and with the tip at `end`.  The symbol
    is placed at `text_pos`, which can be 'start', 'end' or the
    coordinates of a point. If 'end' or 'start', the text is placed at
    a distance `text_spacing` times the width of the total plotting
    area away from the specified point.
    """
    def __init__(self, start, end, text, text_spacing=1./60,
                 fontsize=0, text_pos='start', text_alignment='center'):
        Arrow1.__init__(self, start, end, style='->')
        if isinstance(text_spacing, (tuple,list)):
            if len(text_spacing) == 2:
                spacing = point(drawing_tool.xrange*text_spacing[0],
                                drawing_tool.xrange*text_spacing[1])
            else:
                spacing = drawing_tool.xrange*text_spacing[0]
        else:
            # just a number, this is x spacing
            spacing = drawing_tool.xrange*text_spacing
        start, end = arr2D(start), arr2D(end)

        # Two cases: label at bottom of line or top, need more
        # spacing if bottom
        downward = (end-start)[1] < 0
        upward = not downward  # for easy code reading

        if isinstance(text_pos, str):
            if text_pos == 'start':
                spacing_dir = unit_vec(start - end)
                if upward:
                    spacing *= 1.7
                if isinstance(spacing, (int, float)):
                    text_pos = start + spacing*spacing_dir
                else:
                    text_pos = start + spacing
            elif text_pos == 'end':
                spacing_dir = unit_vec(end - start)
                if downward:
                    spacing *= 1.7
                if isinstance(spacing, (int, float)):
                    text_pos = end + spacing*spacing_dir
                else:
                    text_pos = end + spacing
        self.shapes['text'] = Text(text, text_pos, fontsize=fontsize,
                                   alignment=text_alignment)

    def geometric_features(self):
        d = Arrow1.geometric_features(self)
        d['symbol_location'] = self.shapes['text'].position
        return d

class Axis2(Force):
    def __init__(self, start, length, label,
                 rotation_angle=0, fontsize=0,
                 label_spacing=1./45, label_alignment='left'):
        direction = point(cos(radians(rotation_angle)),
                          sin(radians(rotation_angle)))
        Force.__init__(start=start, end=length*direction, text=label,
                       text_spacing=label_spacing,
                       fontsize=fontsize, text_pos='end',
                       text_alignment=label_alignment)
        # Substitute text by label for axis
        self.shapes['label'] = self.shapes['text']
        del self.shapes['text']

    # geometric features from Force is ok

class Gravity(Axis):
    """Downward-pointing gravity arrow with the symbol g."""
    def __init__(self, start, length, fontsize=0):
        Axis.__init__(self, start, length, '$g$', below=False,
                      rotation_angle=-90, label_spacing=1./30,
                      fontsize=fontsize)
        self.shapes['arrow'].set_linecolor('black')


class Gravity(Force):
    """Downward-pointing gravity arrow with the symbol g."""
    def __init__(self, start, length, text='$g$', fontsize=0):
        Force.__init__(self, start, (start[0], start[1]-length),
                       text, text_spacing=1./60,
                       fontsize=0, text_pos='end')
        self.shapes['arrow'].set_linecolor('black')


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
    def __init__(self, start, end, text, fontsize=0, text_spacing=1/60.,
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
        normal = unit_vec([tangent[1], -tangent[0]])
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

    def geometric_features(self):
        d = self.shapes['arrow'].geometric_features()
        d['text_position'] = self.shapes['text'].position
        return d

class Arc_wText(Shape):
    def __init__(self, text, center, radius,
                 start_angle, arc_angle, fontsize=0,
                 resolution=180, text_spacing=1/60.):
        arc = Arc(center, radius, start_angle, arc_angle,
                  resolution)
        mid = arr2D(arc(arc_angle/2.))
        normal = unit_vec(mid - arr2D(center))
        text_pos = mid + normal*drawing_tool.xrange*text_spacing
        self.shapes = {'arc': arc,
                       'text': Text(text, text_pos, fontsize=fontsize)}

class Composition(Shape):
    def __init__(self, shapes):
        """shapes: list or dict of Shape objects."""
        if isinstance(shapes, (tuple,list)):
            # Convert to dict using the type of the list element as key
            # (add a counter to make the keys unique)
            shapes = {s.__class__.__name__ + '_' + str(i): s
                      for i, s in enumerate(shapes)}
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
    def geometric_features(self):
        t = self.shapes['triangle']
        r = self.shapes['rectangle']
        d = {'pos': t.geometric_features()['p2'],
             'mid_support': r.geometric_features()['lower_mid']}
        return d


class ConstantBeamLoad(Shape):
    """
    Downward-pointing arrows indicating a vertical load.
    The arrows are of equal length and filling a rectangle
    specified as in the :class:`Rectangle` class.

    Recorded geometric features:

    ==================== =============================================
    Attribute            Description
    ==================== =============================================
    mid_top              Middle point at the top of the row of
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

    def geometric_features(self):
        return {'mid_top': self.shapes['box'].geometric_features()['upper_mid']}


class Moment(Arc_wText):
    def __init__(self, text, center, radius,
                 left=True, counter_clockwise=True,
                 fontsize=0, text_spacing=1/60.):
        style = '->' if counter_clockwise else '<-'
        start_angle = 90 if left else -90
        Arc_wText.__init__(self, text, center, radius,
                           start_angle=start_angle,
                           arc_angle=180, fontsize=fontsize,
                           text_spacing=text_spacing,
                           resolution=180)
        self.shapes['arc']['arc'].set_arrow(style)  # Curve object


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
                       'spokes': Composition(
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




class Spring(Shape):
    """
    Specify a *vertical* spring, starting at `start` and with `length`
    as total vertical length. In the middle of the spring there are
    `num_windings` circular windings to illustrate the spring. If
    `teeth` is true, the spring windings look like saw teeth,
    otherwise the windings are smooth circles.  The parameters `width`
    (total width of spring) and `bar_length` (length of first and last
    bar are given sensible default values if they are not specified
    (these parameters can later be extracted as attributes, see table
    below).
    """
    spring_fraction = 1./2  # fraction of total length occupied by spring

    def __init__(self, start, length, width=None, bar_length=None,
                 num_windings=11, teeth=False):
        B = start
        n = num_windings - 1  # n counts teeth intervals
        if n <= 6:
            n = 7
        # n must be odd:
        if n % 2 == 0:
            n = n+1
        L = length
        if width is None:
            w = L/10.
        else:
            w = width/2.0
        s = bar_length

        # [0, x, L-x, L], f = (L-2*x)/L
        # x = L*(1-f)/2.

        # B: start point
        # w: half-width
        # L: total length
        # s: length of first bar
        # P0: start of dashpot (B[0]+s)
        # P1: end of dashpot
        # P2: end point

        shapes = {}
        if s is None:
            f = Spring.spring_fraction
            s = L*(1-f)/2. # start of spring

        self.bar_length = s  # record
        self.width = 2*w

        P0 = (B[0], B[1] + s)
        P1 = (B[0], B[1] + L-s)
        P2 = (B[0], B[1] + L)

        if s >= L:
            raise ValueError('length of first bar: %g is larger than total length: %g' % (s, L))

        shapes['bar1'] = Line(B, P0)
        spring_length = L - 2*s
        t = spring_length/n  # height increment per winding
        if teeth:
            resolution = 4
        else:
            resolution = 90
        q = linspace(0, n, n*resolution + 1)
        x = P0[0] + w*sin(2*pi*q)
        y = P0[1] + q*t
        shapes['spiral'] = Curve(x, y)
        shapes['bar2'] = Line(P1,P2)
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
        blength1 = Distance_wText((B[0]-2*w, B[1]), (B[0]-2*w, P0[1]),
                                       'bar_length',
                                       text_pos=(P0[0]-7*w, P0[1]+w))
        blength2 = Distance_wText((P1[0]-2*w, P1[1]), (P2[0]-2*w, P2[1]),
                                       'bar_length',
                                       text_pos=(P2[0]-7*w, P2[1]+w))
        dims = {'start': start, 'width': width, 'length': length,
                'num_windings': num_windings, 'bar_length1': blength1,
                'bar_length2': blength2}
        self.dimensions = dims

    def geometric_features(self):
        """
        Recorded geometric features:

        ==================== =============================================
        Attribute            Description
        ==================== =============================================
        start                Start point of spring.
        end                  End point of spring.
        width                Total width of spring.
        bar_length           Length of first (and last) bar part.
        ==================== =============================================
        """
        b1 = self.shapes['bar1']
        d = {'start': b1.geometric_features()['start'],
             'end': self.shapes['bar2'].geometric_features()['end'],
             'bar_length': self.bar_length,
             'width': self.width}
        return d


class Dashpot(Shape):
    """
    Specify a vertical dashpot of height `total_length` and `start` as
    bottom/starting point. The first bar part has length `bar_length`.
    Then comes the dashpot as a rectangular construction of total
    width `width` and height `dashpot_length`. The position of the
    piston inside the rectangular dashpot area is given by
    `piston_pos`, which is the distance between the first bar (given
    by `bar_length`) to the piston.

    If some of `dashpot_length`, `bar_length`, `width` or `piston_pos`
    are not given, suitable default values are calculated. Their
    values can be extracted as keys in the dict returned from
    ``geometric_features``.

    """
    dashpot_fraction = 1./2            # fraction of total_length
    piston_gap_fraction = 1./6         # fraction of width
    piston_thickness_fraction = 1./8   # fraction of dashplot_length

    def __init__(self, start, total_length, bar_length=None,
                 width=None, dashpot_length=None, piston_pos=None):
        B = start
        L = total_length
        if width is None:
            w = L/10.    # total width 1/5 of length
        else:
            w = width/2.0
        s = bar_length

        # [0, x, L-x, L], f = (L-2*x)/L
        # x = L*(1-f)/2.

        # B: start point
        # w: half-width
        # L: total length
        # s: length of first bar
        # P0: start of dashpot (B[0]+s)
        # P1: end of dashpot
        # P2: end point

        shapes = {}
        # dashpot is P0-P1 in y and width 2*w
        if dashpot_length is None:
            if s is None:
                f = Dashpot.dashpot_fraction
                s = L*(1-f)/2. # default
            P1 = (B[0], B[1]+L-s)
            dashpot_length = f*L
        else:
            if s is None:
                f = 1./2  # the bar lengths are taken as f*dashpot_length
                s = f*dashpot_length # default
            P1 = (B[0], B[1]+s+dashpot_length)
        P0 = (B[0], B[1]+s)
        P2 = (B[0], B[1]+L)

        if P2[1] > P1[1] > P0[1]:
            pass # ok
        else:
            raise ValueError('Dashpot has inconsistent dimensions! start: %g, dashpot begin: %g, dashpot end: %g, very end: %g' % (B[1], P0[1], P1[1], P2[1]))

        shapes['line start'] = Line(B, P0)

        shapes['pot'] = Curve([P1[0]-w, P0[0]-w, P0[0]+w, P1[0]+w],
                              [P1[1], P0[1], P0[1], P1[1]])
        piston_thickness = dashpot_length*Dashpot.piston_thickness_fraction
        if piston_pos is None:
            piston_pos = 1/3.*dashpot_length
        if piston_pos < 0:
            piston_pos = 0
        elif piston_pos > dashpot_length:
            piston_pos = dashpot_length - piston_thickness

        abs_piston_pos = P0[1] + piston_pos

        gap = w*Dashpot.piston_gap_fraction
        shapes['piston'] = Composition(
            {'line': Line(P2, (B[0], abs_piston_pos + piston_thickness)),
             'rectangle': Rectangle((B[0] - w+gap, abs_piston_pos),
                                    2*w-2*gap, piston_thickness),
             })
        shapes['piston']['rectangle'].set_filled_curves(pattern='X')

        self.shapes = shapes

        self.bar_length = s
        self.width = 2*w
        self.piston_pos = piston_pos
        self.dashpot_length = dashpot_length

        # Dimensions
        start = Text_wArrow('start', (B[0]-1.5*w,B[1]-1.5*w), B)
        width = Distance_wText((B[0]-w, B[1]-3.5*w), (B[0]+w, B[1]-3.5*w),
                               'width')
        dplength = Distance_wText((B[0]+2*w, P0[1]), (B[0]+2*w, P1[1]),
                                  'dashpot_length', text_pos=(B[0]+w,B[1]-w))
        blength = Distance_wText((B[0]-2*w, B[1]), (B[0]-2*w, P0[1]),
                                 'bar_length', text_pos=(B[0]-6*w,P0[1]-w))
        ppos    = Distance_wText((B[0]-2*w, P0[1]), (B[0]-2*w, P0[1]+piston_pos),
                                 'piston_pos', text_pos=(B[0]-6*w,P0[1]+piston_pos-w))
        tlength = Distance_wText((B[0]+4*w, B[1]), (B[0]+4*w, B[1]+L),
                                 'total_length',
                                 text_pos=(B[0]+4.5*w, B[1]+L-2*w))
        line = Line((B[0]+w, abs_piston_pos), (B[0]+7*w, abs_piston_pos)).set_linestyle('dashed').set_linecolor('black').set_linewidth(1)
        pp = Text('abs_piston_pos', (B[0]+7*w, abs_piston_pos), alignment='left')
        dims = {'start': start, 'width': width, 'dashpot_length': dplength,
                'bar_length': blength, 'total_length': tlength,
                'piston_pos': ppos,}
        #'abs_piston_pos': Composition({'line': line, 'text': pp})}
        self.dimensions = dims

    def geometric_features(self):
        """
        Recorded geometric features:

        ==================== =============================================
        Attribute            Description
        ==================== =============================================
        start                Start point of dashpot.
        end                  End point of dashpot.
        bar_length           Length of first bar (from start to spring).
        dashpot_length       Length of dashpot middle part.
        width                Total width of dashpot.
        piston_pos           Position of piston in dashpot, relative to
                             start[1] + bar_length.
        ==================== =============================================
        """
        d = {'start': self.shapes['line start'].geometric_features()['start'],
             'end': self.shapes['piston']['line'].geometric_features()['start'],
             'bar_length': self.bar_length,
             'piston_pos': self.piston_pos,
             'width': self.width,
             'dashpot_length': self.dashpot_length,
             }
        return d

class Wavy(Shape):
    """
    A wavy graph consisting of a user-given main curve y=f(x) with
    additional sinusoidal waves of given (constant) amplitude,
    but varying wavelength (a characteristic wavelength is specified).
    """
    def __init__(self, main_curve, interval, wavelength_of_perturbations,
                 amplitude_of_perturbations, smoothness):
        """
        ============================ ====================================
        Name                         Description
        ============================ ====================================
        main_curve                   f(x) Python function
        interval                     interval for main_curve
        wavelength_of_perturbations  dominant wavelength perturbed waves
        amplitude_of_perturbations   amplitude of perturbed waves
        smoothness                   in [0, 1]: smooth=0, rough=1
        ============================ ====================================
        """
        xmin, xmax = interval
        L = wavelength_of_perturbations
        k_0 = 2*pi/L    # main frequency of waves
        k_p = k_0*0.5
        k_k = k_0/2*smoothness

        A_0 = amplitude_of_perturbations
        A_p = 0.3*A_0
        A_k = k_0/2

        x = linspace(xmin, xmax, 2001)

        def w(x):
            A = A_0 + A_p*sin(A_k*x)
            k = k_0 + k_p*sin(k_k*x)
            y = main_curve(x) + A*sin(k*x)
            return y

        self.shapes = {'wavy': Curve(x, w(x))}
        # Use closure w to define __call__ - then we do not need
        # to store all the parameters A_0, A_k, etc. as attributes
        self.__call__ = w

class StochasticWavyCurve(object):
    """
    Precomputed stochastic wavy graphs.
    There are three graphs with different look.

Curve 0:
----------------------------------------------------------------------
                                 |
                                 |
                                *|
                               * |
                             *   |
                             *   |
                            *    |
                           *     |
                          *      |
                         *       |
                         *       |
                          *      |
                            *    |
                              *  |
                                 |*
                                 |  *
                                 |    *
                                 |      *
                                 |       *
                                 |         *
                                 |          *
                                 |            *
                                 |            *
                                 |            *
                                 |          *
                                 |          *
                                 |          *
                                 |          *
                                 |         *
                                 |         *
                                 |          *
                                 |          *
                                 |           *
                                 |          *
                                 |          *
                                 |           *
                                 |            *
                                 |             *
                                 |              *
                                 |                *
                                 |                  *
                                 |                     *
                                 |                     *
                                 |                   *
                                 |                  *
                                 |                   *
                                 |                    *
                                 |                     *
                                 |                    *
                                 |                 *
                                 |               *
                                 |            *
                                 |          *
                                 |        *
                                 |       *
                                 |       *
                                 |       *
                                 |       *
                                 |       *
                                 |      *
                                 |      *
                                 |     *
                                 |     *
                                 |     *
                                 |        *
                                 |        *
                                 |         *
                                 |           *
                                 |          *
                                 |       *
                                 |    *
                                 |  *
                                 |*
                                *|
                             *   |
                            *    |
                            *    |
                            *    |
                           *     |
                          *      |
                         *       |
                         *       |
                         *       |
                          *      |
                         *       |
                         *       |
                         *       |
                           *     |
                               * |
                                 |*
                                 |   *
                                 |      *
                                 |        *
                                 |         *
                                 |          *
                                 |             *
                                 |             *
                                 |            *
                                 |             *
                                 |              *
                                 |             *
                                 |          *
                                 |      *
                                 |    *
                                 |  *
                                 |  *
                                 |    *
                                 |       *
                                 |        *
                                 |        *
                                 |     *
                                 |   *
                                 | *
                                 | *
                                 |  *
                                 |    *
                                 |      *
                                 |        *
                                 |          *
                                 |          *
                                 |            *
                                 |              *
                                 |             *
                                 |             *
                                 |            *
                                 |          *
                                 |          *
                                 |        *
                                 |       *
                                 |      *
                                 |   *
                                 |   *
                                 |   *
                                 | *
                                 |
                               * |
                             *   |
                            *    |
                             *   |
                             *   |
                              *  |
                               * |
                               * |
                              *  |
                              *  |
                             *   |
                            *    |
                             *   |
                              *  |
                             *   |
                           *     |
                           *     |
                          *      |
                          *      |
                         *       |
                         *       |
                        *        |
                       *         |
                      *          |
                    *            |
                   *             |
                   *             |
                    *            |
                     *           |
                       *         |
Curve 2:
----------------------------------------------------------------------
                                 |
                                 |
                                 |
                                 |*
                                 |*
                                 |*
                                 |
                                 |
                                *|
                                 |*
                                 |   *
                                 |     *
                                 |       *
                                 |         *
                                 |           *
                                 |            *
                                 |            *
                                 |               *
                                 |                   *
                                 |                         *
                                 |                             *
                                 |                                *
                                 |                                 *
                                 |                                *
                                 |                               *
                                 |                             *
                                 |                             *
                                 |                           *
                                 |                        *
                                 |                     *
                                 |                   *
                                 |                 *
                                 |               *
                                 |              *
                                 |             *
                                 |           *
                                 |            *
                                 |            *
                                 |            *
                                 |            *
                                 |             *
                                 |              *
                                 |            *
                                 |           *
                                 |          *
                                 |          *
                                 |         *
                                 |         *
                                 |         *
                                 |        *
                                 |        *
                                 |       *
                                 |       *
                                 |       *
                                 |       *
                                 |       *
                                 |       *
                                 |      *
                                 |    *
                                 |   *
                                 |  *
                                 |
                              *  |
                          *      |
                        *        |
                     *           |
                  *              |
                *                |
              *                  |
             *                   |
             *                   |
              *                  |
              *                  |
             *                   |
           *                     |
          *                      |
         *                       |
         *                       |
         *                       |
         *                       |
        *                        |
         *                       |
         *                       |
          *                      |
            *                    |
             *                   |
                *                |
                    *            |
                        *        |
                            *    |
                               * |
                                 |
                                 | *
                                 |  *
                                 |  *
                                 |   *
                                 |   *
                                 |  *
                                 |   *
                                 |   *
                                 |  *
                                 |  *
                                 |   *
                                 |    *
                                 |       *
                                 |       *
                                 |      *
                                 |      *
                                 |      *
                                 |      *
                                 |     *
                                 |    *
                                 |   *
                                 | *
                                 |*
                                 |*
                                 |
                                 |
                                 |
                                 |*
                                 | *
                                 | *
                                 |*
                                 |
                                *|
                                 |*
                                 |  *
                                 |   *
                                 |       *
                                 |          *
                                 |            *
                                 |              *
                                 |                *
                                 |                 *
                                 |                 *
                                 |                 *
                                 |                  *
                                 |                  *
                                 |                  *
                                 |                   *
                                 |                  *
                                 |                *
                                 |              *
                                 |               *
                                 |              *
                                 |            *
                                 |          *
                                 |         *
                                 |         *
                                 |          *
                                 |           *
                                 |           *
                                 |            *
                                 |            *
                                 |             *
                                 |             *
                                 |              *
                                 |              *
                                 |               *
                                 |               *
                                 |              *
                                 |              *
                                 |            *
                                 |             *
                                 |             *
Curve 2:
----------------------------------------------------------------------
                                 |
                                 |
                                 |
                                 |
                                 |*
                                 | *
                                 | *
                                 |  *
                                 |  *
                                 |    *
                                 |     *
                                 |       *
                                 |         *
                                 |          *
                                 |          *
                                 |         *
                                 |       *
                                 |      *
                                 |    *
                                 |  *
                                 | *
                                 | *
                                 |   *
                                 |     *
                                 |      *
                                 |      *
                                 |    *
                                 | *
                                 |*
                                 |
                               * |
                               * |
                              *  |
                              *  |
                              *  |
                             *   |
                             *   |
                              *  |
                              *  |
                               * |
                                 |*
                                 |  *
                                 |   *
                                 |   *
                                 |   *
                                 |    *
                                 |       *
                                 |       *
                                 |       *
                                 |      *
                                 |      *
                                 |        *
                                 |        *
                                 |        *
                                 |        *
                                 |       *
                                 |      *
                                 |     *
                                 |   *
                                 | *
                                *|
                              *  |
                            *    |
                          *      |
                        *        |
                        *        |
                        *        |
                        *        |
                        *        |
                         *       |
                         *       |
                         *       |
                        *        |
                        *        |
                         *       |
                           *     |
                              *  |
                                 |
                                 |    *
                                 |      *
                                 |       *
                                 |          *
                                 |           *
                                 |              *
                                 |                *
                                 |                   *
                                 |                    *
                                 |                   *
                                 |                   *
                                 |                  *
                                 |                  *
                                 |                *
                                 |             *
                                 |          *
                                 |       *
                                 |      *
                                 |      *
                                 |      *
                                 |    *
                                 |  *
                                 |*
                                *|
                             *   |
                           *     |
                         *       |
                         *       |
                         *       |
                          *      |
                        *        |
                     *           |
                     *           |
                    *            |
                 *               |
              *                  |
             *                   |
              *                  |
               *                 |
               *                 |
               *                 |
               *                 |
                *                |
                *                |
                 *               |
                   *             |
                     *           |
                      *          |
                     *           |
                     *           |
                   *             |
                   *             |
                    *            |
                      *          |
                         *       |
                          *      |
                            *    |
                            *    |
                          *      |
                        *        |
                      *          |
                      *          |
                     *           |
                  *              |
               *                 |
            *                    |
            *                    |
          *                      |
       *                         |
     *                           |
     *                           |
       *                         |
         *                       |
           *                     |
             *                   |
                 *               |
                    *            |
                       *         |
                            *    |
                                *|
                                 |*
                                 |    *
                                 |        *
                                 |           *
                                 |               *
                                 |                *
                                 |                  *
See also hplgit.github.io/pysketcher/doc/src/tut/fig-tut/StochasticWavyCurve.png (and .pdf)

    """
    # The curves were generated by the script generate_road_profiles.py and
    # the code below were generated by plot_roads.py. Both scripts are
    # found doc/src/src-bumpy in the repo git@github.com:hplgit/bumpy.git

    def __init__(self, curve_no=0, percentage=100):
        """
        =============  ===================================================
        Argument       Explanation
        =============  ===================================================
        curve_no       0, 1, or 2: chooses one out of three shapes.
        percentage     The percentage of the defined curve to be used.
        =============  ===================================================
        """
        self._define_curves()
        self.curve_no = curve_no
        m = int(len(self.x)/float(percentage)*100)

        self.shapes = {'wavy': Curve(self.x[:m], self.y[curve_no][:m])}

    def __call__(self, x):
        raise NotImplementedError

    def _define_curves(self):
        self.x = array([0.0000, 0.0606, 0.1212, 0.1818, 0.2424, 0.3030, 0.3636, 0.4242, 0.4848, 0.5455, 0.6061, 0.6667, 0.7273, 0.7879, 0.8485, 0.9091, 0.9697, 1.0303, 1.0909, 1.1515, 1.2121, 1.2727, 1.3333, 1.3939, 1.4545, 1.5152, 1.5758, 1.6364, 1.6970, 1.7576, 1.8182, 1.8788, 1.9394, 2.0000, 2.0606, 2.1212, 2.1818, 2.2424, 2.3030, 2.3636, 2.4242, 2.4848, 2.5455, 2.6061, 2.6667, 2.7273, 2.7879, 2.8485, 2.9091, 2.9697, 3.0303, 3.0909, 3.1515, 3.2121, 3.2727, 3.3333, 3.3939, 3.4545, 3.5152, 3.5758, 3.6364, 3.6970, 3.7576, 3.8182, 3.8788, 3.9394, 4.0000, 4.0606, 4.1212, 4.1818, 4.2424, 4.3030, 4.3636, 4.4242, 4.4848, 4.5455, 4.6061, 4.6667, 4.7273, 4.7879, 4.8485, 4.9091, 4.9697, 5.0303, 5.0909, 5.1515, 5.2121, 5.2727, 5.3333, 5.3939, 5.4545, 5.5152, 5.5758, 5.6364, 5.6970, 5.7576, 5.8182, 5.8788, 5.9394, 6.0000, 6.0606, 6.1212, 6.1818, 6.2424, 6.3030, 6.3636, 6.4242, 6.4848, 6.5455, 6.6061, 6.6667, 6.7273, 6.7879, 6.8485, 6.9091, 6.9697, 7.0303, 7.0909, 7.1515, 7.2121, 7.2727, 7.3333, 7.3939, 7.4545, 7.5152, 7.5758, 7.6364, 7.6970, 7.7576, 7.8182, 7.8788, 7.9394, 8.0000, 8.0606, 8.1212, 8.1818, 8.2424, 8.3030, 8.3636, 8.4242, 8.4848, 8.5455, 8.6061, 8.6667, 8.7273, 8.7879, 8.8485, 8.9091, 8.9697, 9.0303, 9.0909, 9.1515, 9.2121, 9.2727, 9.3333, 9.3939, 9.4545, 9.5152, 9.5758, 9.6364, 9.6970, 9.7576, 9.8182, 9.8788, 9.9394, 10.0000, 10.0606, 10.1212, 10.1818, 10.2424, 10.3030, 10.3636, 10.4242, 10.4848, 10.5455, 10.6061, 10.6667, 10.7273, 10.7879, 10.8485, 10.9091, 10.9697, 11.0303, 11.0909, 11.1515, 11.2121, 11.2727, 11.3333, 11.3939, 11.4545, 11.5152, 11.5758, 11.6364, 11.6970, 11.7576, 11.8182, 11.8788, 11.9394, 12.0000, 12.0606, 12.1212, 12.1818, 12.2424, 12.3030, 12.3636, 12.4242, 12.4848, 12.5455, 12.6061, 12.6667, 12.7273, 12.7879, 12.8485, 12.9091, 12.9697, 13.0303, 13.0909, 13.1515, 13.2121, 13.2727, 13.3333, 13.3939, 13.4545, 13.5152, 13.5758, 13.6364, 13.6970, 13.7576, 13.8182, 13.8788, 13.9394, 14.0000, 14.0606, 14.1212, 14.1818, 14.2424, 14.3030, 14.3636, 14.4242, 14.4848, 14.5455, 14.6061, 14.6667, 14.7273, 14.7879, 14.8485, 14.9091, 14.9697, 15.0303, 15.0909, 15.1515, 15.2121, 15.2727, 15.3333, 15.3939, 15.4545, 15.5152, 15.5758, 15.6364, 15.6970, 15.7576, 15.8182, 15.8788, 15.9394, 16.0000, 16.0606, 16.1212, 16.1818, 16.2424, 16.3030, 16.3636, 16.4242, 16.4848, 16.5455, 16.6061, 16.6667, 16.7273, 16.7879, 16.8485, 16.9091, 16.9697, 17.0303, 17.0909, 17.1515, 17.2121, 17.2727, 17.3333, 17.3939, 17.4545, 17.5152, 17.5758, 17.6364, 17.6970, 17.7576, 17.8182, 17.8788, 17.9394, 18.0000, 18.0606, 18.1212, 18.1818, 18.2424, 18.3030, 18.3636, 18.4242, 18.4848, 18.5455, 18.6061, 18.6667, 18.7273, 18.7879, 18.8485, 18.9091, 18.9697, 19.0303, 19.0909, 19.1515, 19.2121, 19.2727, 19.3333, 19.3939, 19.4545, 19.5152, 19.5758, 19.6364, 19.6970, 19.7576, 19.8182, 19.8788, 19.9394, 20.0000, 20.0606, 20.1212, 20.1818, 20.2424, 20.3030, 20.3636, 20.4242, 20.4848, 20.5455, 20.6061, 20.6667, 20.7273, 20.7879, 20.8485, 20.9091, 20.9697, 21.0303, 21.0909, 21.1515, 21.2121, 21.2727, 21.3333, 21.3939, 21.4545, 21.5152, 21.5758, 21.6364, 21.6970, 21.7576, 21.8182, 21.8788, 21.9394, 22.0000, 22.0606, 22.1212, 22.1818, 22.2424, 22.3030, 22.3636, 22.4242, 22.4848, 22.5455, 22.6061, 22.6667, 22.7273, 22.7879, 22.8485, 22.9091, 22.9697, 23.0303, 23.0909, 23.1515, 23.2121, 23.2727, 23.3333, 23.3939, 23.4545, 23.5152, 23.5758, 23.6364, 23.6970, 23.7576, 23.8182, 23.8788, 23.9394, 24.0000, 24.0606, 24.1212, 24.1818, 24.2424, 24.3030, 24.3636, 24.4242, 24.4848, 24.5455, 24.6061, 24.6667, 24.7273, 24.7879, 24.8485, 24.9091, 24.9697, 25.0303, 25.0909, 25.1515, 25.2121, 25.2727, 25.3333, 25.3939, 25.4545, 25.5152, 25.5758, 25.6364, 25.6970, 25.7576, 25.8182, 25.8788, 25.9394, 26.0000, 26.0606, 26.1212, 26.1818, 26.2424, 26.3030, 26.3636, 26.4242, 26.4848, 26.5455, 26.6061, 26.6667, 26.7273, 26.7879, 26.8485, 26.9091, 26.9697, 27.0303, 27.0909, 27.1515, 27.2121, 27.2727, 27.3333, 27.3939, 27.4545, 27.5152, 27.5758, 27.6364, 27.6970, 27.7576, 27.8182, 27.8788, 27.9394, 28.0000, 28.0606, 28.1212, 28.1818, 28.2424, 28.3030, 28.3636, 28.4242, 28.4848, 28.5455, 28.6061, 28.6667, 28.7273, 28.7879, 28.8485, 28.9091, 28.9697, 29.0303, 29.0909, 29.1515, 29.2121, 29.2727, 29.3333, 29.3939, 29.4545, 29.5152, 29.5758, 29.6364, 29.6970, 29.7576, 29.8182, 29.8788, 29.9394, 30.0000, 30.0606, 30.1212, 30.1818, 30.2424, 30.3030, 30.3636, 30.4242, 30.4848, 30.5455, 30.6061, 30.6667, 30.7273, 30.7879, 30.8485, 30.9091, 30.9697, 31.0303, 31.0909, 31.1515, 31.2121, 31.2727, 31.3333, 31.3939, 31.4545, 31.5152, 31.5758, 31.6364, 31.6970, 31.7576, 31.8182, 31.8788, 31.9394, 32.0000, 32.0606, 32.1212, 32.1818, 32.2424, 32.3030, 32.3636, 32.4242, 32.4848, 32.5455, 32.6061, 32.6667, 32.7273, 32.7879, 32.8485, 32.9091, 32.9697, 33.0303, 33.0909, 33.1515, 33.2121, 33.2727, 33.3333, 33.3939, 33.4545, 33.5152, 33.5758, 33.6364, 33.6970, 33.7576, 33.8182, 33.8788, 33.9394, 34.0000, 34.0606, 34.1212, 34.1818, 34.2424, 34.3030, 34.3636, 34.4242, 34.4848, 34.5455, 34.6061, 34.6667, 34.7273, 34.7879, 34.8485, 34.9091, 34.9697, 35.0303, 35.0909, 35.1515, 35.2121, 35.2727, 35.3333, 35.3939, 35.4545, 35.5152, 35.5758, 35.6364, 35.6970, 35.7576, 35.8182, 35.8788, 35.9394, 36.0000, 36.0606, 36.1212, 36.1818, 36.2424, 36.3030, 36.3636, 36.4242, 36.4848, 36.5455, 36.6061, 36.6667, 36.7273, 36.7879, 36.8485, 36.9091, 36.9697, 37.0303, 37.0909, 37.1515, 37.2121, 37.2727, 37.3333, 37.3939, 37.4545, 37.5152, 37.5758, 37.6364, 37.6970, 37.7576, 37.8182, 37.8788, 37.9394, 38.0000, 38.0606, 38.1212, 38.1818, 38.2424, 38.3030, 38.3636, 38.4242, 38.4848, 38.5455, 38.6061, 38.6667, 38.7273, 38.7879, 38.8485, 38.9091, 38.9697, 39.0303, 39.0909, 39.1515, 39.2121, 39.2727, 39.3333, 39.3939, 39.4545, 39.5152, 39.5758, 39.6364, 39.6970, 39.7576, 39.8182, 39.8788, 39.9394, 40.0000, 40.0606, 40.1212, 40.1818, 40.2424, 40.3030, 40.3636, 40.4242, 40.4848, 40.5455, 40.6061, 40.6667, 40.7273, 40.7879, 40.8485, 40.9091, 40.9697, 41.0303, 41.0909, 41.1515, 41.2121, 41.2727, 41.3333, 41.3939, 41.4545, 41.5152, 41.5758, 41.6364, 41.6970, 41.7576, 41.8182, 41.8788, 41.9394, 42.0000, 42.0606, 42.1212, 42.1818, 42.2424, 42.3030, 42.3636, 42.4242, 42.4848, 42.5455, 42.6061, 42.6667, 42.7273, 42.7879, 42.8485, 42.9091, 42.9697, 43.0303, 43.0909, 43.1515, 43.2121, 43.2727, 43.3333, 43.3939, 43.4545, 43.5152, 43.5758, 43.6364, 43.6970, 43.7576, 43.8182, 43.8788, 43.9394, 44.0000, 44.0606, 44.1212, 44.1818, 44.2424, 44.3030, 44.3636, 44.4242, 44.4848, 44.5455, 44.6061, 44.6667, 44.7273, 44.7879, 44.8485, 44.9091, 44.9697, 45.0303, 45.0909, 45.1515, 45.2121, 45.2727, 45.3333, 45.3939, 45.4545, 45.5152, 45.5758, 45.6364, 45.6970, 45.7576, 45.8182, 45.8788, 45.9394, 46.0000, 46.0606, 46.1212, 46.1818, 46.2424, 46.3030, 46.3636, 46.4242, 46.4848, 46.5455, 46.6061, 46.6667, 46.7273, 46.7879, 46.8485, 46.9091, 46.9697, 47.0303, 47.0909, 47.1515, 47.2121, 47.2727, 47.3333, 47.3939, 47.4545, 47.5152, 47.5758, 47.6364, 47.6970, 47.7576, 47.8182, 47.8788, 47.9394, 48.0000, 48.0606, 48.1212, 48.1818, 48.2424, 48.3030, 48.3636, 48.4242, 48.4848, 48.5455, 48.6061, 48.6667, 48.7273, 48.7879, 48.8485, 48.9091, 48.9697, 49.0303, 49.0909, 49.1515, 49.2121, 49.2727, 49.3333, 49.3939, 49.4545, 49.5152, 49.5758, 49.6364, 49.6970, 49.7576, 49.8182, 49.8788, 49.9394, ])
        self.y = [None]*3
        self.y[0] = array([0.0000, 0.0005, 0.0006, 0.0004, -0.0004, -0.0007, -0.0022, -0.0027, -0.0036, -0.0042, -0.0050, -0.0049, -0.0060, -0.0072, -0.0085, -0.0092, -0.0104, -0.0116, -0.0133, -0.0148, -0.0160, -0.0177, -0.0186, -0.0191, -0.0192, -0.0187, -0.0187, -0.0187, -0.0192, -0.0198, -0.0201, -0.0208, -0.0216, -0.0227, -0.0242, -0.0260, -0.0277, -0.0299, -0.0319, -0.0328, -0.0333, -0.0338, -0.0347, -0.0360, -0.0363, -0.0365, -0.0370, -0.0373, -0.0364, -0.0355, -0.0343, -0.0329, -0.0317, -0.0312, -0.0309, -0.0306, -0.0301, -0.0290, -0.0275, -0.0259, -0.0238, -0.0222, -0.0200, -0.0176, -0.0154, -0.0130, -0.0108, -0.0081, -0.0046, -0.0001, 0.0035, 0.0061, 0.0083, 0.0105, 0.0130, 0.0156, 0.0170, 0.0181, 0.0196, 0.0212, 0.0231, 0.0247, 0.0262, 0.0277, 0.0293, 0.0309, 0.0325, 0.0336, 0.0348, 0.0360, 0.0378, 0.0401, 0.0423, 0.0443, 0.0457, 0.0473, 0.0488, 0.0500, 0.0511, 0.0518, 0.0528, 0.0534, 0.0547, 0.0561, 0.0577, 0.0585, 0.0594, 0.0606, 0.0611, 0.0614, 0.0617, 0.0612, 0.0607, 0.0608, 0.0603, 0.0599, 0.0588, 0.0577, 0.0557, 0.0543, 0.0532, 0.0520, 0.0505, 0.0496, 0.0499, 0.0490, 0.0489, 0.0496, 0.0504, 0.0504, 0.0509, 0.0512, 0.0512, 0.0504, 0.0499, 0.0498, 0.0493, 0.0491, 0.0483, 0.0478, 0.0474, 0.0468, 0.0462, 0.0460, 0.0462, 0.0467, 0.0472, 0.0476, 0.0483, 0.0491, 0.0502, 0.0510, 0.0504, 0.0503, 0.0514, 0.0527, 0.0538, 0.0547, 0.0554, 0.0561, 0.0561, 0.0558, 0.0548, 0.0540, 0.0531, 0.0524, 0.0516, 0.0513, 0.0511, 0.0520, 0.0519, 0.0513, 0.0512, 0.0525, 0.0535, 0.0545, 0.0552, 0.0566, 0.0577, 0.0591, 0.0602, 0.0605, 0.0609, 0.0615, 0.0627, 0.0638, 0.0644, 0.0652, 0.0661, 0.0670, 0.0678, 0.0692, 0.0706, 0.0729, 0.0757, 0.0786, 0.0805, 0.0825, 0.0846, 0.0870, 0.0897, 0.0921, 0.0947, 0.0968, 0.0997, 0.1018, 0.1027, 0.1025, 0.1018, 0.1004, 0.1000, 0.0994, 0.0980, 0.0972, 0.0960, 0.0941, 0.0927, 0.0916, 0.0902, 0.0896, 0.0890, 0.0892, 0.0896, 0.0908, 0.0919, 0.0922, 0.0937, 0.0948, 0.0957, 0.0960, 0.0961, 0.0963, 0.0965, 0.0970, 0.0983, 0.0994, 0.0997, 0.0993, 0.0984, 0.0965, 0.0951, 0.0934, 0.0916, 0.0897, 0.0870, 0.0840, 0.0813, 0.0791, 0.0766, 0.0751, 0.0730, 0.0707, 0.0683, 0.0644, 0.0616, 0.0592, 0.0562, 0.0545, 0.0531, 0.0519, 0.0504, 0.0490, 0.0468, 0.0451, 0.0432, 0.0414, 0.0403, 0.0394, 0.0386, 0.0380, 0.0370, 0.0364, 0.0367, 0.0374, 0.0385, 0.0390, 0.0390, 0.0381, 0.0380, 0.0377, 0.0381, 0.0380, 0.0377, 0.0374, 0.0376, 0.0378, 0.0380, 0.0382, 0.0385, 0.0381, 0.0377, 0.0373, 0.0367, 0.0365, 0.0358, 0.0351, 0.0342, 0.0336, 0.0334, 0.0326, 0.0322, 0.0329, 0.0327, 0.0321, 0.0310, 0.0297, 0.0293, 0.0290, 0.0283, 0.0279, 0.0272, 0.0271, 0.0271, 0.0279, 0.0282, 0.0302, 0.0325, 0.0351, 0.0375, 0.0393, 0.0406, 0.0416, 0.0422, 0.0428, 0.0430, 0.0434, 0.0443, 0.0447, 0.0457, 0.0465, 0.0479, 0.0494, 0.0514, 0.0527, 0.0539, 0.0557, 0.0571, 0.0572, 0.0563, 0.0539, 0.0504, 0.0469, 0.0441, 0.0412, 0.0385, 0.0359, 0.0334, 0.0308, 0.0282, 0.0260, 0.0232, 0.0211, 0.0196, 0.0180, 0.0169, 0.0154, 0.0137, 0.0121, 0.0105, 0.0088, 0.0067, 0.0044, 0.0027, -0.0000, -0.0024, -0.0048, -0.0066, -0.0082, -0.0111, -0.0136, -0.0158, -0.0179, -0.0201, -0.0218, -0.0235, -0.0242, -0.0245, -0.0236, -0.0231, -0.0237, -0.0237, -0.0233, -0.0229, -0.0233, -0.0239, -0.0241, -0.0244, -0.0247, -0.0251, -0.0259, -0.0270, -0.0288, -0.0295, -0.0305, -0.0311, -0.0322, -0.0327, -0.0343, -0.0352, -0.0361, -0.0358, -0.0362, -0.0365, -0.0365, -0.0358, -0.0353, -0.0348, -0.0355, -0.0365, -0.0373, -0.0373, -0.0375, -0.0365, -0.0345, -0.0327, -0.0322, -0.0327, -0.0335, -0.0337, -0.0337, -0.0348, -0.0359, -0.0361, -0.0364, -0.0371, -0.0366, -0.0361, -0.0358, -0.0353, -0.0348, -0.0345, -0.0335, -0.0320, -0.0300, -0.0281, -0.0257, -0.0233, -0.0208, -0.0179, -0.0146, -0.0104, -0.0062, -0.0031, -0.0007, 0.0023, 0.0049, 0.0077, 0.0099, 0.0125, 0.0147, 0.0177, 0.0202, 0.0232, 0.0264, 0.0291, 0.0322, 0.0346, 0.0365, 0.0386, 0.0403, 0.0415, 0.0425, 0.0428, 0.0436, 0.0447, 0.0457, 0.0465, 0.0475, 0.0494, 0.0516, 0.0534, 0.0555, 0.0574, 0.0591, 0.0616, 0.0638, 0.0655, 0.0660, 0.0657, 0.0656, 0.0650, 0.0647, 0.0637, 0.0623, 0.0613, 0.0611, 0.0611, 0.0618, 0.0633, 0.0652, 0.0665, 0.0677, 0.0690, 0.0700, 0.0712, 0.0713, 0.0710, 0.0709, 0.0695, 0.0675, 0.0655, 0.0626, 0.0598, 0.0566, 0.0533, 0.0501, 0.0470, 0.0437, 0.0405, 0.0372, 0.0342, 0.0323, 0.0305, 0.0289, 0.0267, 0.0250, 0.0229, 0.0204, 0.0183, 0.0164, 0.0152, 0.0148, 0.0141, 0.0135, 0.0139, 0.0148, 0.0160, 0.0179, 0.0193, 0.0210, 0.0234, 0.0266, 0.0291, 0.0314, 0.0337, 0.0358, 0.0375, 0.0395, 0.0412, 0.0417, 0.0424, 0.0428, 0.0428, 0.0418, 0.0415, 0.0398, 0.0373, 0.0347, 0.0328, 0.0318, 0.0301, 0.0284, 0.0258, 0.0240, 0.0214, 0.0188, 0.0168, 0.0148, 0.0137, 0.0122, 0.0109, 0.0101, 0.0093, 0.0093, 0.0096, 0.0089, 0.0104, 0.0123, 0.0141, 0.0150, 0.0159, 0.0165, 0.0174, 0.0185, 0.0205, 0.0225, 0.0247, 0.0269, 0.0290, 0.0308, 0.0331, 0.0357, 0.0379, 0.0392, 0.0405, 0.0423, 0.0440, 0.0465, 0.0484, 0.0503, 0.0506, 0.0506, 0.0504, 0.0504, 0.0513, 0.0521, 0.0537, 0.0555, 0.0577, 0.0595, 0.0619, 0.0636, 0.0654, 0.0666, 0.0674, 0.0672, 0.0667, 0.0664, 0.0660, 0.0648, 0.0645, 0.0642, 0.0645, 0.0651, 0.0653, 0.0643, 0.0629, 0.0621, 0.0607, 0.0597, 0.0585, 0.0574, 0.0553, 0.0539, 0.0525, 0.0516, 0.0508, 0.0505, 0.0500, 0.0500, 0.0490, 0.0475, 0.0464, 0.0452, 0.0440, 0.0427, 0.0416, 0.0403, 0.0393, 0.0377, 0.0360, 0.0349, 0.0343, 0.0332, 0.0325, 0.0313, 0.0305, 0.0287, 0.0263, 0.0237, 0.0211, 0.0194, 0.0182, 0.0180, 0.0184, 0.0186, 0.0186, 0.0192, 0.0198, 0.0203, 0.0200, 0.0196, 0.0177, 0.0156, 0.0130, 0.0110, 0.0087, 0.0064, 0.0049, 0.0029, 0.0011, -0.0016, -0.0042, -0.0064, -0.0080, -0.0100, -0.0118, -0.0133, -0.0147, -0.0160, -0.0170, -0.0176, -0.0188, -0.0206, -0.0209, -0.0201, -0.0200, -0.0198, -0.0191, -0.0181, -0.0170, -0.0165, -0.0161, -0.0159, -0.0157, -0.0156, -0.0156, -0.0150, -0.0137, -0.0131, -0.0128, -0.0129, -0.0124, -0.0119, -0.0106, -0.0096, -0.0086, -0.0084, -0.0075, -0.0069, -0.0070, -0.0075, -0.0092, -0.0109, -0.0124, -0.0137, -0.0140, -0.0146, -0.0146, -0.0144, -0.0144, -0.0155, -0.0160, -0.0167, -0.0174, -0.0187, -0.0198, -0.0208, -0.0217, -0.0226, -0.0229, -0.0226, -0.0219, -0.0194, -0.0173, -0.0155, -0.0143, -0.0129, -0.0120, -0.0126, -0.0137, -0.0148, -0.0153, -0.0166, -0.0182, -0.0197, -0.0216, -0.0230, -0.0244, -0.0255, -0.0270, -0.0275, -0.0280, -0.0277, -0.0276, -0.0272, -0.0272, -0.0276, -0.0284, -0.0292, -0.0300, -0.0299, -0.0305, -0.0315, -0.0316, -0.0313, -0.0320, -0.0324, -0.0326, -0.0339, -0.0354, -0.0368, -0.0376, -0.0379, -0.0381, -0.0377, -0.0373, -0.0374, -0.0380, -0.0382, -0.0394, -0.0402, -0.0415, -0.0429, -0.0439, -0.0442, -0.0455, -0.0472, -0.0487, -0.0504, -0.0515, -0.0537, -0.0555, -0.0570, -0.0583, -0.0589, -0.0601, -0.0606, -0.0614, -0.0617, -0.0621, -0.0620, -0.0614, -0.0616, -0.0618, -0.0620, -0.0622, -0.0628, -0.0623, -0.0617, -0.0602, -0.0590, -0.0584, -0.0577, -0.0572, -0.0555, -0.0536, -0.0511, -0.0488, -0.0468, -0.0448, -0.0427, -0.0401, -0.0378, -0.0358, ])
        self.y[1] = array([0.0000, 0.0002, 0.0002, 0.0001, 0.0001, 0.0003, 0.0008, 0.0009, 0.0009, 0.0015, 0.0019, 0.0027, 0.0033, 0.0037, 0.0041, 0.0052, 0.0055, 0.0050, 0.0048, 0.0054, 0.0054, 0.0059, 0.0061, 0.0060, 0.0054, 0.0050, 0.0047, 0.0042, 0.0033, 0.0031, 0.0027, 0.0021, 0.0015, 0.0008, -0.0002, -0.0011, -0.0015, -0.0015, -0.0021, -0.0025, -0.0027, -0.0013, 0.0005, 0.0030, 0.0049, 0.0074, 0.0099, 0.0119, 0.0142, 0.0166, 0.0186, 0.0205, 0.0229, 0.0247, 0.0266, 0.0286, 0.0307, 0.0327, 0.0346, 0.0368, 0.0379, 0.0393, 0.0409, 0.0434, 0.0457, 0.0478, 0.0499, 0.0520, 0.0534, 0.0544, 0.0561, 0.0576, 0.0587, 0.0593, 0.0597, 0.0599, 0.0594, 0.0588, 0.0588, 0.0595, 0.0609, 0.0628, 0.0651, 0.0673, 0.0693, 0.0721, 0.0760, 0.0798, 0.0837, 0.0881, 0.0931, 0.0977, 0.1023, 0.1076, 0.1127, 0.1175, 0.1223, 0.1264, 0.1302, 0.1333, 0.1373, 0.1408, 0.1441, 0.1472, 0.1497, 0.1516, 0.1523, 0.1527, 0.1532, 0.1537, 0.1542, 0.1549, 0.1551, 0.1543, 0.1536, 0.1532, 0.1524, 0.1512, 0.1497, 0.1484, 0.1473, 0.1460, 0.1445, 0.1429, 0.1411, 0.1398, 0.1395, 0.1395, 0.1388, 0.1386, 0.1380, 0.1369, 0.1355, 0.1341, 0.1319, 0.1293, 0.1266, 0.1240, 0.1215, 0.1189, 0.1160, 0.1135, 0.1111, 0.1079, 0.1049, 0.1016, 0.0995, 0.0972, 0.0948, 0.0927, 0.0914, 0.0904, 0.0892, 0.0878, 0.0862, 0.0848, 0.0829, 0.0809, 0.0792, 0.0776, 0.0760, 0.0754, 0.0740, 0.0724, 0.0700, 0.0680, 0.0668, 0.0658, 0.0655, 0.0653, 0.0648, 0.0636, 0.0613, 0.0589, 0.0573, 0.0559, 0.0552, 0.0558, 0.0571, 0.0587, 0.0602, 0.0608, 0.0613, 0.0607, 0.0601, 0.0595, 0.0595, 0.0590, 0.0591, 0.0598, 0.0603, 0.0603, 0.0610, 0.0610, 0.0607, 0.0603, 0.0601, 0.0607, 0.0608, 0.0616, 0.0627, 0.0640, 0.0653, 0.0662, 0.0669, 0.0673, 0.0667, 0.0654, 0.0646, 0.0635, 0.0624, 0.0604, 0.0583, 0.0562, 0.0547, 0.0537, 0.0524, 0.0522, 0.0516, 0.0515, 0.0518, 0.0515, 0.0504, 0.0501, 0.0501, 0.0501, 0.0498, 0.0494, 0.0489, 0.0485, 0.0483, 0.0484, 0.0477, 0.0472, 0.0468, 0.0471, 0.0463, 0.0461, 0.0460, 0.0466, 0.0461, 0.0454, 0.0448, 0.0445, 0.0439, 0.0437, 0.0439, 0.0438, 0.0430, 0.0423, 0.0418, 0.0415, 0.0409, 0.0400, 0.0386, 0.0376, 0.0370, 0.0357, 0.0351, 0.0354, 0.0356, 0.0356, 0.0362, 0.0366, 0.0380, 0.0385, 0.0378, 0.0381, 0.0390, 0.0390, 0.0388, 0.0386, 0.0379, 0.0366, 0.0362, 0.0364, 0.0365, 0.0363, 0.0363, 0.0359, 0.0354, 0.0348, 0.0354, 0.0350, 0.0337, 0.0314, 0.0282, 0.0258, 0.0240, 0.0230, 0.0227, 0.0227, 0.0221, 0.0214, 0.0201, 0.0188, 0.0179, 0.0173, 0.0165, 0.0155, 0.0133, 0.0109, 0.0082, 0.0052, 0.0028, 0.0003, -0.0026, -0.0062, -0.0095, -0.0120, -0.0151, -0.0180, -0.0209, -0.0233, -0.0262, -0.0293, -0.0316, -0.0337, -0.0361, -0.0385, -0.0419, -0.0445, -0.0470, -0.0494, -0.0515, -0.0534, -0.0561, -0.0590, -0.0619, -0.0643, -0.0666, -0.0688, -0.0710, -0.0733, -0.0753, -0.0774, -0.0795, -0.0822, -0.0837, -0.0851, -0.0865, -0.0876, -0.0892, -0.0892, -0.0893, -0.0896, -0.0901, -0.0905, -0.0909, -0.0909, -0.0901, -0.0890, -0.0884, -0.0880, -0.0873, -0.0871, -0.0872, -0.0860, -0.0858, -0.0863, -0.0865, -0.0864, -0.0865, -0.0871, -0.0887, -0.0904, -0.0924, -0.0941, -0.0962, -0.0980, -0.0999, -0.1014, -0.1021, -0.1029, -0.1037, -0.1041, -0.1052, -0.1056, -0.1065, -0.1070, -0.1075, -0.1073, -0.1079, -0.1080, -0.1078, -0.1075, -0.1074, -0.1078, -0.1082, -0.1087, -0.1083, -0.1079, -0.1087, -0.1096, -0.1101, -0.1105, -0.1114, -0.1121, -0.1127, -0.1135, -0.1137, -0.1133, -0.1131, -0.1126, -0.1115, -0.1109, -0.1099, -0.1097, -0.1092, -0.1081, -0.1066, -0.1057, -0.1050, -0.1047, -0.1040, -0.1030, -0.1018, -0.1004, -0.0988, -0.0972, -0.0955, -0.0946, -0.0938, -0.0925, -0.0905, -0.0886, -0.0864, -0.0838, -0.0805, -0.0776, -0.0748, -0.0720, -0.0686, -0.0655, -0.0621, -0.0588, -0.0555, -0.0520, -0.0477, -0.0434, -0.0389, -0.0353, -0.0323, -0.0287, -0.0247, -0.0211, -0.0179, -0.0149, -0.0123, -0.0094, -0.0065, -0.0042, -0.0020, -0.0001, 0.0016, 0.0028, 0.0044, 0.0072, 0.0097, 0.0109, 0.0120, 0.0127, 0.0135, 0.0140, 0.0151, 0.0147, 0.0158, 0.0161, 0.0162, 0.0154, 0.0154, 0.0162, 0.0172, 0.0186, 0.0204, 0.0214, 0.0213, 0.0210, 0.0211, 0.0208, 0.0204, 0.0202, 0.0201, 0.0187, 0.0179, 0.0167, 0.0164, 0.0167, 0.0170, 0.0180, 0.0188, 0.0199, 0.0204, 0.0213, 0.0209, 0.0203, 0.0198, 0.0186, 0.0183, 0.0181, 0.0168, 0.0163, 0.0161, 0.0160, 0.0154, 0.0157, 0.0162, 0.0166, 0.0171, 0.0171, 0.0179, 0.0186, 0.0196, 0.0205, 0.0229, 0.0254, 0.0280, 0.0305, 0.0327, 0.0343, 0.0354, 0.0361, 0.0367, 0.0363, 0.0361, 0.0355, 0.0353, 0.0351, 0.0342, 0.0335, 0.0328, 0.0326, 0.0324, 0.0325, 0.0330, 0.0333, 0.0333, 0.0327, 0.0326, 0.0328, 0.0326, 0.0327, 0.0329, 0.0328, 0.0332, 0.0331, 0.0325, 0.0315, 0.0311, 0.0305, 0.0302, 0.0300, 0.0289, 0.0275, 0.0260, 0.0246, 0.0234, 0.0230, 0.0216, 0.0211, 0.0205, 0.0191, 0.0172, 0.0147, 0.0131, 0.0112, 0.0094, 0.0082, 0.0062, 0.0045, 0.0041, 0.0035, 0.0037, 0.0035, 0.0033, 0.0033, 0.0037, 0.0034, 0.0036, 0.0033, 0.0028, 0.0021, 0.0015, 0.0008, 0.0004, 0.0002, -0.0002, -0.0008, -0.0001, 0.0007, 0.0015, 0.0020, 0.0020, 0.0028, 0.0037, 0.0045, 0.0052, 0.0060, 0.0063, 0.0074, 0.0083, 0.0092, 0.0095, 0.0095, 0.0096, 0.0093, 0.0100, 0.0097, 0.0093, 0.0084, 0.0071, 0.0050, 0.0044, 0.0031, 0.0017, 0.0005, -0.0004, -0.0018, -0.0026, -0.0026, -0.0020, -0.0018, -0.0010, 0.0003, 0.0024, 0.0046, 0.0066, 0.0090, 0.0110, 0.0126, 0.0143, 0.0157, 0.0167, 0.0171, 0.0179, 0.0195, 0.0223, 0.0254, 0.0287, 0.0320, 0.0359, 0.0400, 0.0439, 0.0470, 0.0491, 0.0515, 0.0535, 0.0563, 0.0585, 0.0605, 0.0620, 0.0635, 0.0654, 0.0670, 0.0687, 0.0701, 0.0728, 0.0746, 0.0766, 0.0785, 0.0800, 0.0812, 0.0817, 0.0822, 0.0820, 0.0814, 0.0814, 0.0817, 0.0820, 0.0823, 0.0826, 0.0826, 0.0831, 0.0833, 0.0846, 0.0851, 0.0853, 0.0855, 0.0858, 0.0859, 0.0864, 0.0868, 0.0876, 0.0884, 0.0890, 0.0894, 0.0895, 0.0888, 0.0882, 0.0883, 0.0884, 0.0892, 0.0903, 0.0915, 0.0917, 0.0916, 0.0908, 0.0900, 0.0891, 0.0881, 0.0869, 0.0849, 0.0825, 0.0805, 0.0789, 0.0773, 0.0761, 0.0750, 0.0738, 0.0729, 0.0717, 0.0712, 0.0714, 0.0718, 0.0727, 0.0737, 0.0735, 0.0733, 0.0723, 0.0706, 0.0683, 0.0666, 0.0651, 0.0636, 0.0620, 0.0599, 0.0580, 0.0563, 0.0551, 0.0540, 0.0526, 0.0516, 0.0503, 0.0492, 0.0482, 0.0469, 0.0468, 0.0471, 0.0471, 0.0471, 0.0483, 0.0490, 0.0486, 0.0489, 0.0495, 0.0510, 0.0523, 0.0538, 0.0547, 0.0552, 0.0556, 0.0569, 0.0573, 0.0578, 0.0583, 0.0579, 0.0579, 0.0580, 0.0583, 0.0585, 0.0594, 0.0601, 0.0598, 0.0594, 0.0597, 0.0602, 0.0611, 0.0612, 0.0618, 0.0620, 0.0626, 0.0635, 0.0637, 0.0645, 0.0649, 0.0657, 0.0667, 0.0680, 0.0688, 0.0693, 0.0698, 0.0702, 0.0699, 0.0703, 0.0702, 0.0705, 0.0716, 0.0725, 0.0730, 0.0736, 0.0736, 0.0734, 0.0735, 0.0739, 0.0736, 0.0728, 0.0720, 0.0717, 0.0715, 0.0709, 0.0704, 0.0707, 0.0704, 0.0695, 0.0690, 0.0687, 0.0667, 0.0648, 0.0629, 0.0620, 0.0620, 0.0618, 0.0621, 0.0623, 0.0633, 0.0637, 0.0637, 0.0638, 0.0639, 0.0639, 0.0642, 0.0650, 0.0653, 0.0657, 0.0661, ])
        self.y[2] = array([0.0000, 0.0001, -0.0002, -0.0003, 0.0004, 0.0014, 0.0021, 0.0025, 0.0025, 0.0021, 0.0018, 0.0022, 0.0016, 0.0018, 0.0018, 0.0021, 0.0027, 0.0034, 0.0046, 0.0060, 0.0076, 0.0080, 0.0084, 0.0090, 0.0100, 0.0104, 0.0098, 0.0097, 0.0100, 0.0100, 0.0105, 0.0117, 0.0124, 0.0128, 0.0133, 0.0133, 0.0133, 0.0132, 0.0132, 0.0136, 0.0144, 0.0161, 0.0179, 0.0196, 0.0222, 0.0251, 0.0265, 0.0279, 0.0287, 0.0291, 0.0297, 0.0305, 0.0316, 0.0328, 0.0340, 0.0361, 0.0382, 0.0408, 0.0425, 0.0442, 0.0460, 0.0474, 0.0489, 0.0502, 0.0512, 0.0517, 0.0526, 0.0525, 0.0525, 0.0521, 0.0508, 0.0498, 0.0487, 0.0478, 0.0472, 0.0461, 0.0446, 0.0434, 0.0415, 0.0399, 0.0388, 0.0374, 0.0360, 0.0351, 0.0339, 0.0320, 0.0308, 0.0294, 0.0286, 0.0278, 0.0255, 0.0224, 0.0194, 0.0170, 0.0147, 0.0131, 0.0123, 0.0121, 0.0110, 0.0106, 0.0100, 0.0090, 0.0089, 0.0093, 0.0100, 0.0111, 0.0132, 0.0159, 0.0179, 0.0195, 0.0207, 0.0220, 0.0229, 0.0242, 0.0261, 0.0279, 0.0290, 0.0300, 0.0303, 0.0309, 0.0316, 0.0328, 0.0335, 0.0332, 0.0323, 0.0314, 0.0300, 0.0283, 0.0268, 0.0248, 0.0225, 0.0201, 0.0172, 0.0143, 0.0119, 0.0104, 0.0088, 0.0071, 0.0059, 0.0051, 0.0038, 0.0027, 0.0017, 0.0009, 0.0007, -0.0002, -0.0008, -0.0020, -0.0034, -0.0055, -0.0069, -0.0082, -0.0086, -0.0085, -0.0089, -0.0088, -0.0092, -0.0099, -0.0110, -0.0121, -0.0137, -0.0150, -0.0157, -0.0160, -0.0155, -0.0149, -0.0140, -0.0139, -0.0134, -0.0135, -0.0136, -0.0138, -0.0145, -0.0158, -0.0155, -0.0155, -0.0153, -0.0154, -0.0159, -0.0157, -0.0152, -0.0143, -0.0140, -0.0138, -0.0142, -0.0148, -0.0154, -0.0154, -0.0147, -0.0136, -0.0122, -0.0107, -0.0102, -0.0091, -0.0082, -0.0063, -0.0042, -0.0028, -0.0007, 0.0015, 0.0038, 0.0054, 0.0075, 0.0093, 0.0110, 0.0137, 0.0156, 0.0170, 0.0184, 0.0195, 0.0199, 0.0206, 0.0209, 0.0207, 0.0201, 0.0198, 0.0196, 0.0191, 0.0192, 0.0193, 0.0196, 0.0201, 0.0206, 0.0216, 0.0229, 0.0253, 0.0278, 0.0304, 0.0321, 0.0341, 0.0356, 0.0367, 0.0372, 0.0379, 0.0383, 0.0394, 0.0396, 0.0397, 0.0391, 0.0382, 0.0362, 0.0346, 0.0334, 0.0325, 0.0325, 0.0325, 0.0323, 0.0316, 0.0321, 0.0328, 0.0338, 0.0352, 0.0366, 0.0378, 0.0389, 0.0401, 0.0403, 0.0406, 0.0419, 0.0425, 0.0424, 0.0421, 0.0415, 0.0407, 0.0406, 0.0411, 0.0413, 0.0419, 0.0420, 0.0416, 0.0415, 0.0402, 0.0388, 0.0377, 0.0368, 0.0357, 0.0353, 0.0351, 0.0348, 0.0347, 0.0340, 0.0326, 0.0314, 0.0306, 0.0295, 0.0288, 0.0275, 0.0257, 0.0234, 0.0209, 0.0188, 0.0169, 0.0151, 0.0132, 0.0114, 0.0093, 0.0076, 0.0055, 0.0026, -0.0008, -0.0038, -0.0069, -0.0097, -0.0118, -0.0132, -0.0148, -0.0164, -0.0183, -0.0202, -0.0213, -0.0228, -0.0253, -0.0280, -0.0299, -0.0315, -0.0329, -0.0343, -0.0349, -0.0364, -0.0373, -0.0383, -0.0391, -0.0400, -0.0401, -0.0404, -0.0414, -0.0422, -0.0425, -0.0425, -0.0420, -0.0419, -0.0412, -0.0412, -0.0408, -0.0400, -0.0396, -0.0397, -0.0400, -0.0401, -0.0405, -0.0412, -0.0410, -0.0401, -0.0389, -0.0377, -0.0372, -0.0369, -0.0364, -0.0356, -0.0347, -0.0345, -0.0346, -0.0353, -0.0359, -0.0367, -0.0376, -0.0385, -0.0387, -0.0391, -0.0401, -0.0400, -0.0398, -0.0395, -0.0391, -0.0385, -0.0383, -0.0377, -0.0374, -0.0371, -0.0361, -0.0357, -0.0355, -0.0342, -0.0324, -0.0303, -0.0280, -0.0257, -0.0232, -0.0205, -0.0179, -0.0147, -0.0113, -0.0091, -0.0059, -0.0019, 0.0024, 0.0071, 0.0120, 0.0177, 0.0219, 0.0248, 0.0273, 0.0290, 0.0302, 0.0318, 0.0325, 0.0331, 0.0334, 0.0344, 0.0360, 0.0387, 0.0414, 0.0437, 0.0456, 0.0471, 0.0491, 0.0511, 0.0526, 0.0536, 0.0550, 0.0570, 0.0597, 0.0622, 0.0647, 0.0672, 0.0696, 0.0710, 0.0725, 0.0748, 0.0777, 0.0806, 0.0832, 0.0854, 0.0874, 0.0893, 0.0906, 0.0914, 0.0927, 0.0937, 0.0944, 0.0959, 0.0970, 0.0970, 0.0967, 0.0955, 0.0945, 0.0934, 0.0927, 0.0921, 0.0916, 0.0909, 0.0901, 0.0893, 0.0884, 0.0881, 0.0877, 0.0870, 0.0870, 0.0871, 0.0872, 0.0867, 0.0860, 0.0845, 0.0821, 0.0800, 0.0775, 0.0752, 0.0728, 0.0703, 0.0676, 0.0655, 0.0637, 0.0618, 0.0593, 0.0558, 0.0518, 0.0483, 0.0445, 0.0414, 0.0384, 0.0365, 0.0349, 0.0338, 0.0330, 0.0323, 0.0320, 0.0319, 0.0320, 0.0323, 0.0324, 0.0324, 0.0322, 0.0327, 0.0328, 0.0320, 0.0314, 0.0295, 0.0279, 0.0258, 0.0243, 0.0229, 0.0211, 0.0195, 0.0176, 0.0163, 0.0151, 0.0136, 0.0123, 0.0108, 0.0088, 0.0064, 0.0041, 0.0021, 0.0002, -0.0020, -0.0051, -0.0078, -0.0106, -0.0137, -0.0169, -0.0195, -0.0218, -0.0235, -0.0253, -0.0269, -0.0281, -0.0290, -0.0299, -0.0315, -0.0328, -0.0336, -0.0344, -0.0352, -0.0354, -0.0353, -0.0358, -0.0355, -0.0347, -0.0344, -0.0338, -0.0335, -0.0324, -0.0319, -0.0319, -0.0322, -0.0334, -0.0351, -0.0365, -0.0381, -0.0401, -0.0424, -0.0449, -0.0472, -0.0491, -0.0506, -0.0522, -0.0533, -0.0544, -0.0553, -0.0553, -0.0557, -0.0558, -0.0563, -0.0573, -0.0587, -0.0602, -0.0617, -0.0636, -0.0666, -0.0699, -0.0734, -0.0760, -0.0791, -0.0817, -0.0840, -0.0857, -0.0869, -0.0881, -0.0882, -0.0884, -0.0888, -0.0893, -0.0889, -0.0876, -0.0869, -0.0858, -0.0851, -0.0836, -0.0825, -0.0813, -0.0807, -0.0800, -0.0802, -0.0805, -0.0807, -0.0813, -0.0818, -0.0819, -0.0822, -0.0829, -0.0825, -0.0829, -0.0838, -0.0840, -0.0836, -0.0824, -0.0810, -0.0799, -0.0789, -0.0785, -0.0785, -0.0774, -0.0770, -0.0761, -0.0755, -0.0752, -0.0746, -0.0744, -0.0741, -0.0729, -0.0718, -0.0710, -0.0694, -0.0673, -0.0649, -0.0627, -0.0606, -0.0592, -0.0582, -0.0571, -0.0555, -0.0539, -0.0527, -0.0516, -0.0508, -0.0503, -0.0508, -0.0518, -0.0527, -0.0536, -0.0544, -0.0545, -0.0541, -0.0547, -0.0553, -0.0561, -0.0573, -0.0587, -0.0600, -0.0608, -0.0616, -0.0624, -0.0626, -0.0631, -0.0638, -0.0630, -0.0621, -0.0612, -0.0603, -0.0594, -0.0577, -0.0564, -0.0551, -0.0535, -0.0511, -0.0485, -0.0455, -0.0424, -0.0396, -0.0374, -0.0360, -0.0351, -0.0343, -0.0336, -0.0324, -0.0311, -0.0296, -0.0276, -0.0259, -0.0240, -0.0223, -0.0212, -0.0205, -0.0201, -0.0203, -0.0214, -0.0232, -0.0261, -0.0285, -0.0304, -0.0320, -0.0342, -0.0365, -0.0381, -0.0394, -0.0416, -0.0434, -0.0443, -0.0450, -0.0465, -0.0482, -0.0490, -0.0497, -0.0508, -0.0506, -0.0509, -0.0514, -0.0522, -0.0525, -0.0532, -0.0547, -0.0553, -0.0575, -0.0597, -0.0629, -0.0666, -0.0702, -0.0737, -0.0773, -0.0805, -0.0835, -0.0847, -0.0875, -0.0893, -0.0913, -0.0929, -0.0935, -0.0943, -0.0949, -0.0957, -0.0962, -0.0977, -0.0994, -0.1011, -0.1031, -0.1057, -0.1086, -0.1114, -0.1141, -0.1158, -0.1174, -0.1197, -0.1219, -0.1234, -0.1250, -0.1267, -0.1273, -0.1270, -0.1268, -0.1263, -0.1257, -0.1240, -0.1220, -0.1210, -0.1197, -0.1197, -0.1188, -0.1171, -0.1147, -0.1122, -0.1101, -0.1077, -0.1052, -0.1031, -0.1020, -0.1008, -0.0983, -0.0960, -0.0934, -0.0908, -0.0889, -0.0865, -0.0836, -0.0799, -0.0767, -0.0740, -0.0716, -0.0692, -0.0663, -0.0628, -0.0596, -0.0567, -0.0535, -0.0508, -0.0472, -0.0435, -0.0394, -0.0347, -0.0301, -0.0253, -0.0210, -0.0165, -0.0126, -0.0095, -0.0072, -0.0046, -0.0020, -0.0001, 0.0023, 0.0050, 0.0077, 0.0102, 0.0135, 0.0175, 0.0212, 0.0245, 0.0280, 0.0309, 0.0336, 0.0365, 0.0397, 0.0433, 0.0474, 0.0511, 0.0546, 0.0574, 0.0602, 0.0634, 0.0663, 0.0695, 0.0729, 0.0752, 0.0762, 0.0773, 0.0781, 0.0790, 0.0806, 0.0836, 0.0857, 0.0879, 0.0896, 0.0920, 0.0949, 0.0975, 0.1002, ])

# COMPOSITE types:
# MassSpringForce: Line(horizontal), Spring, Rectangle, Arrow/Line(w/arrow)
# must be easy to find the tip of the arrow
# Maybe extra dict: self.name['mass'] = Rectangle object - YES!


def _test1():
    set_coordinate_system(xmin=0, xmax=10, ymin=0, ymax=10)
    l1 = Line((0,0), (1,1))
    l1.draw()
    eval(input(': '))
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
    eval(input(': '))
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
        print('BIG PROBLEM WITH ANIMATE!!!')
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
    print('converting PNG files to animated GIF:\n', cmd)
    import subprocess
    failure, output = subprocess.getstatusoutput(cmd)
    if failure:  print('Could not run', cmd)


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
        input('Type Return: ')
