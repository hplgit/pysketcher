from typing import List

from pysketcher import Angle
from pysketcher._curve import Curve
from pysketcher._point import Point


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

    def __init__(self, lower_left_corner: Point, width: float, height: float):

        self._width = width
        self._height = height
        self._lower_left_corner = lower_left_corner

        super().__init__(self._generate_points())

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

    @property
    def width(self) -> float:
        """The width of the rectangle."""
        return self._width

    @property
    def height(self) -> float:
        """The height of the rectangle."""
        return self._height

    @property
    def lower_left(self) -> Point:
        """The lower left point of the rectangle."""
        return self._lower_left_corner

    @property
    def lower_right(self) -> Point:
        """The lower right point of the rectangle."""
        return self._lower_left_corner + Point(self._width, 0)

    @property
    def upper_left(self) -> Point:
        """The upper left point of the rectangle."""
        return self._lower_left_corner + Point(0, self._height)

    @property
    def upper_right(self) -> Point:
        """The upper right point of the rectangle."""
        return self._lower_left_corner + Point(self._width, self._height)
