"""A more sophisticated beam than in beam1.py."""
from pysketcher import *

def beam():
    L = 8.0
    a = 3*L/4
    b = L - a
    H = 1.0
    xpos = 0.0
    ypos = 3.0

    drawing_tool.set_coordinate_system(
        xmin=-3, xmax=xpos+1.5*L,
        ymin=0, ymax=ypos+5*H,
        axis=False)
    drawing_tool.set_linecolor('blue')
    #drawing_tool.set_grid(True)
    drawing_tool.set_fontsize(16)

    A = point(xpos,ypos)

    beam = Rectangle(A, L, H)

    h = L/16  # size of support, clamped wall etc

    clamped = Rectangle(A - point(h,0) - point(0,2*h), h,
                        6*h).set_filled_curves(pattern='/')

    load = ConstantBeamLoad(A + point(0,H), L, H)
    load.set_linewidth(1).set_linecolor('black')
    load_text = Text('$w$',
                     load.geometric_features()['mid_top'] +
                     point(0,h/2.))

    B = A + point(a, 0)
    C = B + point(b, 0)

    support = SimplySupportedBeam(B, h)  # pt B is simply supported


    R1 = Force(A-point(0,2*H), A, '$R_1$', text_spacing=1./50)
    R1.set_linewidth(3).set_linecolor('black')
    R2 = Force(B-point(0,2*H),
               support.geometric_features()['mid_support'],
               '$R_2$', text_spacing=1./50)
    R2.set_linewidth(3).set_linecolor('black')
    M1 = Moment('$M_1$', center=A + point(-H, H/2), radius=H/2,
                left=True, text_spacing=1/30.)
    M1.set_linecolor('black')

    ab_level = point(0, 3*h)
    a_dim = Distance_wText(A - ab_level, B - ab_level, '$a$')
    b_dim = Distance_wText(B - ab_level, C - ab_level, '$b$')
    dims = Composition({'a': a_dim, 'b': b_dim})
    symbols = Composition(
        {'R1': R1, 'R2': R2, 'M1': M1,
         'w': load, 'w text': load_text,
         'A': Text('$A$', A+point(0.7*h,-0.9*h)),
         'B': Text('$B$',
                   support.geometric_features()['mid_support']-
                   point(1.25*h,0)),
         'C': Text('$C$', C+point(h/2,-h/2))})

    x_axis = Axis(A + point(L+h, H/2), 2*H, '$x$',).\
             set_linecolor('black')
    y_axis = Axis(A + point(0,H/2), 3.5*H, '$y$',
                  label_alignment='left',
                  rotation_angle=90).set_linecolor('black')
    axes = Composition({'x axis': x_axis, 'y axis': y_axis})

    annotations = Composition({'dims': dims, 'symbols': symbols,
                               'axes': axes})
    beam = Composition({'beam': beam, 'support': support,
                        'clamped end': clamped, 'load': load})

    def deflection(x, a, b, w):
        import numpy as np
        R1 = 5./8*w*a - 3*w*b**2/(4*a)
        R2 = 3./8*w*a + w*b + 3*w*b**2/(4*a)
        M1 = R1*a/3 - w*a**2/12
        y = -(M1/2.)*x**2 + 1./6*R1*x**3 - w/24.*x**4 + \
            1./6*R2*np.where(x > a, 1, 0)*(x-a)**3
        return y

    x = linspace(0, L, 101)
    y = deflection(x, a, b, w=1.0)
    y /= abs(y.max() - y.min())
    y += ypos + H/2

    elastic_line = Curve(x, y).\
                   set_linecolor('red').\
                   set_linestyle('dashed').\
                   set_linewidth(3)

    beam.draw()
    drawing_tool.display()
    drawing_tool.savefig('tmp_beam2_1')

    import time
    time.sleep(1.5)

    annotations.draw()
    drawing_tool.display()
    drawing_tool.savefig('tmp_beam2_2')
    time.sleep(1.5)

    elastic_line.draw()
    drawing_tool.display()
    drawing_tool.savefig('tmp_beam2_3')
    #beam.draw_dimensions()
    #test_Dashpot(xpos+2*W)

beam()
input()
