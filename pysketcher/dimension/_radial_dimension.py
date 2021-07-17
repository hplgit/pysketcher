from typing import Dict

from pysketcher._arrow import Arrow
from pysketcher._line import Line
from pysketcher._point import Point
from pysketcher._shape import Shape
from pysketcher.annotation import LineAnnotation, TextPosition
from pysketcher.composition import Composition


class RadialDimension(Composition):
    """Used to indicate radial distances.

    Examples:
        >>> circle1 = ps.Circle(ps.Point(1.5, 1.5), 0.8)
        >>> circle1.style.line_width = 1
        >>> dim1 = RadialDimension(r"$r$", circle1.center, circle1(np.pi / 3))
        >>>
        >>> circle2 = ps.Circle(ps.Point(3.5, 1.5), 0.8)
        >>> circle2.style.line_width = 1
        >>> dim2 = RadialDimension(r"$r$", circle2.center, circle2(np.pi / 3))
        >>> dim2.diameter = True
        >>>
        >>> circle3 = ps.Circle(ps.Point(5.5, 1.5), 0.8)
        >>> circle3.style.line_width = 1
        >>> dim3 = RadialDimension(r"$r$", circle3.center, circle3(np.pi / 3))
        >>> dim3.center_mark = True
        >>>
        >>> circle4 = ps.Circle(ps.Point(7.5, 1.5), 0.8)
        >>> circle4.style.line_width = 1
        >>> dim4 = RadialDimension(r"$r$", circle4.center, circle4(np.pi / 3))
        >>> dim4.center_line = True
        >>>
        >>> circle5 = ps.Circle(ps.Point(9.5, 1.5), 0.8)
        >>> circle5.style.line_width = 1
        >>> dim5 = RadialDimension(r"$r$", circle5.center, circle5(np.pi / 3))
        >>> dim5.diameter = True
        >>> dim5.center_line = True
        >>>
        >>> fig = ps.Figure(0, 11, 0, 3, backend=MatplotlibBackend)
        >>> fig.add(circle1)
        >>> fig.add(dim1)
        >>> fig.add(circle2)
        >>> fig.add(dim2)
        >>> fig.add(circle3)
        >>> fig.add(dim3)
        >>> fig.add(circle4)
        >>> fig.add(dim4)
        >>> fig.add(circle5)
        >>> fig.add(dim5)
        >>> fig.save("pysketcher/images/radial_dimension.png")

    .. figure:: images/radial_dimension.png
        :alt: An example of LinearDimension.
        :figclass: align-center
        :scale: 30%

        An example of ``RadialDimension``.
    """

    _DEFAULT_DIAMETER: bool = False
    _DEFAULT_CENTER_LINE: bool = False
    _DEFAULT_CENTER_MARK: bool = False

    _DEFAULT_OFFSET: float = 0.2

    def __init__(self, text: str, center: Point, edge: Point):
        self._text = text
        self._center = center
        self._edge = edge
        self._offset = self._DEFAULT_OFFSET
        self._diameter = self._DEFAULT_DIAMETER
        self._center_line = self._DEFAULT_CENTER_LINE
        self._center_mark = self._DEFAULT_CENTER_MARK
        super().__init__(self._generate_shapes())

    def _generate_shapes(self) -> Dict[str, Shape]:
        arrow1 = Arrow(
            self._edge + (self._edge - self._center) * self._offset, self._edge
        )
        text = LineAnnotation(self._text, arrow1, TextPosition.START)
        text.style.font_size = 24
        ret_dict = {"arrow1": arrow1, "text": text}

        if self._diameter:
            inward_vector = self._center - self._edge
            offset_vector = inward_vector.unit_vector * self._offset
            start = self._edge + inward_vector * 2 + offset_vector
            end = self._edge + inward_vector * 2

            ret_dict["arrow2"] = Arrow(start, end)

        if self._center_mark:
            ret_dict["center_mark_h"] = Line(
                self._center - Point(-self._offset * 0.5, 0),
                self._center - Point(self._offset * 0.5, 0),
            )
            ret_dict["center_mark_v"] = Line(
                self._center - Point(0, -self._offset * 0.5),
                self._center - Point(0, self._offset * 0.5),
            )

        if self._center_line:
            ret_dict["center_line"] = Line(self._edge, self._center)

        if self._center_line and self._diameter:
            ret_dict["center_line2"] = Line(
                self._center, self._center + (self._center - self._edge)
            )
        return ret_dict

    @property
    def diameter(self) -> bool:
        """If true, the dimension indicates diameter rather than radius."""
        return self._diameter

    @diameter.setter
    def diameter(self, diameter: bool):
        self._diameter = diameter
        self._shapes = self._generate_shapes()

    @property
    def center_mark(self) -> bool:
        """If true, a center mark will be drawn."""
        return self._center_mark

    @center_mark.setter
    def center_mark(self, center_mark: bool):
        self._center_mark = center_mark
        self._shapes = self._generate_shapes()

    @property
    def center_line(self) -> bool:
        """If true then a line will be drawn from the center to the circumference."""
        return self._center_line

    @center_line.setter
    def center_line(self, center_line: bool):
        self._center_line = center_line
        self._shapes = self._generate_shapes()
