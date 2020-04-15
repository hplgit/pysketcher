from pysketcher import MatplotlibDraw, Point, Triangle, Composition

drawing_tool = MatplotlibDraw(
    xmin=0, xmax=5, ymin=0, ymax=5, axis=False)
drawing_tool.set_linecolor('black')

code = Triangle(Point(1, 1), Point(1, 4), Point(3, 3), drawing_tool)
fig = Composition(dict(text=code), drawing_tool)

fig.draw()
drawing_tool.display()
