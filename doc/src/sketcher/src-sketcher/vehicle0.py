from pysketcher import *

R = 1    # radius of wheel
L = 4    # distance between wheels
H = 2    # height of vehicle body
w_1 = 5  # position of front wheel

drawing_tool.set_coordinate_system(xmin=0, xmax=w_1 + 2*L + 3*R,
                                   ymin=-1, ymax=2*R + 3*H,
                                   axis=False)

wheel1 = Circle(center=(w_1, R), radius=R)
wheel2 = wheel1.copy()
wheel2.translate((L,0))

under = Rectangle(lower_left_corner=(w_1-2*R, 2*R),
                  width=2*R + L + 2*R, height=H)
over  = Rectangle(lower_left_corner=(w_1, 2*R + H),
                  width=2.5*R, height=1.25*H)

wheels = Compose({'wheel1': wheel1, 'wheel2': wheel2})
body = Compose({'under': under, 'over': over})

vehicle = Compose({'wheels': wheels, 'body': body})
ground = CurveWall(x=[w_1 - L, w_1 + 3*L], y=[0, 0],
                   thickness=-0.3*R)

fig = Compose({'vehicle': vehicle, 'ground': ground})
fig.draw()  # send all figures to plotting backend

drawing_tool.display()
drawing_tool.savefig('tmp1.png')

fig['vehicle']['wheels'].set_filled_curves('blue')
fig['vehicle']['wheels'].set_linewidth(6)
fig['vehicle']['wheels'].set_linecolor('black')
fig['vehicle']['body']['under'].set_filled_curves('red')
fig['vehicle']['body']['over'].set_filled_curves(pattern='/')
fig['vehicle']['body']['over'].set_linewidth(14)

drawing_tool.erase()  # avoid drawing old and new fig on top of each other
fig.draw()
drawing_tool.display()
drawing_tool.savefig('tmp2.png')

print fig

import time
time.sleep(1)

# Animate motion
fig['vehicle'].translate((L,0))  # move to start point for "driving"

def v(t):
    return -8*R*t*(1 - t/(2*R))

import numpy
tp = numpy.linspace(0, 2*R, 25)
dt = tp[1] - tp[0]  # time step

def move_vehicle(t, fig):
    x_displacement = dt*v(t)
    fig['vehicle'].translate((x_displacement, 0))

files = animate(fig, tp, move_vehicle, moviefiles=True,
                pause_per_frame=0)

from scitools.std import movie
movie(files, encoder='html', output_file='anim')

raw_input()
