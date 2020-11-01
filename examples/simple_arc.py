import numpy as np

from pysketcher import Angle, Arc, Figure, Point
from pysketcher.backend.matplotlib.matplotlib_backend import MatplotlibBackend

fig = Figure(0.0, 5.0, 0.0, 5.0, MatplotlibBackend)

code = Arc(Point(2.5, 2.5), 1.5, Angle(np.pi / 2), Angle(np.pi / 2))

fig.add(code)
fig.show()
