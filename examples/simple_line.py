import pysketcher
from pysketcher import Point, Line, Composition

drawing_tool = pysketcher.MatplotlibDraw(
    xmin=0, xmax=5, ymin=0, ymax=5, axis=False)
drawing_tool.set_linecolor('black')

code = Line(Point(1, 2), Point(4, 3), drawing_tool)
fig = Composition(dict(text=code), drawing_tool)

fig.draw()
drawing_tool.display()
