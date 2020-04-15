from .matplotlibdraw import MatplotlibDraw
from .shape import Shape


class Composition(Shape):
    def __init__(self, shapes, drawing_tool: MatplotlibDraw):
        """shapes: list or dict of Shape objects."""
        super().__init__(drawing_tool)
        if isinstance(shapes, (tuple, list)):
            # Convert to dict using the type of the list element as key
            # (add a counter to make the keys unique)
            shapes = {s.__class__.__name__ + '_' + str(i): s
                      for i, s in enumerate(shapes)}
        self._shapes = shapes
