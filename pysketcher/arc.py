import logging

import numpy as np

from pysketcher.angle import Angle
from pysketcher.composition.composition import ShapeWithText
from pysketcher.curve import Curve
from pysketcher.point import Point
from pysketcher.text import Text


class Arc(Curve):
    """
    A representation of a continuous connected subset of a circle.
    """

    _center: Point
    _radius: float
    _start_angle: Angle
    _arc_angle: Angle
    _resolution: int

    def __init__(
        self,
        center: Point,
        radius: float,
        start_angle: Angle,
        arc_angle: Angle,
        resolution: int = 180,
    ):
        # Must record some parameters for __call__
        self._center = center
        self._radius = radius
        self._start_angle = Angle(start_angle)
        self._arc_angle = Angle(arc_angle)
        self._resolution = resolution

        if self._arc_angle == 0.0:
            # assume a full circle
            ts = np.linspace(0.0, 2.0 * np.pi, resolution + 1)
        else:
            ts = np.linspace(0.0, self._arc_angle, resolution + 1)

        points = [self(t) for t in ts]
        super().__init__(points)

    def __call__(self, theta: Angle) -> Point:
        """
        Return (x,y) point at start_angle + theta.
        """
        if self._arc_angle != 0.0 and theta > self._arc_angle:
            raise ValueError("Theta is outside the bounds of the arc")
        iota = Angle(self.start_angle + theta)
        ret_point = Point(
            self.center.x + self.radius * np.cos(iota),
            self.center.y + self.radius * np.sin(iota),
        )
        return ret_point

    @property
    def start_angle(self) -> Angle:
        return self._start_angle

    @property
    def arc_angle(self) -> Angle:
        return self._arc_angle

    @property
    def end_angle(self) -> Angle:
        return self._start_angle + self._arc_angle

    @property
    def radius(self) -> float:
        return self._radius

    @property
    def center(self) -> Point:
        return self._center

    @property
    def start(self) -> Point:
        return self(0.0)

    @property
    def end(self) -> Point:
        return self(self.arc_angle)

    def translate(self, vec: Point) -> "Arc":
        arc = Arc(
            self._center + vec,
            self._radius,
            self._start_angle,
            self._arc_angle,
            self._resolution,
        )
        arc.style = self.style
        return arc


class ArcWithText(ShapeWithText):
    def __init__(
        self,
        text: str,
        center: Point,
        radius: float,
        start_angle: Angle,
        arc_angle: Angle,
        resolution: int = 180,
        text_spacing: float = 1 / 6.0,
    ):
        arc = Arc(center, radius, start_angle, arc_angle, resolution)
        mid = arc(arc_angle / 2.0)
        normal = (mid - center).unit_vector()
        text_pos = mid - (normal * text_spacing)
        text = Text(text, text_pos)
        super().__init__(arc, text)
