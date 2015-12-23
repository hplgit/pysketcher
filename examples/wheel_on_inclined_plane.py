from pysketcher import *

def inclined_plane():
    theta = 30.
    L = 10.
    a = 1.
    xmin = 0
    ymin = -3

    drawing_tool.set_coordinate_system(xmin=xmin, xmax=xmin+1.5*L,
                                       ymin=ymin, ymax=ymin+L,
                                       #axis=True,
                                       instruction_file='tmp_mpl.py'
                                       )
    #drawing_tool.set_grid(True)
    fontsize = 18
    from math import tan, radians

    B = point(a+L, 0)
    A = point(a, tan(radians(theta))*L)

    wall = Wall(x=[A[0], B[0]], y=[A[1], B[1]], thickness=-0.25,
                transparent=False)

    angle = Arc_wText(r'$\theta$', center=B, radius=3,
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

    wheel = Composition({'outer': outer_wheel, 'inner': hole})
    wheel.set_shadow(4)

    drawing_tool.set_linecolor('black')
    N = Force(contact - 2*r*normal_vec, contact, r'$N$', text_pos='start')
              #text_alignment='left')
    mg = Gravity(c, 3*r, text='$Mg$')

    x_const = Line(contact, contact + point(0,4))
    x_const.set_linestyle('dotted')
    x_const.rotate(-theta, contact)
    # or x_const = Line(contact-2*r*normal_vec, contact+4*r*normal_vec).set_linestyle('dotted')
    x_axis = Axis(start=contact+ 3*r*normal_vec, length=4*r,
                  label='$x$', rotation_angle=-theta)

    body  = Composition({'wheel': wheel, 'N': N, 'mg': mg})
    fixed = Composition({'angle': angle, 'inclined wall': wall,
                         'wheel': wheel, 'ground': ground,
                         'x start': x_const, 'x axis': x_axis})

    fig = Composition({'body': body, 'fixed elements': fixed})

    fig.draw()
    drawing_tool.savefig('tmp.png')
    drawing_tool.savefig('tmp.pdf')
    drawing_tool.display()
    import time
    time.sleep(1)
    tangent_vec = point(normal_vec[1], -normal_vec[0])

    import numpy
    time_points = numpy.linspace(0, 1, 31)

    def position(t):
        """Position of center point of wheel."""
        return c + 7*t**2*tangent_vec

    def move(t, fig, dt=None):
        x = position(t)
        x0 = position(t-dt)
        displacement = x - x0
        fig['body'].translate(displacement)


    animate(fig, time_points, move, pause_per_frame=0,
            dt=time_points[1]-time_points[0])

    print(str(fig))
    print(repr(fig))

inclined_plane()
input()
