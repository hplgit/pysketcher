from pysketcher._arrow import Arrow
from pysketcher._point import Point
from pysketcher._rectangle import Rectangle
from pysketcher.composition import Composition


class UniformLoad(Composition):
    """Downward-pointing arrows indicating a vertical load.

    The arrows are of equal length and filling a rectangle
    specified as in the :class:`Rectangle` class.

    Examples:
        >>> l = ps.UniformLoad(ps.Point(0.5, 0.5), 4, 0.5)
        >>> fig = ps.Figure(0.0, 5.0, 0.0, 1, backend=MatplotlibBackend)
        >>> fig.add(l)
        >>> fig.save("pysketcher/images/uniform_load.png")

        .. figure:: images/uniform_load.png
            :alt: An example of a Uniform Load.
            :figclass: align-center

            An example of a ``UniformLoad``.
    """

    def __init__(
        self, lower_left_corner: Point, width: float, height: float, num_arrows=10
    ):
        box = Rectangle(lower_left_corner, width, height)
        shapes = {"box": box}
        dx = float(width) / (num_arrows - 1)
        for i in range(num_arrows):
            x = lower_left_corner.x + i * dx
            start = Point(x, lower_left_corner.y + height)
            end = Point(x, lower_left_corner.y)
            shapes["arrow%d" % i] = Arrow(start, end)
        super().__init__(shapes)
