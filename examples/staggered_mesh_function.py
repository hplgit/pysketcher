from pysketcher import *

Nt = 5

# u = SketchyFunc1()
# t_mesh = linspace(0, 8, Nt+1)

u = SketchyFunc3()
t_mesh = linspace(0, 6, Nt + 1)
t_mesh_staggered = linspace(
    0.5 * (t_mesh[0] + t_mesh[1]), 0.5 * (t_mesh[-2] + t_mesh[-1]), Nt
)

# Add 20% space to the left and 30% to the right of the coordinate system
t_axis_extent = t_mesh[-1] - t_mesh[0]
t_min = t_mesh[0] - 0.2 * t_axis_extent
t_max = t_mesh[-1] + 0.3 * t_axis_extent
u_max = 1.3 * max([u(t) for t in t_mesh])
u_min = -0.2 * u_max

drawing_tool._set_coordinate_system(t_min, t_max, u_min, u_max, axis=False)
drawing_tool.set_linecolor("black")

r = 0.005 * (t_max - t_min)  # radius of circles placed at mesh points
u_discrete = Composition(
    {
        i: Composition(
            dict(
                circle=Circle(point(t, u(t)), r).set_filled_curves("black"),
                u_point=Text(
                    "$u_%d$" % i,
                    point(t, u(t)) + (point(0, 5 * r) if i > 0 else point(-5 * r, 0)),
                ),
            )
        )
        for i, t in enumerate(t_mesh)
    }
)

# u' = v
# v = u.smooth.derivative(n=1)
v = SketchyFunc4()

v_discrete = Composition(
    {
        i: Composition(
            dict(
                circle=Circle(point(t, v(t)), r).set_filled_curves("red"),
                v_point=Text(
                    r"$v_{%d/2}$" % (2 * i + 1), point(t, v(t)) + (point(0, 5 * r))
                ),
            )
        )
        for i, t in enumerate(t_mesh_staggered)
    }
)

axes = Composition(
    dict(
        x=Axis(
            point(0, 0),
            t_mesh[-1] + 0.2 * t_axis_extent,
            "$t$",
            label_spacing=(1 / 45.0, -1 / 30.0),
        ),
        y=Axis(point(0, 0), 0.8 * u_max, "$u,v$", rotation_angle=90),
    )
)

h = 0.03 * u_max  # tickmarks height
u_nodes = Composition(
    {
        i: Composition(
            dict(
                node=Line(point(t, h), point(t, -h)),
                name=Text("$t_%d$" % i, point(t, -3.5 * h)),
            )
        )
        for i, t in enumerate(t_mesh)
    }
)
v_nodes = Composition(
    {
        i: Composition(
            dict(
                node=Line(point(t, h / 1.5), point(t, -h / 1.5)).set_linecolor("red"),
                name=Text(r"$t_{%d/2}$" % (2 * i + 1), point(t, -3.5 * h)),
            )
        )
        for i, t in enumerate(t_mesh_staggered)
    }
)
illustration = Composition(
    dict(u=u_discrete, v=v_discrete, u_mesh=u_nodes, v_mesh=v_nodes, axes=axes)
).set_name("fdm_uv")
drawing_tool.erase()
# Staggered t mesh and u and v points
illustration.draw()
drawing_tool.display()
drawing_tool.savefig(illustration.get_name())

# Exact u line (u is a Spline Shape that applies 500 intervals by default
# for drawing the curve)
u_exact = u.set_linestyle("dashed").set_linewidth(1)
u_exact.draw()
# v = Curve(u.xcoor, v(u.xcoor))
t_mesh_staggered_fine = linspace(t_mesh_staggered[0], t_mesh_staggered[-1], 501)
v_exact = Curve(t_mesh_staggered_fine).set_linestyle("dashed").set_linewidth(1)
v_exact.draw()
drawing_tool.display()
drawing_tool.savefig("%s_uve" % illustration.get_name())

input()
