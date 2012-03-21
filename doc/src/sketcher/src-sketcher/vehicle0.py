import sys, os, time
sys.path.insert(0, os.path.join(os.pardir, os.pardir, os.pardir, os.pardir))
from pysketcher import *

drawing_tool.set_coordinate_system(xmin=0, xmax=15,
                                   ymin=-1, ymax=10)
R = 1  # radius of wheel
wheel1 = Circle(center=(4, R), radius=R)
wheel2 = wheel1.copy()
wheel2.translate((4,0))

height1 = 2
under = Rectangle(lower_left_corner=(2, 2*R),
                  width=8, height=height1)
height2 = 2.5
over = Rectangle(lower_left_corner=(4, 2*R+height1),
                 width=2.5, height=height2)

wheels = Compose({'wheel1': wheel1, 'wheel2': wheel2})
body = Compose({'under': under, 'over': over})

vehicle = Compose({'wheels': wheels, 'body': body})
ground = CurveWall(x=[0, 12], y=[0, 0], thickness=-0.3)

fig = Compose({'vehicle': vehicle, 'ground': ground})
fig.draw()  # send all figures to plotting backend

drawing_tool.display()
drawing_tool.savefig('tmp1.png')

fig['vehicle']['wheels'].set_filled_curves('blue')
fig['vehicle']['wheels'].set_linewidth(6)
fig['vehicle']['wheels'].set_linecolor('black')
fig['vehicle']['body']['under'].set_filled_curves('red')
fig['vehicle']['body']['over'].set_filled_curves(pattern='/')
fig['vehicle']['body']['over'].set_linewidth(10)

drawing_tool.erase()  # avoid drawing old and new fig on top of each other
fig.draw()
drawing_tool.display()
drawing_tool.savefig('tmp2.png')

print fig

time.sleep(1)

# Animate motion
fig['vehicle'].translate((3,0))  # move to start point for "driving"

def v(t):
    return point(-t*(1-t/5.), 0)

import numpy
tp = numpy.linspace(0, 5, 35)
dt = tp[1] - tp[0]  # time step

def move_vehicle(t, fig):
    displacement = dt*v(t)
    fig['vehicle'].translate(displacement)

files = animate(fig, tp, move_vehicle, moviefiles=True,
                pause_per_frame=0)

from scitools.std import movie
movie(files, encoder='html', output_file='anim')

raw_input()
