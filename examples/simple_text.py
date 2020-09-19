import logging
from pysketcher import Point, Text, Composition, TextStyle, MatplotlibDraw

logging.basicConfig(level=logging.INFO)

drawing_tool = MatplotlibDraw(xmin=0, xmax=6, ymin=0, ymax=6, axis=False)

code = Text("This is some left text!", Point(3, 1))
code.style.alignment = TextStyle.Alignment.LEFT
code.style.line_color = TextStyle.Color.BLUE
code.style.font_size = TextStyle.FontSize.MEDIUM
code.style.font_family = TextStyle.FontFamily.SERIF

code1 = Text("This is some right text!", Point(3, 2))
code1.style.alignment = TextStyle.Alignment.RIGHT
code1.style.line_color = TextStyle.Color.GREEN
code1.style.font_size = TextStyle.FontSize.MEDIUM
code1.style.font_family = TextStyle.FontFamily.SANS

code2 = Text("This is some center text!", Point(3, 3))
code2.style.alignment = TextStyle.Alignment.CENTER
code2.style.line_color = TextStyle.Color.RED
code2.style.font_size = TextStyle.FontSize.MEDIUM
code2.style.font_family = TextStyle.FontFamily.MONO

fig = Composition(dict(text=code, text1=code1, text2=code2))

fig.draw(drawing_tool)
drawing_tool.display()
