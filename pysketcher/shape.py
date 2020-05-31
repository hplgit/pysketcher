import copy
from abc import ABC, abstractmethod
from typing import List, Callable

from .drawing_tool import DrawingTool
from .point import Point
from .style import Style


class Shape(ABC):
    """
    Superclass for drawing different geometric shapes.
    Subclasses define shapes, but drawing, rotation, translation,
    etc. are done in generic functions in this superclass.
    """

    _name: str
    _shapes: dict
    _style: Style

    @abstractmethod
    def __init__(self):
        self._shapes = dict()
        self._name = None
        self._style = Style()

    def __iter__(self):
        return [self]

    def copy(self):
        return copy.deepcopy(self)

    def _for_all_shapes(self, func: str, *args, **kwargs):
        verbose = kwargs.get('verbose', 0)
        for k, shape in enumerate(self._shapes):
            shape_name = shape
            shape = self._shapes[shape]

            if verbose > 0:
                print('calling %s.%s' % (shape_name, func))
            attribute = getattr(shape, func)
            attribute(*args, **kwargs)

    def draw(self, drawing_tool: DrawingTool) -> None:
        self._for_all_shapes('draw', drawing_tool=drawing_tool)

    def animate(self, drawing_tool: DrawingTool, time_points: List[float], action: Callable[['Shape', float, float], 'Shape'],
                pause_per_frame: float = 0.5,
                dt: float = 0.5,
                title=None):

        for n, t in enumerate(time_points):
            drawing_tool.erase()

            fig = action(self, t, dt)
            fig.draw(self, drawing_tool)

    def draw_dimensions(self, drawing_tool: DrawingTool):
        if hasattr(self, 'dimensions'):
            for shape in self.dimensions:
                self.dimensions[shape].draw(drawing_tool)
            return self
        else:
            # raise AttributeError('no self.dimensions dict for defining dimensions of class %s' %
            # self.__classname__.__name__)
            return self

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
        print(space, '%s: %s.shapes has entries' %
              (self.__class__.__name__, name),
              str(list(self._shapes.keys()))[1:-1])

        for shape in self._shapes:
            print(space, end=' ')
            print('call %s.shapes["%s"].recurse("%s", %d)' %
                  (name, shape, shape, indent + 2))
            self._shapes[shape].recurse(shape, indent + 2)

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
    def style(self):
        return self._style

    @style.setter
    def style(self, style: Style):
        self._style = style

    def set_line_width(self, line_width: int) -> 'Shape':
        self.style.line_with = line_width
        return self

    def set_line_style(self, line_style: Style.LineStyle) -> 'Shape':
        self.style.line_style = line_style
        return self

    def set_line_color(self, line_color: Style.Color) -> 'Shape':
        self.style.line_color = line_color
        return self

    def set_fill_pattern(self, fill_pattern: Style.FillPattern) -> 'Shape':
        self.style.fill_pattern = fill_pattern
        return self

    def set_arrow(self, arrow: Style.ArrowStyle) -> 'Shape':
        self.style.arrow = arrow
        return self
