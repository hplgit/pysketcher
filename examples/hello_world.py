"""Minimialistic pysketcher example."""
from pysketcher import MatplotlibDraw, Composition, Text, Point, TextStyle

drawing_tool = MatplotlibDraw(xmin=0, xmax=5, ymin=0, ymax=3, axis=False)

code = Text("print 'Hello, World!'", Point(2.5, 1.5))

code.style.fontsize = 24
code.style.font_family = TextStyle.FontFamily.MONO
code.style.fill_color = TextStyle.Color.GREY

code.draw(drawing_tool)
drawing_tool.display()
