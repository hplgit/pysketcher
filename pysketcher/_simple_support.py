from pysketcher._point import Point
from pysketcher._rectangle import Rectangle
from pysketcher._triangle import Triangle
from pysketcher.composition import Composition


class SimpleSupport(Composition):
    """A representation of a simple support.

    Often used in static load analysis, this shows a diagrammatic
    representation of a point support.

    Args:
         position: The top of the simple support.
         size: The distance from the top of the simple support to the center of
            the base.

    Examples:
        >>> s = ps.SimpleSupport(ps.Point(1.0, 1.0), 0.5)
        >>> fig = ps.Figure(0, 2.0, 0, 1.5, backend=MatplotlibBackend)
        >>> fig.add(s)
        >>> fig.save("pysketcher/images/simple_support.png")

        .. figure:: images/simple_support.png
            :alt: An example of a SimpleSupport.
            :figclass: align-center

            An example of ``SimpleSupport``.

    """

    _position: Point
    _size: float

    def __init__(self, position: Point, size: float):
        self._position = position
        self._size = size
        self._p0 = Point(position.x - size / 2.0, position.y - size)
        self._p1 = Point(position.x + size / 2.0, position.y - size)
        self._triangle = Triangle(self._p0, self._p1, position)
        gap = size / 5.0
        self._height = size / 4.0  # height of rectangle
        self._p2 = Point(self._p0.x, self._p0.y - gap - self._height)
        self._rectangle = Rectangle(self._p2, self._size, self._height)
        shapes = {"triangle": self._triangle, "rectangle": self._rectangle}
        super().__init__(shapes)

    @property
    def mid_support(self) -> Point:
        """Returns the midpoint of the base of the support."""
        return (self._rectangle.lower_left + self._rectangle.lower_right) * 0.5
