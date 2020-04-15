import copy
from abc import ABC, abstractmethod

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
    _drawing_tool: MatplotlibDraw

    @abstractmethod
    def __init__(self, drawing_tool: MatplotlibDraw):
        if MatplotlibDraw is None:
            raise ValueError("drawing_tool cannot be None")
        self._drawing_tool = drawing_tool
        self._shapes = dict()

    @property
    def name(self) -> str:
        if hasattr(self, '_name'):
            return self._name
        else:
            return 'no_name'

    @name.setter
    def name(self, name: str):
        self._name = name

    def __iter__(self):
        # We iterate over self.shapes many places, and will
        # get here if self.shapes is just a Shape object and
        # not the assumed dict/list.
        print('Warning: class %s does not define self.shapes\n' \
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
        if hasattr(self, 'shapes'):
            self._shapes[name] = value
        else:
            raise Exception('Cannot assign')

    def _for_all_shapes(self, func, *args, **kwargs):
        verbose = kwargs.get('verbose', 0)

        is_dict = True if isinstance(self._shapes, dict) else False
        for k, shape in enumerate(self._shapes):
            if is_dict:
                shape_name = shape
                shape = self._shapes[shape]
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
                elif isinstance(shape, (list, tuple)):
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
                         pprint.pformat(self._shapes)))

            if verbose > 0:
                print('calling %s.%s' % (shape_name, func))
            getattr(shape, func)(*args, **kwargs)

    def draw(self, verbose=0):
        self._for_all_shapes('draw', verbose=verbose)
        return self

    def draw_dimensions(self):
        if hasattr(self, 'dimensions'):
            for shape in self.dimensions:
                self.dimensions[shape].draw()
            return self
        else:
            # raise AttributeError('no self.dimensions dict for defining dimensions of class %s' % self.__classname__.__name__)
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
        if not isinstance(self._shapes, dict):
            raise TypeError('recurse works only with dict self.shape, not %s' %
                            type(self._shapes))
        space = ' ' * indent
        print(space, '%s: %s.shapes has entries' % \
              (self.__class__.__name__, name), \
              str(list(self._shapes.keys()))[1:-1])

        for shape in self._shapes:
            print(space, end=' ')
            print('call %s.shapes["%s"].recurse("%s", %d)' % \
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
        if color in self._drawing_tool.line_colors:
            color = self._drawing_tool.line_colors[color]
        elif color in list(drawing_tool.line_colors.values()):
            pass  # color is ok
        else:
            raise ValueError('%s: invalid color "%s", must be in %s' %
                             (self.__class__.__name__ + '.set_linecolor:',
                              color, list(self._drawing_tool.line_colors.keys())))
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
            pass  # color is ok
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
