import logging
from typing import Dict, Type

import matplotlib.pyplot as plt

from pysketcher.backend.backend import Backend
from pysketcher.backend.matplotlib.matplotlib_adapter import MatplotlibAdapter
from pysketcher.backend.matplotlib.matplotlib_composition import MatplotlibComposition
from pysketcher.backend.matplotlib.matplotlib_curve import MatplotlibCurve
from pysketcher.backend.matplotlib.matplotlib_text import MatplotlibText
from pysketcher.composition import Composition
from pysketcher.curve import Curve
from pysketcher.drawable import Drawable
from pysketcher.text import Text


class MatplotlibBackend(Backend):
    """
    Simple interface for plotting. This interface makes use of
    Matplotlib for plotting.

    """

    _fig: plt.Figure
    _axes: plt.Axes

    def __init__(self, x_min, x_max, y_min, y_max):
        plt.ion()
        self._fig = plt.figure(
            figsize=[x_max - x_min, y_max - y_min], tight_layout=False
        )
        self._axes = self._fig.gca()
        self._axes.set_xlim(x_min, x_max)
        self._axes.set_ylim(y_min, y_max)
        self._axes.set_axis_off()

    def add(self, shape: Drawable) -> None:
        for typ, adapter in self._adapters.items():
            if issubclass(shape.__class__, typ):
                adapter.plot(shape, self._axes)

    def erase(self):
        """Erase the current figure."""
        raise NotImplementedError

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

    # def arrow2(self, x, y, dx, dy, style="->"):
    #     """Draw arrow (dx,dy) at (x,y). `style` is '->', '<-' or '<->'."""
    #     self.ax.annotate(
    #         "",
    #         xy=(x + dx, y + dy),
    #         xytext=(x, y),
    #         arrowprops=dict(
    #             arrowstyle=style, facecolor="black", linewidth=1, shrinkA=0, shrinkB=0
    #         ),
    #     )
