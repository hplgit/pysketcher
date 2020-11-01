from abc import ABC, abstractmethod
from typing import Any

from matplotlib.axes import Axes

from pysketcher.drawable import Drawable


class MatplotlibAdapter(ABC):
    @staticmethod
    @abstractmethod
    def plot(shape: Drawable, axes: Axes):
        pass
