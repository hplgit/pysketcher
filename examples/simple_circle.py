import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend

circle = ps.Circle(ps.Point(2.5, 2.5), 1.5)

fig = ps.Figure(0, 5, 0, 5, backend=MatplotlibBackend)
fig.add(circle)
fig.show()
