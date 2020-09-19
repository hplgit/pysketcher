import pysketcher
from pysketcher import Point, Spline, Composition

drawing_tool = pysketcher.MatplotlibDraw(xmin=0, xmax=5, ymin=0, ymax=16, axis=False)

code = Spline([Point(0, 0), Point(1, 1), Point(2, 4), Point(3, 9), Point(4, 16)])
fig = Composition(dict(text=code))

fig.draw(drawing_tool)
drawing_tool.display()
