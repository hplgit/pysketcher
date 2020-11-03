import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend

model = ps.Triangle(ps.Point(1, 1), ps.Point(1, 4), ps.Point(3, 3))

fig = ps.Figure(0, 5, 0, 5, backend=MatplotlibBackend)
fig.add(model)
fig.show()
