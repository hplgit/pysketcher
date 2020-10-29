import numpy as np
from pysketcher import MatplotlibDraw, Point, Arc, Composition

drawing_tool = MatplotlibDraw(xmin=0, xmax=5, ymin=0, ymax=5, axis=False)
drawing_tool.set_linecolor("black")

code = Arc(Point(2.5, 2.5), 1.5, np.pi / 2, np.pi / 2)
fig = Composition(dict(text=code))

fig.draw(drawing_tool)
drawing_tool.display()
