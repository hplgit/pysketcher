from pysketcher import *

u = SketchyFunc1('$u(t)$', name_pos='end')
t_mesh = [0, 2, 4, 6, 8]

u = SketchyFunc2('$u(t)$', name_pos='end')
n = 7
t_mesh = [i*2.25/(n-1) for i in range(n)]

t_min1 = t_mesh[0] - 0.2*(t_mesh[-1] - t_mesh[0])
t_max1 = t_mesh[-1] + 0.2*(t_mesh[-1] - t_mesh[0])
t_min2 = t_mesh[0] - 0.3*(t_mesh[-1] - t_mesh[0])
t_max2 = t_mesh[-1] + 0.3*(t_mesh[-1] - t_mesh[0])
u_max = 1.3*max([u(t) for t in t_mesh])
u_min = -0.2*u_max

drawing_tool.set_coordinate_system(t_min2, t_max2, u_min, u_max, axis=False)
drawing_tool.set_linecolor('black')

r = 0.005*(t_max2-t_min2)     # radius of circles placed at mesh points
discrete_u = Composition({i: Circle(point(t, u(t)), r).\
                          set_filled_curves('black')
                          for i, t in enumerate(t_mesh)})
print repr(discrete_u)
axes = Composition(dict(x=Axis(point(0,0), t_max2, '$t$'),
                        y=Axis(point(0,0), 0.8*u_max, '$u$',
                               rotation_angle=90)))
h = 0.03*u_max  # tickmarks height
nodes = Composition({i: Composition(dict(
    node=Line(point(t,h), point(t,-h)),
    name=Text('$t_%d$' % i, point(t,-3.5*h))))
                     for i, t in enumerate(t_mesh)})
fig = Composition(dict(u=discrete_u, mesh=nodes, axes=axes)).set_name('fdm_u')
drawing_tool.erase()
fig.draw()
drawing_tool.display()
drawing_tool.savefig(fig.get_name())
raw_input()

