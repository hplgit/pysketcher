import copy
from abc import ABC, abstractmethod
from typing import List

from .matplotlibdraw import MatplotlibDraw
from .point import Point


class Shape(ABC):
    """
    Superclass for drawing different geometric shapes.
    Subclasses define shapes, but drawing, rotation, translation,
    etc. are done in generic functions in this superclass.
    """

    _name: str
    _shapes: dict

    @abstractmethod
    def __init__(self, shapes: dict = None):
        self._shapes = dict() if shapes is None else shapes
        self._line_style = None
        self._line_width = None
        self._line_color = None
        self._fill_color = None
        self._fill_pattern = None
        self._arrow = None
        self._shadow = False

    def __iter__(self):
        return [self]

    def copy(self):
        return copy.deepcopy(self)

    def __getitem__(self, name):
        """
        Allow indexing like::

           obj1['name1']['name2']

        all the way down to ``Curve`` or ``Point`` (``Text``)
        objects.
        """
        if hasattr(self, '_shapes'):
            if name in self._shapes:
                return self._shapes[name]
            else:
                for shape in self._shapes:
                    return self._shapes[shape][name]
        else:
            raise Exception('This is a bug in __getitem__')

    def __setitem__(self, name, value):
        """
        Allow assignment like::

           obj1['name1']['name2'] = value

        all the way down to ``Curve`` or ``Point`` (``Text``)
        objects.
        """
        if hasattr(self, '_shapes'):
            self._shapes[name] = value
        else:
            raise Exception('Cannot assign')

    def _for_all_shapes(self, func: str, *args, **kwargs):
        verbose = kwargs.get('verbose', 0)
        for k, shape in enumerate(self._shapes):
            shape_name = shape
            shape = self._shapes[shape]

            if verbose > 0:
                print('calling %s.%s' % (shape_name, func))
            attribute = getattr(shape, func)
            attribute(*args, **kwargs)

    def draw(self, drawing_tool: MatplotlibDraw, verbose=0) -> None:
        self._for_all_shapes('draw', drawing_tool=drawing_tool, verbose=verbose)

    def draw_dimensions(self, drawing_tool: MatplotlibDraw):
        if hasattr(self, 'dimensions'):
            for shape in self.dimensions:
                self.dimensions[shape].draw(drawing_tool)
            return self
        else:
            # raise AttributeError('no self.dimensions dict for defining dimensions of class %s' %
            # self.__classname__.__name__)
            return self

    def animate(self, drawing_tool: MatplotlibDraw, time_points: List[float], action,
                pause_per_frame=0.5, show_screen_graphics=True,
                title=None,
                **action_kwargs):

        for n, t in enumerate(time_points):
            drawing_tool.erase()

            action(t, self, **action_kwargs)
            # could demand returning fig, but in-place modifications
            # are done anyway
            # fig = action(t, fig)
            # if fig is None:
            #    raise TypeError(
            #        'animate: action returns None, not fig\n'
            #        '(a Shape object with the whole figure)')

            self.draw(drawing_tool)
            drawing_tool.display(title=title, show=show_screen_graphics)

    @abstractmethod
    def rotate(self, angle: float, center: Point):
        pass

    def translate(self, vec):
        return self._for_all_shapes('translate', vec)

    def scale(self, factor):
        return self._for_all_shapes('scale', factor)

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
        space = ' ' * indent
        print(space, '%s: %s.shapes has entries' % \
              (self.__class__.__name__, name), \
              str(list(self._shapes.keys()))[1:-1])

        for shape in self._shapes:
            print(space, end=' ')
            print('call %s.shapes["%s"].recurse("%s", %d)' %
                  (name, shape, shape, indent + 2))
            self._shapes[shape].recurse(shape, indent + 2)

    def graphviz_dot(self, name, classname=True):
        if not isinstance(self._shapes, dict):
            raise TypeError('recurse works only with dict self.shape, not %s' %
                            type(self._shapes))
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
        for shape in self._shapes:
            if classname:
                childname = r"%s:\n%s" % \
                            (self._shapes[shape].__class__.__name__, shape)
            else:
                childname = shape
            couplings.append((parent, childname))
            self._shapes[shape]._object_couplings(childname, couplings,
                                                  classname)
        return couplings

    @property
    def name(self) -> str:
        if hasattr(self, '_name'):
            return self._name
        else:
            return 'no_name'

    @name.setter
    def name(self, name: str):
        self._name = name

    def set_name(self, name: str):
        self.name = name
        return self

    @property
    def line_color(self):
        return self._line_color

    @line_color.setter
    def line_color(self, color):
        self._line_color = color
        self._for_all_shapes('set_line_color', color)

    def set_line_color(self, color):
        self.line_color = color
        return self

    @property
    def line_width(self):
        return self._line_width

    @line_width.setter
    def line_width(self, width):
        self._line_width = width
        self._for_all_shapes('set_line_width', width)

    def set_line_width(self, width):
        self.line_width = width
        return self

    @property
    def line_style(self):
        return self._line_style

    @line_style.setter
    def line_style(self, style):
        self._line_style = style
        self._for_all_shapes('set_line_style', style)

    def set_line_style(self, style):
        self.line_style = style
        return self

    @property
    def arrow(self):
        return self._arrow

    @arrow.setter
    def arrow(self, arrow):
        self._arrow = arrow
        self._for_all_shapes('set_arrow', arrow)

    def set_arrow(self, arrow):
        self.arrow = arrow
        return self

    @property
    def fill_pattern(self):
        return self._fill_pattern

    @fill_pattern.setter
    def fill_pattern(self, pattern=''):
        self._fill_pattern = pattern
        self._for_all_shapes('set_fill_pattern', pattern)

    def set_fill_pattern(self, fill_pattern):
        self.fill_pattern = fill_pattern
        return self

    @property
    def fill_color(self):
        return self._fill_color

    @fill_color.setter
    def fill_color(self, color=''):
        self._fill_color = color
        self._for_all_shapes('set_fill_color', color)

    def set_fill_color(self, fill_color):
        self.fill_color = fill_color
        return self

    @property
    def shadow(self):
        return self._shadow

    @shadow.setter
    def shadow(self, shadow=3):
        self._shadow = shadow
        self._for_all_shapes('set_shadow', shadow)

    def set_shadow(self, shadow):
        self.shadow = shadow
        return self

    def show_hierarchy(self, indent=0, format='std'):
        """Recursive pretty print of hierarchy of objects."""
        if not isinstance(self._shapes, dict):
            print('cannot print hierarchy when %s.shapes is not a dict' % \
                  self.__class__.__name__)
        s = ''
        if format == 'dict':
            s += '{'
        for shape in self._shapes:
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
                            self._shapes[shape].__class__.__name__
            s += '\n%s%s%s %s,' % (
                ' ' * indent,
                shape_str,
                class_str,
                self._shapes[shape].show_hierarchy(indent + 4, format))

        if format == 'dict':
            s += '}'
        return s

    def __str__(self):
        """Display hierarchy with minimum information (just object names)."""
        return self.show_hierarchy(format='plain')

    def __repr__(self):
        """Display hierarchy as a dictionary."""
        return self.show_hierarchy(format='dict')
        # return pprint.pformat(self.shapes)


