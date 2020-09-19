from pysketcher import Point, Arrow, Composition, MatplotlibDraw, Axis
import logging

logging.basicConfig(level=logging.INFO)

drawing_tool = MatplotlibDraw(xmin=0, xmax=5, ymin=0, ymax=5, axis=False)

code = Axis(Point(1, 1), 3, "x")
code2 = Axis(Point(1, 1), 3, "y")
fig = Composition(dict(x=code, y=code2))

fig.draw(drawing_tool)
drawing_tool.display()
