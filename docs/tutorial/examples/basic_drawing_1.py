import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend

figure = ps.Figure(0.0, 5.0, 0.0, 5.0, MatplotlibBackend)

a = ps.Point(1.0, 3.0)
b = ps.Point(4.0, 3.0)

line = ps.Line(a, b)
figure.add(line)
figure.show()


# End Here
import os  # noqa: E402, I100

from .utils.change_extension import change_extension  # noqa: E402

filename = change_extension(__file__, "png")
figure.save(os.path.join("images", filename))
