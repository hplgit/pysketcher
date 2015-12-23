"""Comic strip for illustrating Euler's method for ODEs."""

from pysketcher import *
import numpy as np
xkcd = True

xmin = 0
drawing_tool.set_coordinate_system(xmin=xmin, xmax=4,
                                   ymin=0, ymax=2.5,
                                   axis=True, xkcd=xkcd)
drawing_tool.set_linecolor('blue')

def ForwardEuler(I, a, T, dt):
    u = [I]
    t = [0]
    while t[-1] <= T:
        u_new = u[-1] - a*dt*u[-1]
        u.append(u_new)
        t.append(t[-1] + dt)
    return np.array(u), np.array(t)

def make_fig(dt=0.5, heading=''):
    I = 2
    a = 0.5
    T_e = 3
    T_FE = 1
    t_fine = np.linspace(0, T_e, 101)
    u_e = I*np.exp(-a*t_fine)

    u, t = ForwardEuler(I, a, T_FE, dt)

    # y = slope*(x - x0) + y0
    # u_extrapolated = -a*u[-1]*(t - t[-1]) + u[-1]
    t_future = t[-1] + 1.5   # let the line be longer than one step
    line = Line((t[-1], u[-1]), (t_future, -a*u[-1]*(t_future - t[-1]) + u[-1]))

    circles = {
        i: Circle((t[i], u[i]), 0.05).set_linecolor('red').set_filled_curves('red')
        for i in range(1, len(u))}
    # Add next predicted point
    t_next = t[-1] + dt
    u_next = -a*u[-1]*(t_next - t[-1]) + u[-1]
    circles[0] = Circle((t_next, u_next), 0.05).\
                 set_linecolor('red').set_filled_curves('red')
    circles = Composition(circles)

    curves = Composition(dict(
        exact=Curve(t_fine, u_e).set_linestyle('dashed'),
        numerical=Curve(t, u),
        extrapolation=line.set_linecolor('red').set_linewidth(3)))

    text_exact = Text_wArrow("exact solution", (2.5, 1), (2.5, I*np.exp(-a*2.5)),
                             alignment='left')

    text_predict = Text_wArrow("Here we know the slope:\n$u'=f(u,t)$!\nLet the solution continue\nalong that slope.",
                               (1.7, 1.7), (t[-1], u[-1]),
                               alignment='left')
    text_next = Text_wArrow("This is the next\npredicted point",
                            (1, 0.25), (t_next, u_next),
                            alignment='left')

    text_comment = Text(heading, (0.3, 2.05), alignment='left')

    fig = Composition(dict(curves=curves,
                           circles=circles,
                           exact=text_exact,
                           predict=text_predict,
                           next=text_next,
                           comment=text_comment))
    return fig

fig = make_fig(dt=0.5, heading="Differential equations $u'=f(u,t)$\nare hard to solve,\nbut not with programming!")
fig.draw()
drawing_tool.display()
drawing_tool.savefig('tmp1')

drawing_tool.erase()
fig = make_fig(dt=0.24, heading='Just reduce the time step\nto make more accurate\npredictions!')
fig.draw()
drawing_tool.display()
drawing_tool.savefig('tmp2')

import os
comic = 'comic' if xkcd else 'non_comic'
os.system('doconce combine_images pdf -2 tmp1 tmp2 FE_%s_strip' % comic)
os.system('doconce combine_images png -2 tmp1 tmp2 FE_%s_strip' % comic)

input()
