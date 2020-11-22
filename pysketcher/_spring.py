import numpy as np

from pysketcher import Curve, Point
from pysketcher._line import Line
from pysketcher.composition import Composition


class Spring(Composition):
    """A representation of a spring.

    Specify a *vertical* spring, starting at `start` and with `length`
    as total vertical length. In the middle of the spring there are
    `num_windings` circular windings to illustrate the spring. If
    `teeth` is true, the spring windings look like saw teeth,
    otherwise the windings are smooth circles.  The parameters `width`
    (total width of spring) and `bar_length` (length of first and last
    bar are given sensible default values if they are not specified
    (these parameters can later be extracted as attributes, see table
    below).

    Examples:
        >>> L = 12.0
        >>> H = L / 6.0
        >>> start = ps.Point(0.0, 0.0)
        >>> s = ps.Spring(start, L)
        >>> fig = ps.Figure(-2, 2, -1, L + H, backend=MatplotlibBackend)
        >>> fig.add(s)
        >>> fig.save("pysketcher/images/spring.png")

        .. figure:: images/spring.png
            :alt: An example of a Spring.
            :figclass: align-center
            :scale: 30%

            An example of a ``Spring``.
    """

    spring_fraction = 1.0 / 2  # fraction of total length occupied by spring

    def __init__(
        self,
        start: Point,
        length: float,
        width: float = None,
        bar_length: float = None,
        num_windings: int = 11,
        teeth: bool = False,
    ):
        B = start
        n = num_windings - 1  # n counts teeth intervals
        if n <= 6:
            n = 7
        # n must be odd:
        if n % 2 == 0:
            n = n + 1
        L = length
        if width is None:
            w = L / 10.0
        else:
            w = width / 2.0
        s = bar_length

        shapes = {}
        if s is None:
            f = Spring.spring_fraction
            s = L * (1 - f) / 2.0  # start of spring

        self.bar_length = s  # record
        self.width = 2 * w

        p0 = Point(B.x, B.y + s)
        p1 = Point(B.x, B.y + L - s)
        p2 = Point(B.x, B.y + L)

        if s >= L:
            raise ValueError(
                "length of first bar: %g is larger than total length: %g" % (s, L)
            )

        shapes["bar1"] = Line(B, p0)
        spring_length = L - 2 * s
        t = spring_length / n  # height increment per winding
        if teeth:
            resolution = 4
        else:
            resolution = 90
        q = np.linspace(0, n, n * resolution + 1)
        xs = p0.x + w * np.sin(2 * np.pi * q)
        ys = p0.y + q * t
        points = Point.from_coordinate_lists(xs, ys)
        shapes["spiral"] = Curve(points)
        shapes["bar2"] = Line(p1, p2)
        super().__init__(shapes)
