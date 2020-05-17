import numpy as np
from pysketcher import MatplotlibDraw, Point, Line, Composition

drawing_tool = MatplotlibDraw(
    xmin=0, xmax=5, ymin=0, ymax=5, axis=False)
drawing_tool.set_linecolor('black')

code = Line(Point(1, 2), Point(4, 3))
code2 = code.rotate(np.pi / 2, Point(1, 2))
fig = Composition(dict(line=code, line2=code2))

fig.draw(drawing_tool)
drawing_tool.display()
