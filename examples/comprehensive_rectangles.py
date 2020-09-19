from pysketcher import MatplotlibDraw, Point, Rectangle, Composition

drawing_tool = MatplotlibDraw(xmin=0, xmax=20, ymin=0, ymax=20, axis=False)

code = Rectangle(Point(4, 4), 10, 15)
code.draw_dimensions(drawing_tool)
fig = Composition(dict(text=code))

fig.draw(drawing_tool)
drawing_tool.display()
