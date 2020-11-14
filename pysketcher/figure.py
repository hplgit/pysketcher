from typing import List, Type

from pysketcher.backend.backend import Backend
from pysketcher.drawable import Drawable


class Figure:
    _shapes: List[Drawable]
    _backend: Backend

    def __init__(
        self,
        x_min: float,
        x_max: float,
        y_min: float,
        y_max: float,
        backend: Type[Backend],
    ):
        self._backend = backend(x_min, x_max, y_min, y_max)
        self._shapes = []

    def add(self, shape: Drawable) -> None:
        self._shapes.append(shape)
        self._backend.add(shape)

    def show(self):
        self._backend.show()

    def save(self, filename: str) -> None:
        self._backend.save(filename)

    def erase(self):
        self._backend.erase()

    # def animate(
    #     self,
    #     drawing_tool: DrawingTool,
    #     time_points: List[float],
    #     action: Callable[["Shape", float, float], "Shape"],
    #     pause_per_frame: float = 0.5,
    #     dt: float = 0.5,
    #     title=None,
    # ):
    #
    #     for n, t in enumerate(time_points):
    #         drawing_tool.erase()
    #
    #         fig: Shape = action(self, t, dt)
    #         fig.draw(drawing_tool)
