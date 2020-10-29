import numpy as np

from pysketcher.composition.composition import ShapeWithText

from .curve import Curve
from .point import Point
from .text import Text


class Arc(Curve):
    """
    A representation of a continuous connected subset of a circle.
    """

    _center: Point
    _radius: float
    start_angle: float
    arc_angle: float
    resolution: int

    def __init__(
        self,
        center: Point,
        radius: float,
        start_angle: float,
        arc_angle: float,
        resolution: int = 180,
    ):
        # Must record some parameters for __call__
        self._center = center
        self._radius = radius
        self._resolution = resolution
        self._start_angle = start_angle
        self._arc_angle = arc_angle

        ts = np.linspace(
            self._start_angle, self._start_angle + self._arc_angle, resolution + 1
        )

        points = [
            Point(center.x + radius * np.cos(t), center.y + radius * np.sin(t))
            for t in ts
        ]
        super().__init__(points)

        # Cannot set dimensions (Arc_wText recurses into this
        # constructor forever). Set in test_Arc instead.

    def translate(self, vec: Point) -> "Arc":
        circle = Arc(
            self._center + vec,
            self._radius,
            self._start_angle,
            self._arc_angle,
            self._resolution,
        )
        circle.style = self.style
        return circle

    def geometric_features(self):
        m = self._resolution // 2  # mid point in array
        return {
            "start": self._points[0],
            "end": self._points[-1],
            "mid": self._points[m],
        }

    def __call__(self, theta):
        """
        Return (x,y) point at start_angle + theta.
        Not valid after translation, rotation, or scaling.
        """
        if theta > self._arc_angle:
            raise ValueError("Theta is outside the bounds of the arc")

        return Point(
            self._center.x + self._radius * np.cos(self._start_angle + theta),
            self._center.y + self._radius * np.sin(self._start_angle + theta),
        )


class ArcWithText(ShapeWithText):
    def __init__(
        self,
        text: str,
        center: Point,
        radius: float,
        start_angle: float,
        arc_angle: float,
        fontsize: float = 0,
        resolution: int = 180,
        text_spacing: float = 1 / 6.0,
    ):
        arc = Arc(center, radius, start_angle, arc_angle, resolution)
        mid = arc(arc_angle / 2.0)
        normal = (mid - center).unit_vector()
        text_pos = mid + normal * text_spacing
        text = Text(text, text_pos)
        super().__init__(arc, text)
