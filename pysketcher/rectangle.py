from typing import List

from pysketcher.arrow_with_text import ArrowWithText
from pysketcher.curve import Curve
from pysketcher.distance_with_text import DistanceWithText
from pysketcher.point import Point
from pysketcher.shape import Shape
from pysketcher.style import TextStyle


class Rectangle(Curve):
    """
    Rectangle specified by the point `lower_left_corner`, `width`,
    and `height`.
    """

    _lower_left_corner: Point
    _width: float
    _height: float

    def __init__(self, lower_left_corner: Point, width: float, height: float):

        self._width = width
        self._height = height
        self._lower_left_corner = lower_left_corner

        super().__init__(self._generate_points())

        # Dimensions
        dims = {
            "width": DistanceWithText(
                "width",
                self._lower_left_corner + Point(0, -height / 5.0),
                self._lower_left_corner + Point(width, -height / 5.0),
            ),
            "height": DistanceWithText(
                "height",
                self._lower_left_corner + Point(width + width / 5.0, 0),
                self._lower_left_corner + Point(width + width / 5.0, height),
            ),
            "lower_left_corner": ArrowWithText(
                "lower_left_corner",
                self._lower_left_corner - Point(width / 5.0, height / 5.0),
                self._lower_left_corner,
            ),
        }
        dims["height"]["text"].style.alignment = TextStyle.Alignment.LEFT
        self.dimensions = dims

    def _generate_points(self) -> List[Point]:
        return [
            self._lower_left_corner,
            self._lower_left_corner + Point(self._width, 0),
            self._lower_left_corner + Point(self._width, self._height),
            self._lower_left_corner + Point(0, self._height),
            self._lower_left_corner,
        ]

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
        d = {
            "lower_left": self._points[0],
            "lower_right": self._points[1],
            "upper_right": self._points[2],
            "upper_left": self._points[3],
        }
        d["lower_mid"] = (d["lower_left"] + d["lower_right"]) * 0.5
        d["upper_mid"] = (d["upper_left"] + d["upper_right"]) * 0.5
        d["left_mid"] = (d["lower_left"] + d["upper_left"]) * 0.5
        d["right_mid"] = (d["lower_right"] + d["upper_right"]) * 0.5
        d["center"] = Point(d["lower_mid"].x, d["left_mid"].y)
        return d

    def rotate(self, angle: float, center: Point) -> Curve:
        points = []
        for point in self._points:
            points.append(point.rotate(angle, center))
        return Curve(points)
