from pysketcher import Figure, Point, Text, TextStyle
from pysketcher.backend.matplotlib import MatplotlibBackend

fig = Figure(0.0, 6.0, 0.0, 6.0, MatplotlibBackend)

code = Text("This is some left text!", Point(3, 2))
code.style.alignment = TextStyle.Alignment.LEFT
code.style.line_color = TextStyle.Color.BLUE
code.style.font_family = TextStyle.FontFamily.SERIF

code1 = Text("This is some right text!", Point(3, 3))
code1.style.alignment = TextStyle.Alignment.RIGHT
code1.style.line_color = TextStyle.Color.GREEN
code1.style.font_family = TextStyle.FontFamily.SANS

code2 = Text("This is some center text!", Point(3, 4))
code2.style.alignment = TextStyle.Alignment.CENTER
code2.style.line_color = TextStyle.Color.RED
code2.style.font_family = TextStyle.FontFamily.MONO

fig.add(code)
fig.add(code1)
fig.add(code2)

fig.show()
