import pysketcher
from pysketcher import Point, Text, Composition

drawing_tool = pysketcher.MatplotlibDraw(
    xmin=0, xmax=6, ymin=0, ymax=6, axis=False)
drawing_tool.set_linecolor('black')

code = Text("This is some text!", Point(3, 3), drawing_tool)
fig = Composition(dict(text=code), drawing_tool)

fig.draw()
drawing_tool.display()
