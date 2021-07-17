import logging

import numpy as np

import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend

H = 7.0
W = 6.0

logging.basicConfig(level=logging.INFO)


# drawing_tool.set_grid(True)


def main() -> None:
    L = 5 * H / 7  # length
    P = ps.Point(W / 6, 0.85 * H)  # rotation point
    a = 2 * np.pi / 9  # angle

    vertical = ps.Line(P, P - ps.Point(0, L))
    path = ps.Arc(P, L, -np.pi / 2, a)
    mass_pt = path.end
    rod = ps.Line(P, mass_pt)

    mass = ps.Circle(mass_pt, L / 20.0)
    theta = ps.AngularDimension(
        r"$\theta$", P + ps.Point(0, -L / 4), P + (mass_pt - P).unit_vector * (L / 4), P
    )
    theta.extension_lines = False

    rod_vec = rod.end - rod.start
    unit_rod_vec = rod_vec.unit_vector
    mass_symbol = ps.Text("$m$", mass_pt + unit_rod_vec * (L / 10.0))

    length = ps.LinearDimension("$L$", mass_pt, P)
    gravity = ps.Gravity(start=P + ps.Point(0.8 * L, 0), length=L / 3)

    def set_dashed_thin_blackline(*objects: ps.Shape):
        """Set linestyle of objects to dashed, black, width=1."""
        for obj in objects:
            obj.set_line_style(ps.Style.LineStyle.DASHED)
            obj.set_line_color(ps.Style.Color.BLACK)
            obj.set_line_width(1)

    set_dashed_thin_blackline(vertical, path)
    mass.style.fill_color = ps.Style.Color.BLUE

    model = ps.Composition(
        {
            "vertical": vertical,
            "path": path,
            "theta": theta,
            "rod": rod,
            "body": mass,
            "m": mass_symbol,
            "g": gravity,
            "L": length,
        }
    )

    fig = ps.Figure(0.0, W, 0.0, H, backend=MatplotlibBackend)
    fig.add(model)
    fig.show()

    vertical2 = ps.Line(rod.start, rod.start + ps.Point(0.0, -L / 3.0))
    set_dashed_thin_blackline(vertical2)
    set_dashed_thin_blackline(rod)
    angle2 = ps.Arc(rod.start, L / 6, -np.pi / 2, a)
    angle2.style.arrow = ps.Style.ArrowStyle.DOUBLE
    angle2_label = ps.ArcAnnotation(r"$\theta$", angle2)

    mg_force = ps.Force(
        "$mg$",
        mass_pt,
        mass_pt + ps.Point(0.0, -L / 5.0),
        text_position=ps.TextPosition.END,
    )
    rod_force = ps.Force(
        "$S$",
        mass_pt,
        mass_pt - rod_vec.unit_vector * (L / 3.0),
        text_position=ps.TextPosition.END,
    )

    mass.style.fill_color = ps.Style.Color.BLUE

    body_diagram_shapes = {
        "$mg$": mg_force,
        "S": rod_force,
        "rod": rod,
        "vertical": vertical2,
        "theta": angle2,
        "theta_label": angle2_label,
        "body": mass,
        "m": mass_symbol,
    }

    air_force = ps.Force(
        r"${\sim}|v|v$",
        mass_pt,
        mass_pt + rod_vec.normal * (L / 6.0),
        text_position=ps.TextPosition.END,
        # spacing = Point(0.04, 0.005),
    )

    body_diagram_shapes["air"] = air_force

    x0y0 = ps.Text("$(x_0,y_0)$", P + ps.Point(-0.4, -0.1))

    ir = ps.Force(
        r"$\vec{i}_r$",
        P,
        P + rod_vec.unit_vector * (L / 10.0),
        text_position=ps.TextPosition.END,
    )

    ith = ps.Force(
        r"$\vec{i}_{\theta}$",
        P,
        P + rod_vec.normal * (L / 10.0),
        text_position=ps.TextPosition.END,
    )

    body_diagram_shapes["ir"] = ir
    body_diagram_shapes["ith"] = ith
    body_diagram_shapes["origin"] = x0y0

    fig.erase()
    body_diagram = ps.Composition(body_diagram_shapes)
    fig.add(body_diagram)
    fig.show()


if __name__ == "__main__":
    main()
