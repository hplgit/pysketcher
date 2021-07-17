import numpy as np

import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend

Nt = 5


def main():
    u = ps.SketchyFunc3()
    t_mesh = np.linspace(0, 6, Nt + 1)
    t_mesh_staggered = np.linspace(
        0.5 * (t_mesh[0] + t_mesh[1]), 0.5 * (t_mesh[-2] + t_mesh[-1]), Nt
    )

    # Add 20% space to the left and 30% to the right of the coordinate system
    t_axis_extent = t_mesh[-1] - t_mesh[0]
    t_min = t_mesh[0] - 0.2 * t_axis_extent
    t_max = t_mesh[-1] + 0.3 * t_axis_extent
    u_max = 1.3 * max([u(t) for t in t_mesh])
    u_min = -0.2 * u_max

    r = 0.005 * (t_max - t_min)  # radius of circles placed at mesh Points
    u_discrete = ps.Composition(
        {
            i: ps.Composition(
                dict(
                    circle=ps.Circle(ps.Point(t, u(t)), r).set_fill_color(
                        ps.Style.Color.BLACK
                    ),
                    u_Point=ps.Text(
                        "$u_%d$" % i,
                        ps.Point(t, u(t))
                        + (ps.Point(0, 5 * r) if i > 0 else ps.Point(-5 * r, 0)),
                    ),
                )
            )
            for i, t in enumerate(t_mesh)
        }
    )

    # u' = v
    # v = u.smooth.derivative(n=1)
    v = ps.SketchyFunc4()

    v_discrete = ps.Composition(
        {
            i: ps.Composition(
                dict(
                    circle=ps.Circle(ps.Point(t, v(t)), r).set_fill_color(
                        ps.Style.Color.RED
                    ),
                    v_Point=ps.Text(
                        r"$v_{%d/2}$" % (2 * i + 1),
                        ps.Point(t, v(t)) + (ps.Point(0, 5 * r)),
                    ),
                )
            )
            for i, t in enumerate(t_mesh_staggered)
        }
    )

    axes = ps.Composition(
        dict(
            x=ps.Axis(ps.Point(0, 0), t_mesh[-1] + 0.2 * t_axis_extent, "$t$"),
            y=ps.Axis(ps.Point(0, 0), 0.8 * u_max, "$u,v$", rotation_angle=np.pi / 2),
        )
    )

    h = 0.03 * u_max  # tickmarks height
    u_nodes = ps.Composition(
        {
            i: ps.Composition(
                dict(
                    node=ps.Line(ps.Point(t, h), ps.Point(t, -h)),
                    name=ps.Text("$t_%d$" % i, ps.Point(t, -3.5 * h)),
                )
            )
            for i, t in enumerate(t_mesh)
        }
    )
    v_nodes = ps.Composition(
        {
            i: ps.Composition(
                dict(
                    node=ps.Line(
                        ps.Point(t, h / 1.5), ps.Point(t, -h / 1.5)
                    ).set_line_color(ps.Style.Color.RED),
                    name=ps.Text(r"$t_{%d/2}$" % (2 * i + 1), ps.Point(t, -3.5 * h)),
                )
            )
            for i, t in enumerate(t_mesh_staggered)
        }
    )
    illustration = ps.Composition(
        dict(u=u_discrete, v=v_discrete, u_mesh=u_nodes, v_mesh=v_nodes, axes=axes)
    )

    fig = ps.Figure(t_min, t_max, u_min, u_max, backend=MatplotlibBackend)

    # Staggered t mesh and u and v Points
    fig.add(illustration)
    fig.show()

    # Exact u line (u is a Spline Shape that applies 500 intervals by default
    # for drawing the curve)
    u_exact = u.set_line_style(ps.Style.LineStyle.DASHED).set_line_width(1)
    fig.add(u_exact)
    fig.show()

    # v = Curve(u.xcoor, v(u.xcoor))
    t_mesh_staggered_fine = np.linspace(t_mesh_staggered[0], t_mesh_staggered[-1], 501)
    t_mesh_staggered_points = [ps.Point(x, v(x)) for x in t_mesh_staggered_fine]
    v_exact = (
        ps.Curve(t_mesh_staggered_points)
        .set_line_style(ps.Style.LineStyle.DASHED)
        .set_line_width(1)
    )
    fig.add(v_exact)
    fig.show()


if __name__ == "__main__":
    main()
