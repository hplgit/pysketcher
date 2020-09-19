from pysketcher import MatplotlibDraw, Rectangle, Style, Composition, Point
import logging

drawing_tool = MatplotlibDraw(xmin=0, xmax=20, ymin=0, ymax=12, axis=False)

i = 1
shapes = Composition(dict())
for fill_pattern in Style.FillPattern:
    logging.info("Fill Pattern: %s", fill_pattern)
    name: str = "Rectangle.%d" % i
    rectangle = Rectangle(Point(i, 1), 1, 1).set_fill_pattern(fill_pattern)
    shapes = shapes.add(name, rectangle)
    i = i + 1.5

shapes.draw(drawing_tool)
drawing_tool.display()
