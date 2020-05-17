"""A more sophisticated beam than in beam1.py."""
from typing import List

from pysketcher import *
import numpy as np


def beam():
    L = 8.0
    a = 3 * L / 4
    b = L - a
    H = 1.0
    A = Point(0.0, 3.0)

    drawing_tool = MatplotlibDraw(
        xmin=-3, xmax=A.x + 1.5 * L,
        ymin=0, ymax=A.y + 5 * H,
        axis=False)
    drawing_tool.set_linecolor('blue')
    drawing_tool.set_fontsize(16)

    beam = Rectangle(A, L, H)

    h = L / 16  # size of support, clamped wall etc

    clamped = Rectangle(A - Point(h, 0) - Point(0, 2 * h), h,
                        6 * h).set_fill_pattern('/')

    load = UniformLoad(A + Point(0, H), L, H)
    load.set_line_width(1).set_line_color('black')
    load_text = Text('$w$',
                     load.geometric_features()['mid_top'] +
                     Point(0, h / 2.))

    B = A + Point(a, 0)
    C = B + Point(b, 0)

    support = SimplySupportedBeam(B, h)  # pt B is simply supported

    R1 = Force(A - Point(0, 2 * H), A, '$R_1$', text_spacing=1. / 2)
    R1.set_line_width(3).set_line_color('black')
    R2 = Force(B - Point(0, 2 * H),
               support.geometric_features()['mid_support'],
               '$R_2$', text_spacing=1. / 2)
    R2.set_line_width(3).set_line_color('black')
    M1 = Moment('$M_1$', center=A + Point(-H, H / 2), radius=H / 2,
                left=True, text_spacing=1 / 3.)
    M1.line_color = 'black'

    ab_level = Point(0, 3 * h)
    a_dim = Distance_wText(A - ab_level, B - ab_level, '$a$')
    b_dim = Distance_wText(B - ab_level, C - ab_level, '$b$')
    dims = Composition({'a': a_dim, 'b': b_dim})
    symbols = Composition(
        {'R1': R1, 'R2': R2, 'M1': M1,
         'w': load, 'w text': load_text,
         'A': Text('$A$', A + Point(0.7 * h, -0.9 * h)),
         'B': Text('$B$',
                   support.geometric_features()['mid_support'] -
                   Point(1.25 * h, 0)),
         'C': Text('$C$', C + Point(h / 2, -h / 2))})

    x_axis = Axis(A + Point(L + h, H / 2), 2 * H, '$x$', ). \
        set_line_color('black')
    y_axis = Axis(A + Point(0, H / 2), 3.5 * H, '$y$',
                  rotation_angle=np.pi / 2).set_line_color('black')
    axes = Composition({'x axis': x_axis, 'y axis': y_axis})

    annotations = Composition({'dims': dims, 'symbols': symbols,
                               'axes': axes})
    beam = Composition({'beam': beam, 'support': support,
                        'clamped end': clamped, 'load': load})

    def deflection(x, a, b, w) -> float:
        R1 = 5. / 8 * w * a - 3 * w * b ** 2 / (4 * a)
        R2 = 3. / 8 * w * a + w * b + 3 * w * b ** 2 / (4 * a)
        M1 = R1 * a / 3 - w * a ** 2 / 12
        y = -(M1 / 2.) * x ** 2 + 1. / 6 * R1 * x ** 3 - w / 24. * x ** 4 + \
            1. / 6 * R2 * np.where(x > a, 1, 0) * (x - a) ** 3
        return y

    xs = np.linspace(0, L, 101)
    ys = deflection(xs, a, b, w=1.0)
    ys /= abs(ys.max() - ys.min())
    ys += A.y + H / 2
    points = Point.from_coordinate_lists(xs, ys)

    elastic_line = Curve(points). \
        set_line_color('red'). \
        set_line_style('dashed'). \
        set_line_width(3)

    beam.draw(drawing_tool)
    drawing_tool.display()

    import time
    time.sleep(1.5)

    annotations.draw(drawing_tool)
    drawing_tool.display()
    time.sleep(1.5)

    elastic_line.draw(drawing_tool)
    drawing_tool.display()
    # beam.draw_dimensions()
    # test_Dashpot(xpos+2*W)


beam()
