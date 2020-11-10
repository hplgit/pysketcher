import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend

code = ps.Spline(
    [ps.Point(0, 0), ps.Point(1, 1), ps.Point(2, 4), ps.Point(3, 9), ps.Point(4, 16)]
)
model = ps.Composition(dict(text=code))

fig = ps.Figure(0, 5, 0, 16, backend=MatplotlibBackend)
fig.add(model)
fig.show()
