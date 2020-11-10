import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend

L = 12.0
H = L / 6.0
start = ps.Point(0, 0)
s = ps.Spring(start, L)
fig = ps.Figure(-4, 4, -1, L + H, backend=MatplotlibBackend)
fig.add(s)
fig.show()
