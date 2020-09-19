from pysketcher import *

"""
u = SketchyFunc2('$u(t)$', name_pos='end')
n = 7
t_mesh = [i*2.25/(n-1) for i in range(n)]

u = SketchyFunc2('$u(t)$', name_pos='end')
t_mesh = [0, 2, 4, 6, 8]
"""

u = SketchyFunc3()
Nt = 5
t_mesh = linspace(0, 6, Nt + 1)

# Add 20% space to the left and 30% to the right of the coordinate system
t_axis_extent = t_mesh[-1] - t_mesh[0]
t_min = t_mesh[0] - 0.2 * t_axis_extent
t_max = t_mesh[-1] + 0.3 * t_axis_extent
u_max = 1.3 * max([u(t) for t in t_mesh])
u_min = -0.2 * u_max

drawing_tool._set_coordinate_system(t_min, t_max, u_min, u_max, axis=False)
drawing_tool.set_linecolor("black")

r = 0.005 * (t_max - t_min)  # radius of circles placed at mesh points
# import random; random.seed(12)
perturbations = [0, 0.1, 0.1, 0.2, -0.4, -0.1]
u_points = {}
u_values = []
for i, t in enumerate(t_mesh):
    u_value = u(t) + perturbations[i]
    u_values.append(u_value)
    u_points[i] = Composition(
        dict(
            circle=Circle(point(t, u_value), r).set_filled_curves("black"),
            u_point=Text(
                "$u^%d$" % i,
                point(t, u_value) + (point(0, 3 * r) if i > 0 else point(-3 * r, 0)),
            ),
        )
    )
u_discrete = Composition(u_points)

interpolant = Composition(
    {
        i: Line(
            point(t_mesh[i - 1], u_values[i - 1]), point(t_mesh[i], u_values[i])
        ).set_linewidth(1)
        for i in range(1, len(t_mesh))
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
        y=Axis(point(0, 0), 0.8 * u_max, "$u$", rotation_angle=90),
    )
)

h = 0.03 * u_max  # tickmarks height
nodes = Composition(
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
illustration = Composition(dict(u=u_discrete, mesh=nodes, axes=axes)).set_name("fdm_u")
drawing_tool.erase()
# Draw t_mesh with discrete u points
illustration.draw()
drawing_tool.display()
drawing_tool.savefig(illustration.get_name())

# Add exact u line (u is a Spline Shape that applies 500 intervals by default
# for drawing the curve)
exact = u.set_linestyle("dashed").set_linewidth(1)
exact.draw()
drawing_tool.display()
drawing_tool.savefig("%s_ue" % illustration.get_name())

# Add linear interpolant
interpolant.draw()
drawing_tool.display()
drawing_tool.savefig("%s_uei" % illustration.get_name())

# Linear interpolant without exact, smooth line
drawing_tool.erase()
illustration.draw()
interpolant.draw()
drawing_tool.display()
drawing_tool.savefig("%s_ui" % illustration.get_name())

input()
