from typing import List

from .matplotlibdraw import MatplotlibDraw
from .shape import Shape
from .curve import Curve
from .point import Point

from .distance_wtext import Distance_wText
from .text_warrow import Text_wArrow


class Rectangle(Shape):
    """
    Rectangle specified by the point `lower_left_corner`, `width`,
    and `height`.
    """
    _points: List[Point]
    _lower_left_corner: Point
    _width: float
    _height: float

    def __init__(self, lower_left_corner: Point, width: float, height: float, drawing_tool: MatplotlibDraw):
        super().__init__(drawing_tool)

        self._width = width
        self._height = height
        self._lower_left_corner = lower_left_corner

        self._points = None  # Populated by the next method call
        self._generate_points()
        self._shapes = {'rectangle': Curve(self._points, drawing_tool)}

        # Dimensions
        dims = {
            'width': Distance_wText(self._lower_left_corner + Point(0, -height / 5.),
                                    self._lower_left_corner + Point(width, -height / 5.),
                                    'width', self._drawing_tool),
            'height': Distance_wText(self._lower_left_corner + Point(width + width / 5., 0),
                                     self._lower_left_corner + Point(width + width / 5., height),
                                     'height', self._drawing_tool),
            'lower_left_corner': Text_wArrow('lower_left_corner',
                                             self._lower_left_corner - Point(width / 5., height / 5.),
                                             self._lower_left_corner,
                                             self._drawing_tool)
        }
        self.dimensions = dims

    def _generate_points(self) -> List[Point]:
        self._points = [self._lower_left_corner,
                        self._lower_left_corner + Point(self._width, 0),
                        self._lower_left_corner + Point(self._width, self._height),
                        self._lower_left_corner + Point(0, self._height),
                        self._lower_left_corner]

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
        d = {'lower_left': self._points[0],
             'lower_right': self._points[1],
             'upper_right': self._points[2],
             'upper_left': self._points[3], }
        d['lower_mid'] = 0.5 * (d['lower_left'] + d['lower_right'])
        d['upper_mid'] = 0.5 * (d['upper_left'] + d['upper_right'])
        d['left_mid'] = 0.5 * (d['lower_left'] + d['upper_left'])
        d['right_mid'] = 0.5 * (d['lower_right'] + d['upper_right'])
        d['center'] = Point(d['lower_mid'][0], d['left_mid'][1])
        return d
