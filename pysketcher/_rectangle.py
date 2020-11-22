from typing import List

from pysketcher import Angle
from pysketcher._arrow_with_text import ArrowWithText
from pysketcher._curve import Curve
from pysketcher._distance_with_text import DistanceWithText
from pysketcher._point import Point
from pysketcher._style import TextStyle


class Rectangle(Curve):
    """A representation of a rectangle.

    Rectangle specified by the point `lower_left_corner`, `width`,
    and `height`.

    Args:
        lower_left_corner: The point from which the ``Rectangle`` should
            be drawn.
        width: The width of the ``Rectangle``.
        height: The height of the ``Rectangle``.

    Examples:
        >>> code = ps.Rectangle(ps.Point(1, 1), 3, 4)
        >>> model = ps.Composition(dict(text=code))
        >>> fig = ps.Figure(0, 5, 0, 5, backend=MatplotlibBackend)
        >>> fig.add(model)
        >>> fig.save("pysketcher/images/rectangle.png")


    .. figure:: images/rectangle.png
        :alt: An example of Rectangle.
        :figclass: align-center
        :scale: 50%

        An example of ``Rectangle``.
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

    def rotate(self, angle: Angle, center: Point) -> Curve:
        """Rotates the rectangle through ``angle`` radians about ``center``.

        Args:
            angle: The angle in radians through which the rotation should be.
            center: The point about which the rotation should be performed.

        Returns:
            A curve which looks like a rectangle rotated. We need to fix this
            so that the rectangle class supports rectangles with sides which are not
            parallel to the horizontal.
        """
        points = []
        for point in self._points:
            points.append(point.rotate(angle, center))
        return Curve(points)
