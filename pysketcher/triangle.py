from pysketcher.curve import Curve
from pysketcher.point import Point
from pysketcher.text import Text


class Triangle(Curve):
    """
    Triangle defined by its three vertices p1, p2, and p3.

    Recorded geometric features:

    ==================== =============================================
    Attribute            Description
    ==================== =============================================
    p1, p2, p3           Corners as given to the constructor.
    ==================== =============================================

    """

    def __init__(self, p1: Point, p2: Point, p3: Point):
        self._p1 = p1
        self._p2 = p2
        self._p3 = p3

        # Dimensions
        self.dimensions = {
            "p1": Text("p1", p1),
            "p2": Text("p2", p2),
            "p3": Text("p3", p3),
        }
        super().__init__([p1, p2, p3, p1])

    def geometric_features(self):
        return {"p1": self._p1, "p2": self._p2, "p3": self._p3}

    def rotate(self, angle: float, center: Point):
        return Triangle(
            self._p1.rotate(angle, center),
            self._p2.rotate(angle, center),
            self._p3.rotate(angle, center),
        )
