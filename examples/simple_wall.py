import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend

model = ps.Wall(
    [ps.Point(1, 1), ps.Point(2, 2), ps.Point(3, 2.5), ps.Point(4, 2), ps.Point(5, 1)],
    0.1,
)

fig = ps.Figure(0, 6, 0, 3, backend=MatplotlibBackend)
fig.add(model)
fig.show()
