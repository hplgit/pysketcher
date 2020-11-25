import numpy as np

from pysketcher._arc import Arc
from pysketcher._point import Point


class Circle(Arc):
    """A representation of a 2D circle.

    Args:
        center: The center of the circle.
        radius: The radius of the circle.

    Examples:
        >>> circle = ps.Circle(ps.Point(1.5, 1.5), 1)
        >>> fig = ps.Figure(0, 3, 0, 3, backend=MatplotlibBackend)
        >>> fig.add(circle)
        >>> fig.save("pysketcher/images/circle.png")

    .. figure:: images/circle.png
        :alt: An example of Circle.
        :figclass: align-center

        An example of ``Circle``.
    """

    def __init__(self, center: Point, radius: float, resolution=180):
        super().__init__(center, radius, 0, 2 * np.pi, resolution)
