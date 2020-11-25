from pysketcher._curve import Curve
from pysketcher._point import Point


class Triangle(Curve):
    """Triangle defined by its three vertices p1, p2, and p3.

    Args:
        p1: The first ``Point``.
        p2: The second ``Point``.
        p3: The third ``Point``.

    Examples:
        >>> model = ps.Triangle(ps.Point(1, 1), ps.Point(1, 4), ps.Point(3, 3))
        >>> fig = ps.Figure(0, 5, 0, 5, backend=MatplotlibBackend)
        >>> fig.add(model)
        >>> fig.save("pysketcher/images/triangle.png")

        .. figure:: images/triangle.png
            :alt: An example of Triangle.
            :figclass: align-center
            :scale: 30%

            An example of ``Triangle``.
    """

    def __init__(self, p1: Point, p2: Point, p3: Point):
        self._p1 = p1
        self._p2 = p2
        self._p3 = p3

        super().__init__([p1, p2, p3, p1])

    def rotate(self, angle: float, center: Point):
        """Rotates the Triangle through a ``angle`` about ``center``.

        Args:
            angle: The angle through which the triangle should be rotated in radians.
            center: The point about which the triangle should be rotated.

        Returns:
            A copy of the triangle subjected to the specified rotation.
        """
        return Triangle(
            self._p1.rotate(angle, center),
            self._p2.rotate(angle, center),
            self._p3.rotate(angle, center),
        )
