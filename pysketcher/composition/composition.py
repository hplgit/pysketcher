from typing import Any, Callable, Dict, TypeVar, Union

from pysketcher.point import Point
from pysketcher.shape import Shape, Stylable
from pysketcher.style import Style, TextStyle
from pysketcher.text import Text

T = TypeVar("type")


class Composition(Stylable):
    class CompositionStyle(Style):
        """Presents the Stylable contract for a Composition, setting the style of each object in the composition
        transparently """

        _composition: "Composition"

        def __init__(self, composition: "Composition"):
            super().__init__()
            self._composition = composition

        @property
        def line_style(self) -> Style.LineStyle:
            return super().line_style

        @line_style.setter
        def line_style(self, line_style: Style.LineStyle):
            for shape in self._composition:
                shape.style.line_style = line_style

        @property
        def line_width(self) -> float:
            return super().line_width

        @line_width.setter
        def line_width(self, line_width: float):
            for shape in self._composition:
                shape.style.line_width = line_width

        @property
        def line_color(self) -> Style.Color:
            return super().line_color

        @line_color.setter
        def line_color(self, line_color: Style.Color):
            for shape in self._composition:
                shape.style.line_color = line_color

        @property
        def fill_color(self) -> Style.Color:
            return super().fill_color

        @fill_color.setter
        def fill_color(self, fill_color: Style.Color):
            for shape in self._composition:
                shape.style.fill_color = fill_color

        @property
        def fill_pattern(self) -> Style.FillPattern:
            return super().fill_pattern

        @fill_pattern.setter
        def fill_pattern(self, fill_pattern: Style.Color):
            for shape in self._composition:
                shape.style.fill_pattern = fill_pattern

        @property
        def arrow(self) -> Style.ArrowStyle:
            return super().arrow

        @arrow.setter
        def arrow(self, arrow: Style.ArrowStyle):
            for shape in self._composition:
                shape.style.arrow = arrow

        @property
        def shadow(self) -> float:
            return super().shadow

        @shadow.setter
        def shadow(self, shadow: float):
            for shape in self._composition:
                shape.style.shadow = shadow

    _shapes: dict

    def __init__(self, shapes: dict):
        """shapes: list or dict of Shape objects."""
        super().__init__()
        self._shapes = shapes
        self._style = self.CompositionStyle(self)

    def __iter__(self):
        return self._shapes.values().__iter__()

    def add(self, key: str, shape: Shape) -> "Composition":
        """Provides a copy of the composition with the requisite shape added"""
        shapes = self._shapes.copy()
        shapes[key] = shape
        return Composition(shapes)

    def __setitem__(self, key: str, value: Shape) -> "Composition":
        return self.add(key, value)

    def __getitem__(self, name):
        return self._shapes[name]

    def _for_all_shapes(self, func: str, *args, **kwargs) -> "Composition":
        shapes = dict()
        for key, shape in self._shapes.items():
            shapes[key] = getattr(shape, func)(*args, **kwargs)
        return Composition(shapes)

    def rotate(self, angle: float, center: Point) -> "Composition":
        return self._for_all_shapes("rotate", angle, center)

    def translate(self, vec) -> "Composition":
        return self._for_all_shapes("translate", vec)

    def scale(self, factor) -> "Composition":
        return self._for_all_shapes("scale", factor)

    def apply(self, func: Callable[[Union[Shape, "Composition"]], T]) -> Dict[str, T]:
        ret_dict = {}
        for key, shape in self._shapes.items():
            ret_dict[key] = func(shape)
        return ret_dict


class ShapeWithText(Composition):
    def __init__(self, shape: Shape, text: Text):
        super().__init__({"text": text, "shape": shape})
