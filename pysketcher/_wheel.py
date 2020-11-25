import numpy as np

from pysketcher._circle import Circle
from pysketcher._line import Line
from pysketcher._point import Point
from pysketcher.composition import Composition


class Wheel(Composition):
    """A representation of a wheel.

    Args:
        center: The center of the ``Wheel``.
        radius: The radius of the ``Wheel``.
        inner_radius: The radius of the hub of the ``Wheel``.

    Examples:
        >>> w = ps.Wheel(ps.Point(1.0, 1.0), 0.5, 0.25)
        >>> fig = ps.Figure(0.0, 2.0, 0.0, 2.0, backend=MatplotlibBackend)
        >>> fig.add(w)
        >>> fig.save("pysketcher/images/wheel.png")

        .. figure:: images/wheel.png
            :alt: An example of a Wheel.
            :figclass: align-center

            An example of a ``Wheel``.
    """

    _center: Point
    _radius: float
    _inner_radius: float
    _nlines: int

    def __init__(
        self, center: Point, radius: float, inner_radius: float = None, nlines: int = 10
    ):
        self._center = center
        self._radius = radius
        self._inner_radius = inner_radius
        self._nlines = nlines

        if inner_radius is None:
            self._inner_radius = radius / 5.0

        outer = Circle(center, radius)
        inner = Circle(center, inner_radius)
        lines = []
        # Draw nlines+1 since the first and last coincide
        # (then nlines lines will be visible)
        t = np.linspace(0, 2 * np.pi, nlines + 1)

        xinner = self._center.x + self._inner_radius * np.cos(t)
        yinner = self._center.y + self._inner_radius * np.sin(t)
        xouter = self._center.x + self._radius * np.cos(t)
        youter = self._center.y + self._radius * np.sin(t)
        lines = [
            Line(Point(xi, yi), Point(xo, yo))
            for xi, yi, xo, yo in zip(xinner, yinner, xouter, youter)
        ]
        super().__init__(
            {
                "inner": inner,
                "outer": outer,
                "spokes": Composition(
                    {"spoke%d" % i: lines[i] for i in range(len(lines))}
                ),
            }
        )
