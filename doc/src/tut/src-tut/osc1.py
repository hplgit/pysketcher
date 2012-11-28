from pysketcher import *

L = 12.
H = L/6
W = L/6

xmax = L
drawing_tool.set_coordinate_system(xmin=-L, xmax=xmax,
                                   ymin=-1, ymax=L,
                                   axis=True,
                                   instruction_file='tmp_mpl.py')
x = 0

def make_dashpot(x):
    d_start = (-L,2*H)
    d = Dashpot(start=d_start, total_length=L+x, width=W,
                bar_length=3*H/2, dashpot_length=L/2, piston_pos=H+x)
    d.rotate(-90, d_start)
    return d

def make_spring(x):
    s_start = (-L,4*H)
    s = Spring(start=s_start, length=L+x, bar_length=3*H/2, teeth=True)
    s.rotate(-90, s_start)
    return s

d = make_dashpot(0)
s = make_spring(0)

M = Rectangle((0,H), 4*H, 4*H)
left_wall = Rectangle((-L,0),H/10,4*H).set_filled_curves(pattern='/')
ground = Wall(x=[-L/2,L], y=[0,0], thickness=-H/10)
wheel1 = Circle((H,H/2), H/2)
wheel2 = wheel1.copy()
wheel2.translate(point(2*H, 0))
fig = Compose({
    'dashpot': d, 'spring': s, 'mass': M, 'left wall': left_wall,
    'ground': ground, 'wheel1': wheel1, 'wheel2': wheel2})

fig.draw()
#s.draw()
print s
print s.shapes['bar1']['line'].x, s.shapes['bar1']['line'].y
print s.shapes['bar2']['line'].x, s.shapes['bar2']['line'].y
drawing_tool.display()
raw_input()
