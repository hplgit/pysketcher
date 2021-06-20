import time

import numpy as np

from pysketcher import (
    ArcWithText,
    Axis,
    Circle,
    Figure,
    Force,
    Gravity,
    Line,
    Point,
    Shape,
    Style,
    Wall,
)
from pysketcher.backend.matplotlib import MatplotlibBackend
from pysketcher.composition import Composition


def main():
    theta = np.pi / 6
    L = 10.0
    a = 1.0
    x_min = 0.0
    y_min = -3.0

    B = Point(a + L, 0)
    A = Point(a, np.tan(theta) * L)

    wall = Wall([A, B], thickness=-0.25)
    wall.style.fill_pattern = Style.FillPattern.UP_LEFT_TO_RIGHT

    angle = ArcWithText(
        r"$\theta$", center=B, radius=3, start_angle=np.pi - theta, arc_angle=theta
    )
    angle.style.line_color = Style.Color.BLACK
    angle.style.line_width = 1

    ground = Line(Point(B.x - L / 10.0, 0), Point(B.x - L / 2.0, 0))
    ground.style.line_color = Style.Color.BLACK
    ground.style.line_style = Style.LineStyle.DASHED
    ground.style.line_width = 1

    r = 1.0  # radius of wheel
    help_line = Line(A, B)
    x = a + 3 * L / 10.0
    y = help_line(x=x)
    contact = Point(x, y)
    normal_vec = Point(np.sin(theta), np.cos(theta))
    c = contact + normal_vec * r
    outer_wheel = (
        Circle(c, r).set_line_color(Style.Color.BLUE).set_fill_color(Style.Color.BLUE)
    )
    hole = (
        Circle(c, r / 2.0)
        .set_line_color(Style.Color.BLUE)
        .set_fill_color(Style.Color.WHITE)
    )
    wheel = Composition({"outer": outer_wheel, "inner": hole})

    N = Force("$N$", contact - normal_vec * 2 * r, contact, spacing=0.2)
    N.style.line_color = Style.Color.BLACK

    # text_alignment='left')
    mg = Gravity(c, 3 * r, text="$Mg$", text_position=Gravity.TextPosition.END)

    x_const = Line(contact, contact + Point(0, 4))
    x_const.style.line_style = Style.LineStyle.DOTTED
    x_const = x_const.rotate(-theta, contact)

    x_axis = Axis(
        start=contact + normal_vec * 3.0 * r,
        length=4 * r,
        label="$x$",
        rotation_angle=-theta,
    )

    body = Composition({"wheel": wheel, "N": N, "mg": mg})
    fixed = Composition(
        {
            "angle": angle,
            "inclined wall": wall,
            "wheel": wheel,
            "ground": ground,
            "x start": x_const,
            "x axis": x_axis,
        }
    )

    model = Composition({"fixed elements": fixed, "body": body})

    fig = Figure(x_min, x_min + 1.5 * L, y_min, y_min + L, backend=MatplotlibBackend)

    fig.add(model)
    fig.show()
    time.sleep(1)
    tangent_vec = Point(normal_vec.y, -normal_vec.x)

    def position(t):
        """Position of center point of wheel."""
        return c + tangent_vec * 7 * t ** 2

    def move(fig: Shape, t: float, dt: float = None) -> fig:
        x = position(t)
        x0 = position(t - dt)
        displacement = x - x0
        return fig["body"].translate(displacement)


if __name__ == "__main__":
    main()
