from pysketcher import Arrow, DoubleArrow, Figure, Point
from pysketcher.backend.matplotlib import MatplotlibBackend

fig = Figure(0, 5, 0, 5, backend=MatplotlibBackend)

arrow = Arrow(Point(1, 2), Point(4, 3))
arrow2 = DoubleArrow(Point(2, 1), Point(3, 4))

fig.add(arrow)
fig.add(arrow2)
fig.show()
