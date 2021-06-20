import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend

R = 1  # radius of wheel
L = 4  # distance between wheels
H = 2  # height of vehicle body
w_1 = 5  # position of front wheel


# TODO : draw grids
# drawing_tool.set_grid(True)
def main() -> None:
    c = ps.Point(w_1, R)

    wheel1 = ps.Circle(c, R)
    wheel2 = wheel1.translate(ps.Point(L, 0))
    under = ps.Rectangle(ps.Point(w_1 - 2 * R, 2 * R), 2 * R + L + 2 * R, H)
    over = ps.Rectangle(ps.Point(w_1, 2 * R + H), 2.5 * R, 1.25 * H).set_fill_color(
        ps.Style.Color.WHITE
    )
    ground = ps.Wall([ps.Point(w_1 - L, 0), ps.Point(w_1 + 3 * L, 0)], -0.3 * R)
    ground.style.fill_pattern = ps.Style.FillPattern.UP_RIGHT_TO_LEFT

    vehicle = ps.Composition(
        {
            "wheel1": wheel1,
            "wheel2": wheel2,
            "under": under,
            "over": over,
            "ground": ground,
        }
    )

    vehicle.style.line_color = ps.Style.Color.RED

    wheel1_dim = ps.ArrowWithText("$w_1$", c + ps.Point(2, 0.25), c)
    hdp = w_1 + L + 3 * R  # horizontal dimension position
    R_dim = ps.DistanceWithText("$R$", ps.Point(hdp, 0), ps.Point(hdp, R))
    H_dim = ps.DistanceWithText("$H$", ps.Point(hdp, 2 * R), ps.Point(hdp, 2 * R + H))
    H2_dim = ps.DistanceWithText(
        "$\\frac{5}{4}H$", ps.Point(hdp, 2 * R + H), ps.Point(hdp, 2 * R + (9 / 4) * H)
    )

    vdp = 2 * R + H + 3 / 2 * H
    R2_dim = ps.DistanceWithText("$2R$", ps.Point(w_1 - 2 * R, vdp), ps.Point(w_1, vdp))
    L_dim = ps.DistanceWithText("$L$", ps.Point(w_1, vdp), ps.Point(w_1 + L, vdp))
    R3_dim = ps.DistanceWithText(
        "$2R$", ps.Point(w_1 + L, vdp), ps.Point(w_1 + L + 2 * R, vdp)
    )

    dimensions = ps.Composition(
        {
            "wheel1_dim": wheel1_dim,
            "R_dim": R_dim,
            "H_dim": H_dim,
            "H2_dim": H2_dim,
            "R2_dim": R2_dim,
            "L_dim": L_dim,
            "R3_dim": R3_dim,
        }
    )

    model = ps.Composition({"vehicle": vehicle, "dimensions": dimensions})

    figure = ps.Figure(
        0, w_1 + 2 * L + 3 * R, -1, 2 * R + 3 * H, backend=MatplotlibBackend
    )
    figure.add(model)
    figure.show()


if __name__ == "__main__":
    main()
