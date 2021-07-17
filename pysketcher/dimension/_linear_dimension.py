from enum import auto, Enum, unique
from typing import Dict

from pysketcher._arrow import DoubleArrow
from pysketcher._line import Line
from pysketcher._point import Point
from pysketcher._shape import Shape
from pysketcher.annotation import LineAnnotation, TextPosition
from pysketcher.composition import Composition


class LinearDimension(Composition):
    """Used to indicate the linear distance between two points.

    Examples:
        >>> triangle1 = ps.Triangle(ps.Point(1, 1), ps.Point(1, 2), ps.Point(3, 1))
        >>> dim1 = LinearDimension(r"$c$", ps.Point(3, 1), ps.Point(1, 2))
        >>> text1 = ps.Text("Aligned", ps.Point(2, 0.5))
        >>>
        >>> triangle2 = ps.Triangle(ps.Point(5, 1), ps.Point(5, 2), ps.Point(7, 1))
        >>> dim2 = LinearDimension(r"$a$", ps.Point(7, 1), ps.Point(5, 2))
        >>> dim2.offset_style = LinearDimension.OffsetStyle.HORIZONTAL
        >>> text2 = ps.Text("Horizontal", ps.Point(6, 0.5))
        >>>
        >>> triangle3 = ps.Triangle(ps.Point(9, 1), ps.Point(9, 2), ps.Point(11, 1))
        >>> dim3 = LinearDimension(r"$b$", ps.Point(11, 1), ps.Point(9, 2))
        >>> dim3.offset_style = LinearDimension.OffsetStyle.VERTICAL
        >>> text3 = ps.Text("Vertical", ps.Point(10, 0.5))
        >>>
        >>> fig = ps.Figure(0, 13, 0, 3, backend=MatplotlibBackend)
        >>> fig.add(triangle1)
        >>> fig.add(dim1)
        >>> fig.add(text1)
        >>> fig.add(triangle2)
        >>> fig.add(dim2)
        >>> fig.add(text2)
        >>> fig.add(triangle3)
        >>> fig.add(dim3)
        >>> fig.add(text3)
        >>> fig.save("pysketcher/images/linear_dimension.png")

        .. figure:: images/linear_dimension.png
            :alt: An example of LinearDimension.
            :figclass: align-center
            :scale: 30%

            An example of ``LinearDimension``.
    """

    _DEFAULT_OFFSET: float = 0.5
    _DEFAULT_MINOR_OFFSET: float = 0.1

    @unique
    class OffsetStyle(Enum):
        """The style of offset in a Linear dimension."""

        HORIZONTAL = auto()
        VERTICAL = auto()
        ALIGNED = auto()

    def __init__(
        self,
        text: str,
        start: Point,
        end: Point,
        offset_style: OffsetStyle = OffsetStyle.ALIGNED,
    ):
        self._start = start
        self._end = end
        self._text = text
        self._offset_style = offset_style
        self._offset = self._DEFAULT_OFFSET
        self._minor_offset = self._DEFAULT_MINOR_OFFSET

        super().__init__(self._generate_shapes())

    def _generate_shapes(self) -> Dict[str, Shape]:
        if self._offset_style == self.OffsetStyle.ALIGNED:
            self._dimension_vector = self._start - self._end
            self._offset_vector = self._dimension_vector.normal * self.offset

            arrow = DoubleArrow(
                self._start + self._offset_vector, self._end + self._offset_vector
            )

        elif self._offset_style == self.OffsetStyle.HORIZONTAL:
            arrow = self._horizontal_arrow()

        elif self._offset_style == self.OffsetStyle.VERTICAL:
            arrow = self._vertical_arrow()
        else:
            raise NotImplementedError()

        annotation = LineAnnotation(self._text, arrow, TextPosition.MIDDLE)

        def extension_line(start: Point, end: Point) -> Line:
            return Line(
                start + (end - start) * self._minor_offset,
                end + (end - start) * self._minor_offset,
            )

        return {
            "arrow": arrow,
            "annotation": annotation,
            "extension_line_1": extension_line(self._start, arrow.start),
            "extension_line_2": extension_line(self._end, arrow.end),
        }

    def _horizontal_arrow(self) -> DoubleArrow:
        if self._start.x < self._end.x:
            return DoubleArrow(
                Point(self._start.x, self._start.y + self._offset),
                Point(self._end.x, self._start.y + self._offset),
            )
        else:
            return DoubleArrow(
                Point(self._start.x, self._end.y + self._offset),
                Point(self._end.x, self._end.y + self._offset),
            )

    def _vertical_arrow(self) -> DoubleArrow:
        if self._start.y > self._end.y:
            return DoubleArrow(
                Point(self._end.x + self._offset, self._start.y),
                Point(self._end.x + self._offset, self._end.y),
            )
        else:
            return DoubleArrow(
                Point(self._start.x + self._offset, self._start.y),
                Point(self._start.x + self._offset, self._end.y),
            )

    @property
    def offset_style(self) -> OffsetStyle:
        """Specifies the orientation of the drawn dimension."""
        return self._offset_style

    @offset_style.setter
    def offset_style(self, offset_style: OffsetStyle):
        self._offset_style = offset_style
        self._shapes = self._generate_shapes()

    @property
    def offset(self) -> float:
        """How far the dimension should be offset from the provided points."""
        return self._offset

    @offset.setter
    def offset(self, offset: float):
        self._offset = offset
        self._shapes = self._generate_shapes()

    @property
    def start(self) -> Point:
        """The start of the dimension."""
        return self._start

    @property
    def end(self) -> Point:
        """The end of the dimension."""
        return self._end
