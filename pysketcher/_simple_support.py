from pysketcher._distance_with_text import DistanceWithText
from pysketcher._point import Point
from pysketcher._rectangle import Rectangle
from pysketcher._text import Text
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
        p0 = Point(position.x - size / 2.0, position.y - size)
        p1 = Point(position.x + size / 2.0, position.y - size)
        triangle = Triangle(p0, p1, position)
        gap = size / 5.0
        h = size / 4.0  # height of rectangle
        p2 = Point(p0.x, p0.y - gap - h)
        rectangle = Rectangle(p2, size, h)
        shapes = {"triangle": triangle, "rectangle": rectangle}
        super().__init__(shapes)

        self._dimensions = {
            "position": Text("position", position),
            "size": DistanceWithText(
                "size", Point(p2.x, p2.y - size), Point(p2.x + size, p2.y - size)
            ),
        }
