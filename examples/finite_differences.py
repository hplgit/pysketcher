"""
Illustrate forward, backward and centered finite differences
in four figures.
"""

from pysketcher import *

# test_test()
xaxis = 2
drawing_tool = MatplotlibDraw(0, 7, 1, 6, axis=False)

f = SketchyFunc1("$u(t)$")
x = 3  # center point where we want the derivative
xb = 2  # x point used for backward difference
xf = 4  # x point used for forward difference
p = Point(x, f(x))  # center point
pf = Point(xf, f(xf))  # forward point
pb = Point(xb, f(xb))  # backward point
r = 0.1  # radius of circles placed at key points
c = Circle(p, r).set_line_color(Style.Color.BLUE)
cf = Circle(pf, r).set_line_color(Style.Color.RED)
cb = Circle(pb, r).set_line_color(Style.Color.GREEN)

# Points in the mesh
p0 = Point(x, xaxis)  # center point
pf0 = Point(xf, xaxis)  # forward point
pb0 = Point(xb, xaxis)  # backward point
tick = 0.05

axis = Composition(
    {
        "hline": Line(pf0 - Point(3, 0), pb0 + Point(3, 0))
        .set_line_color(Style.Color.BLACK)
        .set_line_width(1),
        "tick_m1": Line(pf0 + Point(0, tick), pf0 - Point(0, tick))
        .set_line_color(Style.Color.BLACK)
        .set_line_width(1),
        "tick_n": Line(p0 + Point(0, tick), p0 - Point(0, tick))
        .set_line_color(Style.Color.BLACK)
        .set_line_width(1),
        "tick_p1": Line(pb0 + Point(0, tick), pb0 - Point(0, tick))
        .set_line_color(Style.Color.BLACK)
        .set_line_width(1),
    }
)

# 1D mesh with three points
mesh = Composition(
    {
        "tnm1": Text("$t_{n-1}$", pb0 - Point(0, 0.3)),
        "tn": Text("$t_{n}$", p0 - Point(0, 0.3)),
        "tnp1": Text("$t_{n+1}$", pf0 - Point(0, 0.3)),
        "axis": axis,
    }
)

# 1D mesh with three points for Crank-Nicolson
mesh_cn = Composition(
    {
        "tnm1": Text("$t_{n}$", pb0 - Point(0, 0.3)),
        "tn": Text(r"$t_{n+\frac{1}{2}}$", p0 - Point(0, 0.3)),
        "tnp1": Text("$t_{n+1}$", pf0 - Point(0, 0.3)),
        "axis": axis,
    }
)

# Vertical dotted lines at each mesh point
vlinec = (
    Line(p, p0)
    .set_line_style(Style.LineStyle.DOTTED)
    .set_line_color(Style.Color.BLUE)
    .set_line_width(1)
)
vlinef = (
    Line(pf, pf0)
    .set_line_style(Style.LineStyle.DOTTED)
    .set_line_color(Style.Color.RED)
    .set_line_width(1)
)
vlineb = (
    Line(pb, pb0)
    .set_line_style(Style.LineStyle.DOTTED)
    .set_line_color(Style.Color.GREEN)
    .set_line_width(1)
)

# Compose vertical lines for each type of difference
forward_lines = Composition({"center": vlinec, "right": vlinef})
backward_lines = Composition({"center": vlinec, "left": vlineb})
centered_lines = Composition({"left": vlineb, "right": vlinef})
centered_lines2 = Composition({"left": vlineb, "right": vlinef, "center": vlinec})

# Tangents illustrating the derivative
domain = (1, 5)
domain2 = (2, 5)
forward_tangent = (
    Line(p, pf)
    .interval(x_range=domain2)
    .set_line_style(Style.LineStyle.DASHED)
    .set_line_color(Style.Color.RED)
)
backward_tangent = (
    Line(pb, p)
    .interval(x_range=domain)
    .set_line_style(Style.LineStyle.DASHED)
    .set_line_color(Style.Color.GREEN)
)
centered_tangent = (
    Line(pb, pf)
    .interval(x_range=domain)
    .set_line_style(Style.LineStyle.DASHED)
    .set_line_color(Style.Color.BLUE)
)
h = 1e-3  # h in finite difference approx used to compute the exact tangent
exact_tangent = (
    Line(Point(x + h, f(x + h)), Point(x - h, f(x - h)))
    .interval(x_range=domain)
    .set_line_style(Style.LineStyle.DOTTED)
    .set_line_color(Style.Color.BLACK)
)

forward = Composition(
    dict(
        tangent=forward_tangent,
        point1=c,
        point2=cf,
        coor=forward_lines,
        name=Text(
            "forward", forward_tangent.geometric_features()["end"] + Point(0.1, 0)
        ),
    )
)
backward = Composition(
    dict(
        tangent=backward_tangent,
        point1=c,
        point2=cb,
        coor=backward_lines,
        name=Text(
            "backward", backward_tangent.geometric_features()["end"] + Point(0.1, 0)
        ).set_alignment(TextStyle.Alignment.LEFT),
    )
)
centered = Composition(
    dict(
        tangent=centered_tangent,
        point1=cb,
        point2=cf,
        point=c,
        coor=centered_lines2,
        name=Text(
            "centered", centered_tangent.geometric_features()["end"] + Point(0.1, 0)
        ).set_alignment(TextStyle.Alignment.LEFT),
    )
)

exact = Composition(dict(graph=f, tangent=exact_tangent))
forward = Composition(dict(difference=forward, exact=exact))
backward = Composition(dict(difference=backward, exact=exact))
centered = Composition(dict(difference=centered, exact=exact))

for fig in forward, backward, centered:
    drawing_tool.erase()
    fig.draw(drawing_tool)
    mesh.draw(drawing_tool)
    drawing_tool.display()

# Crank-Nicolson around t_n+1/2
drawing_tool.erase()
centered.draw(drawing_tool)
mesh_cn.draw(drawing_tool)
drawing_tool.display()
