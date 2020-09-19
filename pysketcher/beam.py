from .composition import Composition
from .distance_with_text import DistanceWithText
from .point import Point
from .style import Style
from .text import Text
from .triangle import Triangle
from .rectangle import Rectangle


class SimpleSupport(Composition):
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

    def geometric_features(self):
        t = self["triangle"]
        r = self["rectangle"]
        d = {
            "pos": t.geometric_features()["p2"],
            "mid_support": r.geometric_features()["lower_mid"],
        }
        return d
