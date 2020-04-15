from pysketcher import MatplotlibDraw, Point, Rectangle, Composition

drawing_tool = MatplotlibDraw(
    xmin=0, xmax=20, ymin=0, ymax=20, axis=False)
drawing_tool.set_linecolor('black')

code = Rectangle(Point(4, 4), 10, 15, drawing_tool)
code.draw_dimensions()
fig = Composition(dict(text=code), drawing_tool)

fig.draw()
drawing_tool.display()
