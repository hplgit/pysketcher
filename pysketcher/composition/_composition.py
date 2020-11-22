from typing import Callable, Dict, TypeVar, Union

from pysketcher._point import Point
from pysketcher._shape import Shape, Stylable
from pysketcher._style import Style
from pysketcher._text import Text

T = TypeVar("T")


class Composition(Stylable):
    """Provides a convenient means to group shapes together."""

    class CompositionStyle(Style):
        """Presents the Stylable contract for a Composition.

        Sets the style of each object in the composition
        transparently.
        """

        composition: "Composition"

        def __init__(self, composition: "Composition"):
            super().__init__()
            self.composition = composition

        @property
        def line_style(self) -> Style.LineStyle:
            """The line style of all ``Shapes`` in the composition."""
            return super().line_style

        @line_style.setter
        def line_style(self, line_style: Style.LineStyle):
            for shape in self.composition:
                shape.style.line_style = line_style

        @property
        def line_width(self) -> float:
            """The line width of all ``Shapes`` in the composition."""
            return super().line_width

        @line_width.setter
        def line_width(self, line_width: float):
            for shape in self.composition:
                shape.style.line_width = line_width

        @property
        def line_color(self) -> Style.Color:
            """The line color of all ``Shapes`` in the composition."""
            return super().line_color

        @line_color.setter
        def line_color(self, line_color: Style.Color):
            for shape in self.composition:
                shape.style.line_color = line_color

        @property
        def fill_color(self) -> Style.Color:
            """The fill color of all ``Shapes`` in the composition."""
            return super().fill_color

        @fill_color.setter
        def fill_color(self, fill_color: Style.Color):
            for shape in self.composition:
                shape.style.fill_color = fill_color

        @property
        def fill_pattern(self) -> Style.FillPattern:
            """The fill pattern of all ``Shapes`` in the composition."""
            return super().fill_pattern

        @fill_pattern.setter
        def fill_pattern(self, fill_pattern: Style.Color):
            for shape in self.composition:
                shape.style.fill_pattern = fill_pattern

        @property
        def arrow(self) -> Style.ArrowStyle:
            """The arrow nature of all ``Shapes`` in the composition."""
            return super().arrow

        @arrow.setter
        def arrow(self, arrow: Style.ArrowStyle):
            for shape in self.composition:
                shape.style.arrow = arrow

        @property
        def shadow(self) -> float:
            """The shadow style of all ``Shapes`` in the composition."""
            return super().shadow

        @shadow.setter
        def shadow(self, shadow: float):
            for shape in self.composition:
                shape.style.shadow = shadow

    _shapes: dict

    def __init__(self, shapes: dict):
        """shapes: list or dict of Shape objects."""
        super().__init__()
        self._shapes = shapes
        self._style = self.CompositionStyle(self)

    def __iter__(self):
        """Provides an ``interable`` of the shapes in the composition."""
        return self._shapes.values().__iter__()

    def add(self, key: str, shape: Shape) -> "Composition":
        """Adds a shape to the composition.

        Args:
            key: the name of the shape to be added
            shape: the shape to be added.

        Returns:
            a copy of the composition with the requisite shape added
        """
        shapes = self._shapes.copy()
        shapes[key] = shape
        return Composition(shapes)

    def __getitem__(self, key):
        """Gets the ``shape`` in the ``Composition`` with key ``key``."""
        return self._shapes[key]

    def _for_all_shapes(self, func: str, *args, **kwargs) -> "Composition":
        shapes = dict()
        for key, shape in self._shapes.items():
            shapes[key] = getattr(shape, func)(*args, **kwargs)
        return Composition(shapes)

    def rotate(self, angle: float, center: Point) -> "Composition":
        """Rotate the composition.

        Args:
            angle: The ``Angle`` in radians through which the shape should be rotated.
            center: The ``Point`` about which the rotation should be performed.

        Returns:
            A copy of the ``Composition`` rotated through ``angle`` about ``center``.
        """
        return self._for_all_shapes("rotate", angle, center)

    def translate(self, vec) -> "Composition":
        """Translate the composition.

        Args:
            vec: The vector through which the ``Composition`` should be translated.

        Returns:
            A copy of the ``Composition`` translated through ``vec``.
        """
        return self._for_all_shapes("translate", vec)

    def scale(self, factor) -> "Composition":
        """Scale the composition.

        Args:
            factor: The factor by which the ``Composition`` should be scaled.

        Returns:
            A copy of the ``Composition`` scaled by ``factor``.
        """
        return self._for_all_shapes("scale", factor)

    def apply(
        self, func: Callable[[Union[Shape, Text, "Composition"]], T]
    ) -> Dict[str, T]:
        """Applies a function to every member of a ``Composition``.

        Args:
            func: The function to apply.

        Returns:
            A copy of the ``Composition`` with the function applied.
        """
        ret_dict = {}
        for key, shape in self._shapes.items():
            ret_dict[key] = func(shape)
        return ret_dict


class ShapeWithText(Composition):
    """A convenience class to combine a Shape with a Text Object.

    Args:
        shape: The shape.
        text: The text.
    """

    def __init__(self, shape: Shape, text: Text):
        super().__init__({"text": text, "shape": shape})
