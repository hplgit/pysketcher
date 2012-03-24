from pysketcher import *

L = 8.0
a = 3*L/4
b = L - a
H = 1.0
xpos = 0.0
ypos = 3.0

drawing_tool.set_coordinate_system(xmin=-3, xmax=xpos+1.5*L,
                                   ymin=0, ymax=ypos+5*H,
                                   axis=True)
drawing_tool.set_linecolor('blue')
drawing_tool.set_grid(True)

fontsize=16
A = point(xpos,ypos)
main = Rectangle(A, L, H)
h = L/16  # size of support, clamped wall etc
clamped = Rectangle(A - point(h,0) - point(0,2*h), h, 6*h).set_filled_curves(pattern='/')

load = ConstantBeamLoad(A + point(0,H), L, H)
load.set_linewidth(1).set_linecolor('black')
load_text = Text('$w$', load.mid_top + point(0,h/2.), fontsize=fontsize)

B = A + point(a, 0)
C = B + point(b, 0)

support = SimplySupportedBeam(B, h)


R1 = Force(A-point(0,2*H), A, '$R_1$',
           fontsize=fontsize, symbol_spacing=1./20)
R1.set_linewidth(3).set_linecolor('black')
R2 = Force(B-point(0,2*H), support.mid_support,
           '$R_2$', fontsize=fontsize, symbol_spacing=1./20)
R2.set_linewidth(3).set_linecolor('black')
M1 = Moment('$M_1$', center=A + point(-H, H/2), radius=H/2,
            left=True, fontsize=fontsize,
            symbol_spacing=1/30.)
M1.set_linecolor('black')

ab_level = point(0, 3*h)
a_dim = Distance_wText(A - ab_level, B - ab_level, '$a$',
                       fontsize=fontsize)
b_dim = Distance_wText(B - ab_level, C - ab_level, '$b$',
                       fontsize=fontsize)
dims = Compose({'a': a_dim, 'b': b_dim})
symbols = Compose({'R1': R1, 'R2': R2, 'M1': M1,
                   'w': load, 'w text': load_text,
                   'A': Text('$A$', A+point(h/2,-h/2)),
                   'B': Text('$B$', support.mid_support-point(h,0)),
                   'C': Text('$C$', C+point(h/2,-h/2))})

x_axis = Axis(A + point(L+h, H/2), 2*H, '$x$',
              fontsize=fontsize).set_linecolor('black')
y_axis = Axis(A + point(0,H/2), 3.5*H, '$y$',
              below=False, rotation_angle=90,
              fontsize=fontsize).set_linecolor('black')
axes = Compose({'x axis': x_axis, 'y axis': y_axis})

annotations = Compose({'dims': dims, 'symbols': symbols,
                'axes': axes})
beam = Compose({'main': main, 'support': support,
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

elastic_line = Curve(x, y).set_linecolor('red').set_linestyle('dashed').set_linewidth(3)

beam.draw()
drawing_tool.display()
drawing_tool.savefig('tmp_beam2_1.png')

import time
time.sleep(1.5)

annotations.draw()
drawing_tool.display()
drawing_tool.savefig('tmp_beam2_1.png')
time.sleep(1.5)

elastic_line.draw()
drawing_tool.display()
drawing_tool.savefig('tmp_beam2_3.png')
#beam.draw_dimensions()

#test_Dashpot(xpos+2*W)

raw_input()
