import numpy as np
import time
from pysketcher import (
    Shape,
    Point,
    MatplotlibDraw,
    Wall,
    ArcWithText,
    Line,
    Circle,
    Composition,
    Axis,
    Force,
    Gravity,
    Style,
)


def inclined_plane():
    theta = np.pi / 6
    L = 10.0
    a = 1.0
    xmin = 0
    ymin = -3

    drawing_tool = MatplotlibDraw(
        xmin=xmin, xmax=xmin + 1.5 * L, ymin=ymin, ymax=ymin + L
    )
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

    r = 1  # radius of wheel
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
    # or x_const = Line(contact-2*r*normal_vec, contact+4*r*normal_vec).set_linestyle('dotted')
    x_axis = Axis(
        start=contact + normal_vec * 3 * r,
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

    fig = Composition({"fixed elements": fixed, "body": body})

    fig.draw(drawing_tool)
    drawing_tool.savefig("tmp.png")
    drawing_tool.savefig("tmp.pdf")
    drawing_tool.display()
    time.sleep(1)
    tangent_vec = Point(normal_vec.y, -normal_vec.x)

    time_points = np.linspace(0, 1, 31)

    def position(t):
        """Position of center point of wheel."""
        return c + tangent_vec * 7 * t ** 2

    def move(fig: Shape, t: float, dt: float = None) -> fig:
        x = position(t)
        x0 = position(t - dt)
        displacement = x - x0
        return fig["body"].translate(displacement)

    # animate(fig, time_points, move, pause_per_frame=0,
    #        dt=time_points[1] - time_points[0])

    print(str(fig))
    print(repr(fig))


inclined_plane()
input()
