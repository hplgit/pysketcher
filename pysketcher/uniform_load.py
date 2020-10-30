from pysketcher.arrow import Arrow
from pysketcher.composition.composition import Composition
from pysketcher.point import Point
from pysketcher.rectangle import Rectangle


class UniformLoad(Composition):
    """
    Downward-pointing arrows indicating a vertical load.
    The arrows are of equal length and filling a rectangle
    specified as in the :class:`Rectangle` class.

    Recorded geometric features:

    ==================== =============================================
    Attribute            Description
    ==================== =============================================
    mid_top              Middle point at the top of the row of
                         arrows (often used for positioning a text).
    ==================== =============================================
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

    def geometric_features(self):
        return {"mid_top": self["box"].geometric_features()["upper_mid"]}
