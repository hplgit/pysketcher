import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend

code = ps.Rectangle(ps.Point(4, 4), 10, 15)
# code.draw_dimensions(drawing_tool)
model = ps.Composition(dict(text=code))

fig = ps.Figure(0, 20, 0, 20, backend=MatplotlibBackend)
fig.add(model)
fig.show()
