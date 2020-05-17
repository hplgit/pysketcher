import numpy as np
import logging
from pysketcher import MatplotlibDraw, Wall, Point, VelocityProfile, Line, Composition, Distance_wText, Text

logging.basicConfig(level=logging.INFO)

W = 5  # upstream area
L = 10  # downstream area
H = 4  # height
sigma = 2
alpha = 2

drawing_tool = MatplotlibDraw(xmin=0, xmax=W + L + 1,
                              ymin=-2, ymax=H + 1,
                              axis=True)


# Create bottom
def gaussian(x: float) -> float:
    return alpha * np.exp(-(x - W) ** 2 / (0.5 * sigma ** 2))


wall = Wall([Point(x, gaussian(x)) for x in np.linspace(0, W + L, 51)], 0.3)
wall.line_color = 'brown'


def velocity_profile(y: float) -> Point:
    return Point(2 * y * (2 * H - y) / H ** 2, 0)


inlet_profile = VelocityProfile(Point(0, 0), H, velocity_profile, 5)
inlet_profile.line_color = 'blue'

symmetry_line = Line(Point(0, H), Point(W + L, H))
symmetry_line.line_style = 'dashed'

outlet = Line(Point(W + L, 0), Point(W + L, H))
outlet.line_style = 'dashed'

fig = Composition({
    'bottom': wall,
    'inlet': inlet_profile,
    'symmetry line': symmetry_line,
    'outlet': outlet,
})

fig.draw(drawing_tool)  # send all figures to plotting backend

velocity = velocity_profile(H / 2.)
symbols = {
    'alpha': Distance_wText(Point(W, 0), Point(W, alpha), r'$\alpha$'),

    'W': Distance_wText(Point(0, -0.5), Point(W, -0.5), r'$W$',
                        text_spacing=-1. / 30),

    'L': Distance_wText(Point(W, -0.5), Point(W + L, -0.5), r'$L$',
                        text_spacing=-1. / 30),
    'v(y)': Text('$v(y)$  ', Point(H / 2., velocity.x)),
    'dashed line': Line(Point(W - 2.5 * sigma, 0), Point(W + 2.5 * sigma, 0)).
                             set_line_style('dotted').
                             set_line_color('black'),
}
symbols = Composition(symbols)
symbols.draw(drawing_tool)

drawing_tool.display()

