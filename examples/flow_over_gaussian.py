import numpy as np
import logging
from pysketcher import (
    MatplotlibDraw,
    Wall,
    Point,
    VelocityProfile,
    Line,
    Composition,
    DistanceWithText,
    Text,
    Style,
)

logging.basicConfig(level=logging.INFO)

W = 5  # upstream area
L = 10  # downstream area
H = 4  # height
sigma = 2
alpha = 2

drawing_tool = MatplotlibDraw(xmin=0, xmax=W + L + 1, ymin=-2, ymax=H + 1, axis=True)


# Create bottom
def gaussian(x: float) -> float:
    return alpha * np.exp(-((x - W) ** 2) / (0.5 * sigma ** 2))


wall = Wall([Point(x, gaussian(x)) for x in np.linspace(0, W + L, 51)], 0.3)
wall.style.line_color = Style.Color.BROWN


def velocity_profile(y: float) -> Point:
    return Point(2 * y * (2 * H - y) / H ** 2, 0)


inlet_profile = VelocityProfile(Point(0, 0), H, velocity_profile, 5)
inlet_profile.style.line_color = Style.Color.BLUE

symmetry_line = Line(Point(0, H), Point(W + L, H))
symmetry_line.style.line_style = Style.LineStyle.DASHED

outlet = Line(Point(W + L, 0), Point(W + L, H))
outlet.style.line_style = Style.LineStyle.DASHED

fig = Composition(
    {
        "bottom": wall,
        "inlet": inlet_profile,
        "symmetry line": symmetry_line,
        "outlet": outlet,
    }
)

fig.draw(drawing_tool)  # send all figures to plotting backend

velocity = velocity_profile(H / 2.0)
line = Line(Point(W - 2.5 * sigma, 0), Point(W + 2.5 * sigma, 0))
line.style.line_style = Style.LineStyle.DASHED
symbols = {
    "alpha": DistanceWithText(r"$\alpha$", Point(W, 0), Point(W, alpha)),
    "W": DistanceWithText(r"$W$", Point(0, -0.5), Point(W, -0.5), spacing=-1.0 / 3),
    "L": DistanceWithText(r"$L$", Point(W, -0.5), Point(W + L, -0.5), spacing=-1.0 / 3),
    "v(y)": Text("$v(y)$  ", Point(H / 2.0, velocity.x)),
    "dashed line": line,
}
symbols = Composition(symbols)
symbols.draw(drawing_tool)

drawing_tool.display()
