"""A very simple beam."""
import logging

# TODO: switch this to ps style importing
from pysketcher import (
    Figure,
    Force,
    LinearDimension,
    Point,
    Rectangle,
    SimpleSupport,
    Style,
)
from pysketcher.backend.matplotlib import MatplotlibBackend
from pysketcher.composition import Composition


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    L = 8.0
    H = 1.0
    x_pos = 2.0
    y_pos = 3.0

    fig = Figure(0, x_pos + 1.2 * L, 0, y_pos + 5 * H, MatplotlibBackend)

    p0 = Point(x_pos, y_pos)
    main = Rectangle(p0, L, H).set_fill_pattern(Style.FillPattern.UP_LEFT_TO_RIGHT)
    h = L / 16  # size of support, clamped wall etc
    support = SimpleSupport(p0, h)
    clamped = Rectangle(p0 + Point(L, 0) - Point(0, 2 * h), h, 6 * h).set_fill_pattern(
        Style.FillPattern.UP_RIGHT_TO_LEFT
    )
    F_pt = Point(p0.x + L / 2, p0.y + H)
    force = Force("$F$", F_pt + Point(0, 2 * H), F_pt).set_line_width(3)
    L_dim = LinearDimension(
        "$L$", Point(x_pos, p0.y - 3 * h), Point(x_pos + L, p0.y - 3 * h)
    )
    beam = Composition(
        {
            "main": main,
            "simply supported end": support,
            "clamped end": clamped,
            "force": force,
            "L": L_dim,
        }
    )

    fig.add(beam)
    # beam.draw_dimensions(drawing_tool)
    fig.show()


if __name__ == "__main__":
    main()
