import logging

import numpy as np

import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend

logging.basicConfig(level=logging.INFO)

W = 5  # upstream area
L = 10  # downstream area
H = 4  # height
sigma = 2
alpha = 2


# Create bottom
def gaussian(x: float) -> float:
    return alpha * np.exp(-((x - W) ** 2) / (0.5 * sigma ** 2))


wall = ps.Wall([ps.Point(x, gaussian(x)) for x in np.linspace(0, W + L, 51)], 0.3)
wall.style.line_color = ps.Style.Color.BROWN


def velocity_profile(y: float) -> ps.Point:
    return ps.Point(2 * y * (2 * H - y) / H ** 2, 0)


inlet_profile = ps.VelocityProfile(ps.Point(0, 0), H, velocity_profile, 5)
inlet_profile.style.line_color = ps.Style.Color.BLUE

symmetry_line = ps.Line(ps.Point(0, H), ps.Point(W + L, H))
symmetry_line.style.line_style = ps.Style.LineStyle.DASHED

outlet = ps.Line(ps.Point(W + L, 0), ps.Point(W + L, H))
outlet.style.line_style = ps.Style.LineStyle.DASHED

model = ps.Composition(
    {
        "bottom": wall,
        "inlet": inlet_profile,
        "symmetry line": symmetry_line,
        "outlet": outlet,
    }
)

velocity = velocity_profile(H / 2.0)
line = ps.Line(ps.Point(W - 2.5 * sigma, 0), ps.Point(W + 2.5 * sigma, 0))
line.style.line_style = ps.Style.LineStyle.DASHED
symbols = {
    "alpha": ps.DistanceWithText(r"$\alpha$", ps.Point(W, 0), ps.Point(W, alpha)),
    "W": ps.DistanceWithText(
        r"$W$", ps.Point(0, -0.5), ps.Point(W, -0.5), spacing=-1.0 / 3
    ),
    "L": ps.DistanceWithText(
        r"$L$", ps.Point(W, -0.5), ps.Point(W + L, -0.5), spacing=-1.0 / 3
    ),
    "v(y)": ps.Text("$v(y)$  ", ps.Point(H / 2.0, velocity.x)),
    "dashed line": line,
}
symbols = ps.Composition(symbols)

drawing_tool = ps.Figure(0, W + L + 1, -2, H + 1, backend=MatplotlibBackend)
drawing_tool.display()
