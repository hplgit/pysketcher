from pysketcher.drawing_tool import DrawingTool
from .point import Point
from .shape import Shape
from .style import Style, TextStyle
from .text import Text


class Composition(Shape):

    _shapes: dict

    def __init__(self, shapes: dict):
        """shapes: list or dict of Shape objects."""
        super().__init__()
        self._shapes = shapes

    def add(self, key: str, shape: Shape) -> "Composition":
        shapes = self._shapes.copy()
        shapes[key] = shape
        return Composition(shapes)

    def __setitem__(self, key: str, value: Shape) -> "Composition":
        return self.add(key, value)

    def __getitem__(self, name):
        return self._shapes[name]

    def draw(self, drawing_tool: DrawingTool) -> None:
        for shape in self._shapes.values():
            shape.draw(drawing_tool)

    def _for_all_shapes(self, func: str, *args, **kwargs) -> "Composition":
        shapes = dict()
        for key, shape in self._shapes:
            shapes[key] = getattr(shape, func)(*args, **kwargs)
        return Composition[shapes]

    def rotate(self, angle: float, center: Point) -> "Composition":
        return self._for_all_shapes("rotate", angle, center)

    def translate(self, vec) -> "Shape":
        return self._for_all_shapes("translate", vec)

    def scale(self, factor) -> "Shape":
        return self._for_all_shapes("scale", factor)


class ShapeWithText(Composition):
    def __init__(self, shape: Shape, text: Text):
        super().__init__({"text": text, "shape": shape})

    @property
    def style(self) -> Style:
        return self["shape"].style

    @style.setter
    def style(self, style: Style):
        self["shape"].style = style

    @property
    def text_style(self) -> TextStyle:
        return self["text"].style

    @text_style.setter
    def text_style(self, text_style: TextStyle):
        self["text"].style = text_style
