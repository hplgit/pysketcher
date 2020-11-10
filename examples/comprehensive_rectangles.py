import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend

rect = ps.Rectangle(ps.Point(4, 4), 10, 15)

fig = ps.Figure(0, 20, 0, 20, backend=MatplotlibBackend)
fig.add(rect)
fig.show()
