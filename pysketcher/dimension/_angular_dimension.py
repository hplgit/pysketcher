from enum import auto, Enum, unique
from typing import Dict

import numpy as np

from pysketcher._arc import Arc
from pysketcher._line import Line
from pysketcher._point import Point
from pysketcher._shape import Shape
from pysketcher._style import Style
from pysketcher.annotation import ArcAnnotation
from pysketcher.composition import Composition


class AngularDimension(Composition):
    """Used to indicate the angle between two points about a given center.

    Args:
        start: the point from which the angle should be indicated
        end: the point to which the angle should be indicated
        center: the point about which the angle should be indicated

    returns: A composition.

    Examples:
        >>> arc1 = ps.Arc(ps.Point(0.25, 0.25), 1.0, ps.Angle(0.0), ps.Angle(np.pi / 2))
        >>> arc1.style.line_color = ps.Style.Color.BLUE
        >>> dim1 = ps.AngularDimension("$a$", arc1.start, arc1.end, arc1.center)
        >>>
        >>> arc2 = ps.Arc(
        ...     ps.Point(0.25, -0.25), 1.0, ps.Angle(0.0), ps.Angle(-np.pi / 2)
        ... )
        >>> arc2.style.line_color = ps.Style.Color.GREEN
        >>> dim2 = ps.AngularDimension("$b$", arc2.start, arc2.end, arc2.center)
        >>>
        >>> arc3 = ps.Arc(
        ...     ps.Point(-0.25, 0.25), 1.0, ps.Angle(np.pi / 2), ps.Angle(np.pi / 2)
        ... )
        >>> arc3.style.line_color = ps.Style.Color.RED
        >>> dim3 = ps.AngularDimension("$c$", arc3.start, arc3.end, arc3.center)
        >>>
        >>> fig = ps.Figure(-2.0, 2.0, -2.0, 2.0, backend=MatplotlibBackend)
        >>> fig.add(arc1)
        >>> fig.add(dim1)
        >>> fig.add(arc2)
        >>> fig.add(dim2)
        >>> fig.add(arc3)
        >>> fig.add(dim3)
        >>> fig.save("pysketcher/images/angular_dimension.png")
    """

    @unique
    class Orientation(Enum):
        """Specifies if the dimension should be drawn inside or outside the angle."""

        INTERNAL = auto()
        EXTERNAL = auto()

    _DEFAULT_OFFSET: float = 0.5
    _DEFAULT_MINOR_OFFSET: float = 0.1
    _DEFAULT_ORIENTATION: Orientation = Orientation.EXTERNAL
    _DEFAULT_EXTENSION_LINES: bool = True

    def __init__(self, text: str, start: Point, end: Point, center: Point):
        self._text = text
        self._start = start
        self._end = end
        self._center = center
        self._offset = self._DEFAULT_OFFSET
        self._minor_offset = self._DEFAULT_MINOR_OFFSET
        self._orientation = self._DEFAULT_ORIENTATION
        self._extension_lines = self._DEFAULT_EXTENSION_LINES
        super().__init__(self._generate_shapes())

    def _generate_shapes(self) -> Dict[str, Shape]:
        shapes = self._generate_extension_lines()

        # TODO: code a flag to indicate the outside angle
        self._start_angle = (self._start - self._center).angle
        self._end_angle = (self._end - self._center).angle
        if abs(self._end.angle - self._start.angle) > np.pi:
            self._start_angle, self._end_angle = self._end_angle, self._start_angle

        arc = Arc(
            self._center,
            abs(self._center - self._start) + self._offset,
            self._start_angle,
            (self._end_angle - self._start_angle),
        ).set_arrow(Style.ArrowStyle.DOUBLE)
        shapes["arrow"] = arc
        shapes["annotation"] = ArcAnnotation(self._text, arc)

        return shapes

    def _generate_extension_lines(self) -> Dict[str, Shape]:
        extension_lines = {}

        def extension_line_vector(p: Point, c: Point):
            if self._orientation == self.Orientation.EXTERNAL:
                vec = (p - c).unit_vector
            elif self._orientation == self.Orientation.INTERNAL:
                vec = (p - c).unit_vector * -1
            else:
                raise ValueError(f"Invalid value for Orientation: {self._orientation}")
            return vec

        if self._extension_lines:
            extension_line1_vector = extension_line_vector(self._start, self._center)
            extension_lines["extension_line_1"] = Line(
                self._start + extension_line1_vector * self._minor_offset,
                self._start
                + extension_line1_vector * (self._offset + self._minor_offset),
            )

            extension_line2_vector = extension_line_vector(self._end, self._center)
            extension_lines["extension_line_2"] = Line(
                self._end + extension_line2_vector * self._minor_offset,
                self._end
                + extension_line2_vector * (self._offset + self._minor_offset),
            )
        return extension_lines

    @property
    def start(self) -> Point:
        """The start of the dimension."""
        return self._start

    @property
    def end(self) -> Point:
        """The end of the dimension."""
        return self._end

    @property
    def center(self) -> Point:
        """The center of the dimension."""
        return self._center

    @property
    def extension_lines(self) -> bool:
        """If true, extension lines will be drawn."""
        return self._extension_lines

    @extension_lines.setter
    def extension_lines(self, extension_lines):
        self._extension_lines = extension_lines
        self._shapes = self._generate_shapes()
