import logging
from typing import Callable, Dict, Optional, Tuple, Type, Union

from celluloid import Camera
from matplotlib.animation import ArtistAnimation
import matplotlib.pyplot as plt

from pysketcher._curve import Curve
from pysketcher._drawable import Drawable
from pysketcher._text import Text
from pysketcher.backend.backend import Backend
from pysketcher.backend.matplotlib._matplotlib_adapter import MatplotlibAdapter
from pysketcher.backend.matplotlib._matplotlib_composition import MatplotlibComposition
from pysketcher.backend.matplotlib._matplotlib_curve import MatplotlibCurve
from pysketcher.backend.matplotlib._matplotlib_text import MatplotlibText
from pysketcher.composition import Composition


# plt.rc("text", usetex=True)
# plt.rcParams["text.latex.preamble"] = r"\usepackage{amsmath}"


class MatplotlibBackend(Backend):
    """Simple interface for plotting. Makes use of Matplotlib for plotting."""

    _fig: plt.Figure
    _axes: plt.Axes
    _camera: Optional[Camera]
    _x_min: float
    _y_min: float
    _x_max: float
    _y_max: float

    _INTERVAL: int = 40  # ms between each frame

    def __init__(self, x_min, x_max, y_min, y_max):
        plt.ion()
        self._x_min = x_min
        self._x_max = x_max
        self._y_min = y_min
        self._y_max = y_max
        self._camera = None
        self._fig = plt.figure(
            figsize=[(x_max - x_min) * 3, (y_max - y_min) * 3], tight_layout=False
        )
        self._axes = self._fig.gca()
        self._configure_axes()

    def _configure_axes(self):
        self._axes.set_xlim(self._x_min, self._x_max)
        self._axes.set_ylim(self._y_min, self._y_max)
        self._axes.set_aspect("equal")
        self._axes.set_axis_off()

    def add(self, shape: Drawable) -> None:
        for typ, adapter in self._adapters.items():
            if issubclass(shape.__class__, typ):
                adapter.plot(shape, self._axes)

    def erase(self):
        self._fig.clear()
        self._axes = self._fig.gca()
        self._configure_axes()

    def show(self):
        self._fig.sca(self._axes)
        self._fig.canvas.draw()
        self._fig.show()

    def save(self, filename: str) -> None:
        logging.info(f"Saving to {filename}.")
        # TODO: manage formats
        self._fig.savefig(filename)

    @property
    def _adapters(self) -> Dict[Type, MatplotlibAdapter]:
        return {
            Curve: MatplotlibCurve(),
            Text: MatplotlibText(),
            Composition: MatplotlibComposition(self),
        }

    def animate(
        self,
        func: Callable[[float], Drawable],
        interval: Union[Tuple[float, float], Tuple[float, float, float]],
    ):
        if len(interval) == 2:
            start, end = interval
            increment = 1
        else:
            start, end, increment = interval
        self._camera = Camera(self._fig)
        i: float = start
        while i < end:
            self.add(func(i))
            self._camera.snap()
            i += increment

    def show_animation(self):
        animation: ArtistAnimation = self._camera.animate(interval=self._INTERVAL)
        animation.show()

    def save_animation(self, filename: str):
        animation: ArtistAnimation = self._camera.animate(interval=self._INTERVAL)
        animation.save(filename)
