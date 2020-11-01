from typing import List, Type, Union

import numpy as np

from pysketcher.backend.backend import Backend
from pysketcher.backend.matplotlib.matplotlib_backend import MatplotlibBackend
from pysketcher.drawable import Drawable


class Figure:
    _shapes: List[Drawable]
    _backend: Backend

    def __init__(
        self,
        x_min: np.float64,
        x_max: np.float64,
        y_min: np.float64,
        y_max: np.float64,
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
