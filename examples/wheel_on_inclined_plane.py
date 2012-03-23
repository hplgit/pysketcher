import sys, os
sys.path.insert(0, os.path.join(os.pardir, 'pysketcher'))
from shapes import *

print dir()
print 'drawin_tool' in dir()

def inclined_plane():
    drawing_tool.set_coordinate_system(xmin=0, xmax=15,
                                       ymin=-1, ymax=10,
                                       #axis=True,
                                       )
    #drawing_tool.set_grid(True)
    fontsize = 18
    from math import tan, radians

    theta = 30.
    L = 10.
    a = 1.
    B = point(a+L, 0)
    A = point(a, tan(radians(theta))*L)

    wall = CurveWall(x=[A[0], B[0]], y=[A[1], B[1]], thickness=-0.25)

    angle = ArcSymbol(r'$\theta$', center=B, radius=3,
                      start_angle=180-theta, arc_angle=theta,
                      fontsize=fontsize)
    angle.set_linecolor('black')
    angle.set_linewidth(1)

    ground = Line((B[0]-L/10., 0), (B[0]-L/2.,0))
    ground.set_linecolor('black')
    ground.set_linestyle('dashed')
    ground.set_linewidth(1)

    r = 1  # radius of wheel
    help_line = Line(A, B)
    x = a + 3*L/10.; y = help_line(x=x)
    contact = point(x, y)
    normal_vec = point(sin(radians(theta)), cos(radians(theta)))
    c = contact + r*normal_vec
    outer_wheel = Circle(c, r)
    outer_wheel.set_linecolor('blue')
    outer_wheel.set_filled_curves('blue')
    hole = Circle(c, r/2.)
    hole.set_linecolor('blue')
    hole.set_filled_curves('white')

    wheel = Compose({'outer': outer_wheel, 'inner': hole})

    drawing_tool.set_linecolor('black')
    N_arr = Arrow3((4,2), 2)
    N_arr.rotate(-theta, (4,4))
    N_text = Text('$N$', (3.7,2.6), fontsize=fontsize)
    N_force = Compose({'arrow': N_arr, 'symbol': N_text})

    g = Gravity(c, 2.5)

    x_const = Line(contact, contact + point(0,4))
    x_const.set_linestyle('dotted')
    x_const.rotate(-theta, contact)
    x_axis_start = point(5.5, x_const(x=5.5))
    x_axis = Axis(x_axis_start, 2*L/5, '$x$', rotation_angle=-theta)

    body  = Compose({'wheel': wheel, 'N force': N_force, 'g': g})
    fixed = Compose({'angle': angle, 'inclined wall': wall,
                     'wheel': wheel, 'ground': ground,
                     'x start': x_const, 'x axis': x_axis})

    fig = Compose({'body': body, 'fixed elements': fixed})

    #import copy
    #body2 = copy.deepcopy(body)
    #body2.translate(3, 0)
    #body2.draw()

    fig.draw()
    drawing_tool.savefig('tmp.png')
    drawing_tool.display()
    import time
    time.sleep(1)
    tangent_vec = point(normal_vec[1], -normal_vec[0])
    print 'loop'
    for t in range(7):
        drawing_tool.erase()
        body.translate(0.2*t*tangent_vec)
        time.sleep(0.5)
        fig.draw()
        drawing_tool.display()
    print str(fig)
    print repr(fig)

inclined_plane()
raw_input()
