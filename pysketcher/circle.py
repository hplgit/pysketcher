import numpy as np

from .arc import Arc
from .matplotlibdraw import MatplotlibDraw
from .point import Point


class Circle(Arc):
    def __init__(self, center: Point, radius: float, resolution=180):
        super().__init__(center, radius, 0, 2 * np.pi, resolution)
