from matplotlib.axes import Axes

from pysketcher.backend.matplotlib._matplotlib_adapter import MatplotlibAdapter
from pysketcher.composition import Composition


class MatplotlibComposition(MatplotlibAdapter):
    def __init__(self, mplb):
        self._mplb = mplb

    def plot(self, shape: Composition, axes: Axes):
        shape.apply(self._mplb.add)
