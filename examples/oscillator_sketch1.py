"""Draw mechanical vibration system."""

import numpy as np

import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend

L = 12.0
H = L / 6
W = L / 6

x_max = L
x = 0


def make_dashpot(x):
    d_start = ps.Point(-L, 2 * H)
    d = ps.Dashpot(
        start=d_start,
        total_length=L + x,
        width=W,
        bar_length=3 * H / 2,
        dashpot_length=L / 2,
        piston_pos=H + x,
    )
    d = d.rotate(-np.pi / 2, d_start)
    return d


def make_spring(x):
    s_start = ps.Point(-L, 4 * H)
    s = ps.Spring(start=s_start, length=L + x, bar_length=3 * H / 2)
    s = s.rotate(-np.pi / 2, s_start)
    return s


def main() -> None:
    d = make_dashpot(0)
    s = make_spring(0)

    M = ps.Rectangle(ps.Point(0, H), 4 * H, 4 * H).set_line_width(4)
    left_wall = ps.Rectangle(ps.Point(-L, 0), H / 10, L).set_fill_pattern(
        ps.Style.FillPattern.UP_LEFT_TO_RIGHT
    )
    ground = ps.Wall([ps.Point(-L / 2, 0), ps.Point(L, 0)], thickness=-H / 10)
    wheel1 = ps.Circle(ps.Point(H, H / 2), H / 2)
    wheel2 = wheel1.translate(ps.Point(2 * H, 0))

    fontsize = 24
    text_m = ps.Text("$m$", ps.Point(2 * H, H + 2 * H))
    text_m.style.font_size = fontsize
    text_ku = ps.Text("$ku$", ps.Point(-L / 2, H + 4 * H))
    text_ku.style.font_size = fontsize
    text_bv = ps.Text("$bu'$", ps.Point(-L / 2, H))
    text_bv.style.font_size = fontsize
    x_axis = ps.Axis(ps.Point(2 * H, L), H, "$u(t)$")
    x_axis_start = ps.Line(
        ps.Point(2 * H, L - H / 4), ps.Point(2 * H, L + H / 4)
    ).set_line_width(4)

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

    fig = ps.Figure(-L, x_max, -1, L + H, backend=MatplotlibBackend)
    fig.add(model)

    damping = ps.Composition({"dashpot": d, "text_bv": text_bv})

    # or fig = Composition(dict(fig=fig, dashpot=d, text_bv=text_bv))
    fig.add(damping)
    fig.show()


if __name__ == "__main__":
    main()
