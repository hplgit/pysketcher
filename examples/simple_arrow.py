import pysketcher
from pysketcher import Point, Arrow, Composition

drawing_tool = pysketcher.MatplotlibDraw(xmin=0, xmax=5, ymin=0, ymax=5, axis=False)

code = Arrow(Point(1, 2), Point(4, 3))
fig = Composition(dict(text=code))

fig.draw(drawing_tool)
drawing_tool.display()
