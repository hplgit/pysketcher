from .point import Point
from .shape import Shape


class Composition(Shape):
    def __init__(self, shapes: dict):
        """shapes: list or dict of Shape objects."""
        super().__init__()
        self._shapes = shapes

    def add(self, key: str, shape: Shape) -> 'Composition':
        shapes = self._shapes.copy()
        shapes[key] = shape
        return Composition(shapes)

    def __setitem__(self, key: str, value: Shape) -> 'Composition':
        return self.add(key, value)

    def rotate(self, angle: float, center: Point):
        shapes = dict()
        for key, shape in self._shapes:
            shapes[key] = shape.rotate(angle, center)
        return Composition(shapes)

