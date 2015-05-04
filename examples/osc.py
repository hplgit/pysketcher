from pysketcher import *

L = 12.
H = L/6
W = L/6

xmax = L
drawing_tool.set_coordinate_system(xmin=-L, xmax=xmax,
                                   ymin=-1, ymax=L+H,
                                   axis=False,
                                   instruction_file='tmp_mpl.py')
x = 0
drawing_tool.set_linecolor('black')

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

M = Rectangle((0,H), 4*H, 4*H).set_linewidth(4)
left_wall = Rectangle((-L,0),H/10,4*H).set_filled_curves(pattern='/')
ground = Wall(x=[-L/2,L], y=[0,0], thickness=-H/10)
wheel1 = Circle((H,H/2), H/2)
wheel2 = wheel1.copy()
wheel2.translate(point(2*H, 0))

fontsize = 18
text_m = Text('$m$', (2*H, H+2*H), fontsize=fontsize)
text_kx = Text('$kx$', (-L/2, H+4*H), fontsize=fontsize)
text_bv = Text('$b\dot x$', (-L/2, H), fontsize=fontsize)
x_axis = Axis((2*H, L), H, '$x(t)$', fontsize=fontsize,
              label_spacing=(0.04, -0.01))
x_axis_start = Line((2*H, L-H/4), (2*H, L+H/4)).set_linewidth(4)

fig = Composition({
    'dashpot': d, 'spring': s, 'mass': M, 'left wall': left_wall,
    'ground': ground, 'wheel1': wheel1, 'wheel2': wheel2,
    'text_m': text_m, 'text_kx': text_kx, 'text_bv': text_bv,
    'x_axis': x_axis, 'x_axis_start': x_axis_start})

fig.draw()
#s.draw()
print s
print s.shapes['bar1']['line'].x, s.shapes['bar1']['line'].y
print s.shapes['bar2']['line'].x, s.shapes['bar2']['line'].y
drawing_tool.display()
drawing_tool.savefig('oscillator')
raw_input()
