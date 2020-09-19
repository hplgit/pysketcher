"""A more sophisticated beam than in beam1.py."""

from pysketcher import *
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)


def beam():
    L = 8.0
    a = 3 * L / 4
    b = L - a
    H = 1.0
    A = Point(0.0, 3.0)

    drawing_tool = MatplotlibDraw(
        xmin=-3, xmax=A.x + 1.5 * L, ymin=0, ymax=A.y + 5 * H, axis=False
    )

    beam = (
        Rectangle(A, L, H)
        .set_fill_pattern(Style.FillPattern.UP_RIGHT_TO_LEFT)
        .set_line_color(Style.Color.BLUE)
    )

    h = L / 16  # size of support, clamped wall etc

    clamped = Rectangle(A - Point(h, 0) - Point(0, 2 * h), h, 6 * h).set_fill_pattern(
        Style.FillPattern.UP_LEFT_TO_RIGHT
    )

    load = UniformLoad(A + Point(0, H), L, H)
    load.set_line_width(1).set_line_color(Style.Color.BLACK)
    load_text = Text("$w$", load.geometric_features()["mid_top"] + Point(0, h / 2.0))

    B = A + Point(a, 0)
    C = B + Point(b, 0)

    support = SimpleSupport(B, h)  # pt B is simply supported

    R1 = Force("$R_1$", A - Point(0, 2 * H), A, start_spacing=0.3)
    R1.set_line_width(3).set_line_color(Style.Color.BLACK)
    R2 = Force(
        "$R2$",
        B - Point(0, 2 * H),
        support.geometric_features()["mid_support"],
        start_spacing=0.3,
    )
    R2.set_line_width(3).set_line_color(Style.Color.BLACK)
    M1 = Moment(
        "$M_1$",
        center=A + Point(-H, H / 2),
        radius=H / 2,
        left=True,
        text_spacing=1 / 3.0,
    )
    M1.line_color = "black"

    ab_level = Point(0, 3 * h)
    a_dim = DistanceWithText("$a$", A - ab_level, B - ab_level)
    b_dim = DistanceWithText("$b$", B - ab_level, C - ab_level)
    dims = Composition({"a": a_dim, "b": b_dim})
    symbols = Composition(
        {
            "R1": R1,
            "R2": R2,
            "M1": M1,
            "w": load,
            "w text": load_text,
            "A": Text("$A$", A + Point(0.7 * h, -0.9 * h)),
            "B": Text(
                "$B$", support.geometric_features()["mid_support"] - Point(1.25 * h, 0)
            ),
            "C": Text("$C$", C + Point(h / 2, -h / 2)),
        }
    )

    x_axis = Axis(
        A + Point(L + h, H / 2),
        2 * H,
        "$x$",
    ).set_line_color(Style.Color.BLACK)
    y_axis = Axis(
        A + Point(0, H / 2), 3.5 * H, "$y$", rotation_angle=np.pi / 2
    ).set_line_color(Style.Color.BLACK)
    axes = Composition({"x axis": x_axis, "y axis": y_axis})

    annotations = Composition({"dims": dims, "symbols": symbols, "axes": axes})
    beam = Composition(
        {"beam": beam, "support": support, "clamped end": clamped, "load": load}
    )

    def deflection(x, a, b, w) -> float:
        R1 = 5.0 / 8 * w * a - 3 * w * b ** 2 / (4 * a)
        R2 = 3.0 / 8 * w * a + w * b + 3 * w * b ** 2 / (4 * a)
        M1 = R1 * a / 3 - w * a ** 2 / 12
        y = (
            -(M1 / 2.0) * x ** 2
            + 1.0 / 6 * R1 * x ** 3
            - w / 24.0 * x ** 4
            + 1.0 / 6 * R2 * np.where(x > a, 1, 0) * (x - a) ** 3
        )
        return y

    xs = np.linspace(0, L, 101)
    ys = deflection(xs, a, b, w=1.0)
    ys /= abs(ys.max() - ys.min())
    ys += A.y + H / 2
    points = Point.from_coordinate_lists(xs, ys)

    elastic_line = (
        Curve(points)
        .set_line_color(Style.Color.RED)
        .set_line_style(Style.LineStyle.DASHED)
        .set_line_width(3)
    )

    beam.draw(drawing_tool)
    drawing_tool.display()

    import time

    time.sleep(1.5)

    annotations.draw(drawing_tool)
    drawing_tool.display()
    time.sleep(1.5)

    elastic_line.draw(drawing_tool)
    drawing_tool.display()
    # beam.draw_dimensions()
    # test_Dashpot(xpos+2*W)


beam()
