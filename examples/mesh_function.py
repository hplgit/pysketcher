import logging

import numpy as np

import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend


def main() -> None:
    u = ps.SketchyFunc3()
    Nt = 5
    t_mesh = np.linspace(0, 6, Nt + 1)

    # Add 20% space to the left and 30% to the right of the coordinate system
    t_axis_extent = t_mesh[-1] - t_mesh[0]
    logging.info(t_axis_extent)
    t_min = t_mesh[0] - 0.2 * t_axis_extent
    logging.info(t_min)
    t_max = t_mesh[-1] + 0.3 * t_axis_extent
    logging.info(t_max)
    u_max = 1.3 * max([u(t) for t in t_mesh])
    logging.info(u_max)
    u_min = -0.2 * u_max
    logging.info(u_max)

    r = 0.005 * (t_max - t_min)  # radius of circles placed at mesh points
    # import random; random.seed(12)
    perturbations = [0, 0.1, 0.1, 0.2, -0.4, -0.1]
    u_points = {}
    u_values = []
    for i, t in enumerate(t_mesh):
        u_value = u(t) + perturbations[i]
        u_values.append(u_value)
        circle = ps.Circle(ps.Point(t, u_value), r).set_fill_color(ps.Style.Color.BLACK)
        text = ps.Text(
            "$u^%d$" % i,
            ps.Point(t, u_value)
            + (ps.Point(0.0, 3 * r) if i > 0 else ps.Point(-3 * r, 0.0)),
        )
        u_points[i] = ps.Composition({"circle": circle, "u_point": text})
    u_discrete = ps.Composition(u_points)

    i_lines = {}
    for i in range(1, len(t_mesh)):
        i_lines[i] = ps.Line(
            ps.Point(t_mesh[i - 1], u_values[i - 1]), ps.Point(t_mesh[i], u_values[i])
        ).set_line_width(1)
    interpolant = ps.Composition(i_lines)

    x_axis_extent: float = t_mesh[-1] + 0.2 * t_axis_extent
    logging.info(x_axis_extent)
    axes = ps.Composition(
        {
            "x": ps.Axis(
                ps.Point(0.0, 0.0),
                x_axis_extent,
                "$t$",
            ),
            "y": ps.Axis(
                ps.Point(0.0, 0.0), 0.8 * u_max, "$u$", rotation_angle=np.pi / 2
            ),
        }
    )

    h = 0.03 * u_max  # tickmarks height
    i_nodes = {}
    for i, t in enumerate(t_mesh):
        i_nodes[i] = ps.Composition(
            {
                "node": ps.Line(ps.Point(t, h), ps.Point(t, -h)),
                "name": ps.Text("$t_%d$" % i, ps.Point(t, -3.5 * h)),
            }
        )

    nodes = ps.Composition(i_nodes)

    fig = ps.Figure(t_min, t_max, u_min, u_max, backend=MatplotlibBackend)

    # Draw t_mesh with discrete u points
    illustration = ps.Composition(
        dict(
            u=u_discrete,
            mesh=nodes,
            axes=axes,
        )
    )
    fig.erase()
    fig.add(illustration)
    fig.show()

    # Add exact u line (u is a Spline Shape that applies 500 intervals by default
    # for drawing the curve)
    exact = u.set_line_style(ps.Style.LineStyle.DASHED).set_line_width(1)

    fig.add(exact)
    fig.show()

    # Add linear interpolant
    fig.add(interpolant)
    fig.show()

    # Linear interpolant without exact, smooth line
    fig.erase()
    fig.add(illustration)
    fig.add(interpolant)
    fig.show()


if __name__ == "__main__":
    main()
