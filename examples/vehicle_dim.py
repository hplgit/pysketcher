from pysketcher import (
    MatplotlibDraw,
    Circle,
    Rectangle,
    Point,
    Wall,
    Composition,
    Style,
    ArrowWithText,
    DistanceWithText,
)


R = 1  # radius of wheel
L = 4  # distance between wheels
H = 2  # height of vehicle body
w_1 = 5  # position of front wheel
drawing_tool = MatplotlibDraw(0, w_1 + 2 * L + 3 * R, -1, 2 * R + 3 * H, axis=True)
drawing_tool.set_grid(True)

c = Point(w_1, R)

wheel1 = Circle(c, R)
wheel2 = wheel1.translate(Point(L, 0))
under = Rectangle(Point(w_1 - 2 * R, 2 * R), 2 * R + L + 2 * R, H)
over = Rectangle(Point(w_1, 2 * R + H), 2.5 * R, 1.25 * H).set_fill_color(
    Style.Color.WHITE
)
ground = Wall([Point(w_1 - L, 0), Point(w_1 + 3 * L, 0)], -0.3 * R)
ground.style.fill_pattern = Style.FillPattern.UP_RIGHT_TO_LEFT

vehicle = Composition(
    {"wheel1": wheel1, "wheel2": wheel2, "under": under, "over": over, "ground": ground}
)

vehicle.style.line_color = Style.Color.RED

wheel1_dim = ArrowWithText("$w_1$", c + Point(2, 0.25), c)
hdp = w_1 + L + 3 * R  # horizontal dimension position
R_dim = DistanceWithText("$R$", Point(hdp, 0), Point(hdp, R))
H_dim = DistanceWithText("$H$", Point(hdp, 2 * R), Point(hdp, 2 * R + H))
H2_dim = DistanceWithText(
    "$\\frac{5}{4}H$", Point(hdp, 2 * R + H), Point(hdp, 2 * R + (9 / 4) * H)
)

vdp = 2 * R + H + 3 / 2 * H
R2_dim = DistanceWithText("$2R$", Point(w_1 - 2 * R, vdp), Point(w_1, vdp))
L_dim = DistanceWithText("$L$", Point(w_1, vdp), Point(w_1 + L, vdp))
R3_dim = DistanceWithText("$2R$", Point(w_1 + L, vdp), Point(w_1 + L + 2 * R, vdp))

dimensions = Composition(
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

figure = Composition({"vehicle": vehicle, "dimensions": dimensions})

figure.draw(drawing_tool)
drawing_tool.display()
