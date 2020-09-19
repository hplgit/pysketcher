from pysketcher import *
from numpy import exp, linspace

W = 10.0
H = 10.0

drawing_tool._set_coordinate_system(
    xmin=-1, xmax=W + 1, ymin=-1, ymax=H + 1, axis=False
)
drawing_tool.set_linecolor("black")
drawing_tool.set_fontsize(24)

a = [0, 1.5, 3, 4.5, 6, 8.2, 10]
layers = {"layer%d" % i: Line((0, a[i]), (W, a[i])) for i in range(len(a))}
symbols_ell = {
    "l_%d" % i: Text("$\ell_%d$" % i, (-0.5, a[i])) for i in range(1, len(a) - 1)
}
symbols_a = {
    "a_%d" % i: Text("$a_%d$" % i, (W / 2, 0.5 * (a[i] + a[i + 1])))
    for i in range(len(a) - 1)
}

sides = {"left": Line((0, 0), (0, H)), "right": Line((W, 0), (W, H))}
d = sides.copy()
d.update(layers)
d.update(symbols_ell)
d.update(symbols_a)
fig = Composition(d)

fig.draw()
drawing_tool.display()
drawing_tool.savefig("tmp1")

input()
