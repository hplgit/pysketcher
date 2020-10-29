import pysketcher
from pysketcher import Composition, Point, Wall

drawing_tool = pysketcher.MatplotlibDraw(xmin=0, xmax=6, ymin=0, ymax=3, axis=False)

code = Wall([Point(1, 1), Point(2, 2), Point(3, 2.5), Point(4, 2), Point(5, 1)], 0.1)
fig = Composition(dict(text=code))

fig.draw(drawing_tool)
drawing_tool.display()
