import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend

R = 1  # radius of wheel
L = 4  # distance between wheels
H = 2  # height of vehicle body
w_1 = 5  # position of front wheel


def main() -> None:
    wheel1 = (
        ps.Circle(ps.Point(w_1, R), R)
        .set_fill_color(ps.Style.Color.BLUE)
        .set_line_width(6)
    )
    wheel2 = wheel1.translate(ps.Point(L, 0))
    under = ps.Rectangle(ps.Point(w_1 - 2 * R, 2 * R), 2 * R + L + 2 * R, H)
    under.style.fill_color = ps.Style.Color.RED
    under.style.line_color = ps.Style.Color.RED
    over = ps.Rectangle(ps.Point(w_1, 2 * R + H), 2.5 * R, 1.25 * H).set_fill_color(
        ps.Style.Color.WHITE
    )
    over.style.line_width = 14
    over.style.line_color = ps.Style.Color.RED
    over.style.fill_pattern = ps.Style.FillPattern.UP_RIGHT_TO_LEFT

    ground = ps.Wall([ps.Point(w_1 - L, 0), ps.Point(w_1 + 3 * L, 0)], -0.3 * R)
    ground.style.fill_pattern = ps.Style.FillPattern.UP_LEFT_TO_RIGHT

    model = ps.Composition(
        {
            "wheel1": wheel1,
            "wheel2": wheel2,
            "under": under,
            "over": over,
            "ground": ground,
        }
    )

    fig = ps.Figure(
        0, w_1 + 2 * L + 3 * R, -1, 2 * R + 3 * H, backend=MatplotlibBackend
    )
    fig.add(model)
    fig.show()


if __name__ == "__main__":
    main()
