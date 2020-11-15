import numpy as np

from pysketcher._arc import Arc
from pysketcher._point import Point


class Circle(Arc):
    def __init__(self, center: Point, radius: float, resolution=180):
        super().__init__(center, radius, 0, 2 * np.pi, resolution)
