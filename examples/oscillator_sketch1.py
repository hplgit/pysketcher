"""Draw mechanical vibration system."""

import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend

L = 12.0
H = L / 6
W = L / 6

xmax = L
x = 0


def make_dashpot(x):
    d_start = (-L, 2 * H)
    d = ps.Dashpot(
        start=d_start,
        total_length=L + x,
        width=W,
        bar_length=3 * H / 2,
        dashpot_length=L / 2,
        piston_pos=H + x,
    )
    d.rotate(-90, d_start)
    return d


def make_spring(x):
    s_start = (-L, 4 * H)
    s = ps.Spring(start=s_start, length=L + x, bar_length=3 * H / 2, teeth=True)
    s.rotate(-90, s_start)
    return s


d = make_dashpot(0)
s = make_spring(0)

M = ps.Rectangle(ps.Point(0, H), 4 * H, 4 * H).set_linewidth(4)
left_wall = ps.Rectangle(ps.Point(-L, 0), H / 10, L).set_filled_curves(pattern="/")
ground = ps.Wall([ps.Point(-L / 2, 0), ps.Point(L, 0)], thickness=-H / 10)
wheel1 = ps.Circle(ps.Point(H, H / 2), H / 2)
wheel2 = wheel1.translate(ps.Point(2 * H, 0))

fontsize = 18
text_m = ps.Text("$m$", ps.Point(2 * H, H + 2 * H))
text_ku = ps.Text("$ku$", ps.Point(-L / 2, H + 4 * H))
text_bv = ps.Text("$bu'$", ps.Point(-L / 2, H))
x_axis = ps.Axis(ps.Point(2 * H, L), H, "$u(t)$", label_spacing=(0.04, -0.01))
x_axis_start = ps.Line(
    ps.Point(2 * H, L - H / 4), ps.Point(2 * H, L + H / 4)
).set_linewidth(4)

model = ps.Composition(
    {
        "spring": s,
        "mass": M,
        "left wall": left_wall,
        "ground": ground,
        "wheel1": wheel1,
        "wheel2": wheel2,
        "text_m": text_m,
        "text_ku": text_ku,
        "x_axis": x_axis,
        "x_axis_start": x_axis_start,
    }
)

fig = ps.Figure(-L, xmax, -1, L + H, backend=MatplotlibBackend)
fig.add(model)
fig.show()

drawing_tool.erase()

fig["dashpot"] = d
fig["text_bv"] = text_bv

# or fig = Composition(dict(fig=fig, dashpot=d, text_bv=text_bv))
fig.show()

# drawing_tool.display()
# drawing_tool.savefig("tmp_oscillator")
#
# drawing_tool.erase()
#
# text_ku = Text("$ku$", (-L / 2, H + 4 * H), fontsize=fontsize)
# text_bv = Text("$bu'$", (-L / 2, H), fontsize=fontsize)
# x_axis = Axis((2 * H, L), H, "$u(t)$", fontsize=fontsize, label_spacing=(0.04, -0.01))
# F_force = Force(
#     (4 * H, H + 2 * H),
#     (4 * H + H, H + 2 * H),
#     "$F(t)$",
#     text_spacing=(0.057, -0.007),
#     text_alignment="left",
#     fontsize=fontsize,
# )
# fig["text_ku"] = text_ku
# fig["text_bv"] = text_bv
# fig["x_axis"] = x_axis
# fig["F_force"] = F_force
# fig.draw()
# drawing_tool.savefig("tmp_oscillator_general")
#
# raw_input()
