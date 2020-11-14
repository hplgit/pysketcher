from abc import ABC, abstractmethod

from matplotlib.axes import Axes

from pysketcher.drawable import Drawable


class MatplotlibAdapter(ABC):
    @staticmethod
    @abstractmethod
    def plot(shape: Drawable, axes: Axes):
        pass
