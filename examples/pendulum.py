from pysketcher import *

H = 7.
W = 6.

drawing_tool.set_coordinate_system(xmin=0, xmax=W,
                                   ymin=0, ymax=H,
                                   axis=False)
drawing_tool.set_linecolor('blue')
#drawing_tool.set_grid(True)

def set_dashed_thin_blackline(*objects):
    """Set linestyle of an object to dashed, black, width=1."""
    for obj in objects:
        obj.set_linestyle('dashed')
        obj.set_linecolor('black')
        obj.set_linewidth(1)


L = 5*H/7          # length
P = (W/6, 0.85*H)  # rotation point
a = 40             # angle

path = Arc(P, L, -90, a)
angle = Arc_wText(r'$\theta$', P, L/4, -90, a, text_spacing=1/30.)
vertical = Line(P, P-point(0,L))

rod = Line(P, P + L*point(sin(radians(a)), -L*cos(radians(a))))
# or shorter (and more reliable)
mass_pt = path.geometric_features()['end']
rod = Line(P, mass_pt)

mass = Circle(center=mass_pt, radius=L/20.)
mass.set_filled_curves(color='blue')
rod_vec = rod.geometric_features()['end'] - rod.geometric_features()['start']
mass_symbol = Text('$m$', mass_pt + L/10*unit_vec(rod_vec))

length = Distance_wText(P, mass_pt, '$L$')
# Displace length indication
length.translate(L/15*point(cos(radians(a)), sin(radians(a))))
gravity = Gravity(start=P+point(0.8*L,0), length=L/3)

set_dashed_thin_blackline(vertical, path)

dims = Composition(
    {'vertical': vertical, 'theta': angle, 'path': path,
     'g': gravity, 'L': length, 'm': mass_symbol})

fig = Composition({'body': mass, 'rod': rod, 'dims': dims})

fig.draw()
drawing_tool.display()
drawing_tool.savefig('tmp_pendulum1')

# Draw body diagram
raw_input('Press Return to make body diagram: ')
#import time; time.sleep(3)
drawing_tool.erase()

drawing_tool.set_linecolor('black')
mg_force = Force(mass_pt, mass_pt + L/5*point(0,-1), '$mg$', text_pos='end')
rod_force = Force(mass_pt, mass_pt - L/3*unit_vec(rod_vec),
                  '$S$', text_pos='end')

rod_start = rod.geometric_features()['start']
vertical2 = Line(rod_start, rod_start + point(0,-L/3))
set_dashed_thin_blackline(vertical2)
set_dashed_thin_blackline(rod)
angle2 = Arc_wText(r'$\theta$', rod_start, L/6, -90, a, text_spacing=1/30.)

# Cannot understand this one:
#path2 = Arc(P, L, -90+a-a/2., a)
#path2.set_arrow('<-')
#path2.set_linestyle('dashed')

body_diagram = Composition(
    {'mg': mg_force, 'S': rod_force, 'rod': rod,
     'vertical': vertical2, 'theta': angle2,
     #'path': path2,
     'body': mass, 'm': mass_symbol})

body_diagram.draw()
drawing_tool.display('Body diagram')
drawing_tool.savefig('tmp_pendulum2')

drawing_tool.adjust_coordinate_system(body_diagram.minmax_coordinates(), 90)
drawing_tool.display('Body diagram')
drawing_tool.savefig('tmp_pendulum3')

raw_input()
