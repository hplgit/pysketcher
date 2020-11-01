from matplotlib.axes import Axes

from pysketcher.backend.matplotlib.matplotlib_adapter import MatplotlibAdapter
from pysketcher.composition import Composition


class MatplotlibComposition(MatplotlibAdapter):

    _mplb: "MatplotlibBackend"

    def __init__(self, mplb: "MatplotlibBackend"):
        self._mplb = mplb

    def plot(self, shape: Composition, axes: Axes):
        shape.apply(self._mplb.add)
