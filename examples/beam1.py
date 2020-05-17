"""A very simple beam."""
from pysketcher import *

L = 8.0
H = 1.0
x_pos = 2.0
y_pos = 3.0

drawing_tool = MatplotlibDraw(xmin=0, xmax=x_pos + 1.2 * L,
                              ymin=0, ymax=y_pos + 5 * H,
                              axis=True)
drawing_tool.set_linecolor('blue')
drawing_tool.set_grid(True)
drawing_tool.set_fontsize(22)

p0 = Point(x_pos, y_pos)
main = Rectangle(p0, L, H)
h = L / 16  # size of support, clamped wall etc
support = SimplySupportedBeam(p0, h)
clamped = Rectangle(p0 + Point(L, 0) - Point(0, 2 * h), h, 6 * h).set_fill_pattern('/')
F_pt = Point(p0.x + L / 2, p0.y + H)
force = Force(F_pt + Point(0, 2 * H), F_pt, '$F$').set_line_width(3)
L_dim = Distance_wText(Point(x_pos, p0.y - 3 * h), Point(x_pos + L, p0.y - 3 * h), '$L$')
beam = Composition({'main': main, 'simply supported end': support,
                    'clamped end': clamped, 'force': force,
                    'L': L_dim})

beam.draw(drawing_tool)
beam.draw_dimensions(drawing_tool)
drawing_tool.display()

# test_Dashpot(xpos+2*W)

