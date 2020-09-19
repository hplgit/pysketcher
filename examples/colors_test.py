from pysketcher import MatplotlibDraw, Rectangle, Style, Composition, Point
import logging

logging.basicConfig(level=logging.INFO)
drawing_tool = MatplotlibDraw(xmin=0, xmax=12, ymin=0, ymax=12, axis=False)

i = 1
shapes = Composition(dict())
for line_color in Style.Color:
    j = 1
    for fill_color in Style.Color:
        logging.info("Line Color: %s", line_color)
        name: str = "Rectangle.%d.%d" % (i, j)
        rectangle = Rectangle(Point(i, j), 1, 1)
        rectangle.style.line_width = 3.0
        rectangle.style.line_color = line_color
        rectangle.style.fill_color = fill_color
        shapes = shapes.add(name, rectangle)
        j = j + 1
    i = i + 1

shapes.draw(drawing_tool)
drawing_tool.display()
