"""Illustrate forward, backward and centered finite differences in four figures."""

import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend


def main() -> None:
    xaxis = 2

    f = ps.SketchyFunc1("$u(t)$")
    x = 3  # center point where we want the derivative
    xb = 2  # x point used for backward difference
    xf = 4  # x point used for forward difference
    p = ps.Point(x, f(x))  # center point
    pf = ps.Point(xf, f(xf))  # forward point
    pb = ps.Point(xb, f(xb))  # backward point
    r = 0.1  # radius of circles placed at key points
    c = ps.Circle(p, r).set_line_color(ps.Style.Color.BLUE)
    cf = ps.Circle(pf, r).set_line_color(ps.Style.Color.RED)
    cb = ps.Circle(pb, r).set_line_color(ps.Style.Color.GREEN)

    # Points in the mesh
    p0 = ps.Point(x, xaxis)  # center point
    pf0 = ps.Point(xf, xaxis)  # forward point
    pb0 = ps.Point(xb, xaxis)  # backward point
    tick = 0.05

    axis = ps.Composition(
        {
            "hline": ps.Line(pf0 - ps.Point(3, 0), pb0 + ps.Point(3, 0))
            .set_line_color(ps.Style.Color.BLACK)
            .set_line_width(1),
            "tick_m1": ps.Line(pf0 + ps.Point(0, tick), pf0 - ps.Point(0, tick))
            .set_line_color(ps.Style.Color.BLACK)
            .set_line_width(1),
            "tick_n": ps.Line(p0 + ps.Point(0, tick), p0 - ps.Point(0, tick))
            .set_line_color(ps.Style.Color.BLACK)
            .set_line_width(1),
            "tick_p1": ps.Line(pb0 + ps.Point(0, tick), pb0 - ps.Point(0, tick))
            .set_line_color(ps.Style.Color.BLACK)
            .set_line_width(1),
        }
    )

    # 1D mesh with three points
    mesh = ps.Composition(
        {
            "tnm1": ps.Text("$t_{n-1}$", pb0 - ps.Point(0, 0.3)),
            "tn": ps.Text("$t_{n}$", p0 - ps.Point(0, 0.3)),
            "tnp1": ps.Text("$t_{n+1}$", pf0 - ps.Point(0, 0.3)),
            "axis": axis,
        }
    )

    # 1D mesh with three points for Crank-Nicolson
    mesh_cn = ps.Composition(
        {
            "tnm1": ps.Text("$t_{n}$", pb0 - ps.Point(0, 0.3)),
            "tn": ps.Text(r"$t_{n+\frac{1}{2}}$", p0 - ps.Point(0, 0.3)),
            "tnp1": ps.Text("$t_{n+1}$", pf0 - ps.Point(0, 0.3)),
            "axis": axis,
        }
    )

    # Vertical dotted lines at each mesh point
    vlinec = (
        ps.Line(p, p0)
        .set_line_style(ps.Style.LineStyle.DOTTED)
        .set_line_color(ps.Style.Color.BLUE)
        .set_line_width(1)
    )
    vlinef = (
        ps.Line(pf, pf0)
        .set_line_style(ps.Style.LineStyle.DOTTED)
        .set_line_color(ps.Style.Color.RED)
        .set_line_width(1)
    )
    vlineb = (
        ps.Line(pb, pb0)
        .set_line_style(ps.Style.LineStyle.DOTTED)
        .set_line_color(ps.Style.Color.GREEN)
        .set_line_width(1)
    )

    # Compose vertical lines for each type of difference
    forward_lines = ps.Composition({"center": vlinec, "right": vlinef})
    backward_lines = ps.Composition({"center": vlinec, "left": vlineb})
    centered_lines = ps.Composition({"left": vlineb, "right": vlinef, "center": vlinec})

    # Tangents illustrating the derivative
    domain = (1.0, 5.0)
    domain2 = (2.0, 5.0)
    forward_tangent = (
        ps.Line(p, pf)
        .interval(x_range=domain2)
        .set_line_style(ps.Style.LineStyle.DASHED)
        .set_line_color(ps.Style.Color.RED)
    )
    backward_tangent = (
        ps.Line(pb, p)
        .interval(x_range=domain)
        .set_line_style(ps.Style.LineStyle.DASHED)
        .set_line_color(ps.Style.Color.GREEN)
    )
    centered_tangent = (
        ps.Line(pb, pf)
        .interval(x_range=domain)
        .set_line_style(ps.Style.LineStyle.DASHED)
        .set_line_color(ps.Style.Color.BLUE)
    )
    h = 1e-3  # h in finite difference approx used to compute the exact tangent
    exact_tangent = (
        ps.Line(ps.Point(x + h, f(x + h)), ps.Point(x - h, f(x - h)))
        .interval(x_range=domain)
        .set_line_style(ps.Style.LineStyle.DOTTED)
        .set_line_color(ps.Style.Color.BLACK)
    )

    forward = ps.Composition(
        dict(
            tangent=forward_tangent,
            point1=c,
            point2=cf,
            coor=forward_lines,
            name=ps.Text("forward", forward_tangent.end + ps.Point(0.1, 0)),
        )
    )
    backward = ps.Composition(
        dict(
            tangent=backward_tangent,
            point1=c,
            point2=cb,
            coor=backward_lines,
            name=ps.Text(
                "backward", backward_tangent.end + ps.Point(0.1, 0)
            ).set_alignment(ps.TextStyle.Alignment.LEFT),
        )
    )
    centered = ps.Composition(
        dict(
            tangent=centered_tangent,
            point1=cb,
            point2=cf,
            point=c,
            coor=centered_lines,
            name=ps.Text(
                "centered", centered_tangent.end + ps.Point(0.1, 0)
            ).set_alignment(ps.TextStyle.Alignment.LEFT),
        )
    )

    exact = ps.Composition(dict(graph=f, tangent=exact_tangent))
    forward = ps.Composition(dict(difference=forward, exact=exact))
    backward = ps.Composition(dict(difference=backward, exact=exact))
    centered = ps.Composition(dict(difference=centered, exact=exact))

    fig = ps.Figure(0.0, 7.0, 1.0, 6.0, backend=MatplotlibBackend)

    for model in forward, backward, centered:
        fig.erase()
        fig.add(model)
        fig.add(mesh)
        fig.show()

    # Crank-Nicolson around t_n+1/2
    fig.erase()
    fig.add(centered)
    fig.add(mesh_cn)
    fig.show()


if __name__ == "__main__":
    main()
