"""
Illustrate forward, backward and centered finite differences
in four figures.
"""

from pysketcher import *

#test_test()
xaxis = 2
drawing_tool.set_coordinate_system(0, 7, 1, 6, axis=False)

f = SketchyFunc1('$u(t)$')
x = 3                 # center point where we want the derivative
xb = 2                # x point used for backward difference
xf = 4                # x point used for forward difference
p = (x, f(x))         # center point
pf = (xf, f(xf))      # forward point
pb = (xb, f(xb))      # backward point
r = 0.1               # radius of circles placed at key points
c = Circle(p, r).set_linecolor('blue')
cf = Circle(pf, r).set_linecolor('red')
cb = Circle(pb, r).set_linecolor('green')

# Points in the mesh
p0 = point(x, xaxis)        # center point
pf0 = point(xf, xaxis)      # forward point
pb0 = point(xb, xaxis)      # backward point
tick = 0.05

# 1D mesh with three points
mesh = Composition({
    'tnm1': Text('$t_{n-1}$', pb0 - point(0, 0.3)),
    'tn': Text('$t_{n}$', p0 - point(0, 0.3)),
    'tnp1': Text('$t_{n+1}$', pf0 - point(0, 0.3)),
    'axis': Composition({
        'hline': Line(pf0-point(3,0), pb0+point(3,0)).\
        set_linecolor('black').set_linewidth(1),
        'tick_m1': Line(pf0+point(0,tick), pf0-point(0,tick)).\
        set_linecolor('black').set_linewidth(1),
        'tick_n':  Line(p0+point(0,tick), p0-point(0,tick)).\
        set_linecolor('black').set_linewidth(1),
        'tick_p1': Line(pb0+point(0,tick), pb0-point(0,tick)).\
        set_linecolor('black').set_linewidth(1)}),
    })

# 1D mesh with three points for Crank-Nicolson
mesh_cn = Composition({
    'tnm1': Text('$t_{n}$', pb0 - point(0, 0.3)),
    'tn': Text(r'$t_{n+\frac{1}{2}}$', p0 - point(0, 0.3)),
    'tnp1': Text('$t_{n+1}$', pf0 - point(0, 0.3)),
    'axis': Composition({
        'hline': Line(pf0-point(3,0), pb0+point(3,0)).\
        set_linecolor('black').set_linewidth(1),
        'tick_m1': Line(pf0+point(0,tick), pf0-point(0,tick)).\
        set_linecolor('black').set_linewidth(1),
        'tick_n':  Line(p0+point(0,tick), p0-point(0,tick)).\
        set_linecolor('black').set_linewidth(1),
        'tick_p1': Line(pb0+point(0,tick), pb0-point(0,tick)).\
        set_linecolor('black').set_linewidth(1)}),
    })

# Vertical dotted lines at each mesh point
vlinec = Line(p, p0).set_linestyle('dotted').\
         set_linecolor('blue').set_linewidth(1)
vlinef = Line(pf, pf0).set_linestyle('dotted').\
         set_linecolor('red').set_linewidth(1)
vlineb = Line(pb, pb0).set_linestyle('dotted').\
         set_linecolor('green').set_linewidth(1)

# Compose vertical lines for each type of difference
forward_lines = Composition({'center': vlinec, 'right': vlinef})
backward_lines = Composition({'center': vlinec, 'left': vlineb})
centered_lines = Composition({'left': vlineb, 'right': vlinef})
centered_lines2 = Composition({'left': vlineb, 'right': vlinef,
                               'center': vlinec})

# Tangents illustrating the derivative
domain = [1, 5]
domain2 = [2, 5]
forward_tangent = Line(p, pf).new_interval(x=domain2).\
                  set_linestyle('dashed').set_linecolor('red')
backward_tangent = Line(pb, p).new_interval(x=domain).\
                   set_linestyle('dashed').set_linecolor('green')
centered_tangent = Line(pb, pf).new_interval(x=domain).\
                   set_linestyle('dashed').set_linecolor('blue')
h = 1E-3  # h in finite difference approx used to compute the exact tangent
exact_tangent = Line((x+h, f(x+h)), (x-h, f(x-h))).\
                new_interval(x=domain).\
                set_linestyle('dotted').set_linecolor('black')

forward = Composition(
    dict(tangent=forward_tangent,
         point1=c, point2=cf, coor=forward_lines,
         name=Text('forward',
                   forward_tangent.geometric_features()['end'] + \
                   point(0.1,0), alignment='left')))
backward = Composition(
    dict(tangent=backward_tangent,
         point1=c, point2=cb, coor=backward_lines,
         name=Text('backward',
                   backward_tangent.geometric_features()['end'] + \
                   point(0.1,0), alignment='left')))
centered = Composition(
    dict(tangent=centered_tangent,
         point1=cb, point2=cf, point=c, coor=centered_lines2,
         name=Text('centered',
                   centered_tangent.geometric_features()['end'] + \
                   point(0.1,0), alignment='left')))

exact = Composition(dict(graph=f, tangent=exact_tangent))
forward = Composition(dict(difference=forward, exact=exact)).\
          set_name('forward')
backward = Composition(dict(difference=backward, exact=exact)).\
           set_name('backward')
centered = Composition(dict(difference=centered, exact=exact)).\
           set_name('centered')
all = Composition(
    dict(exact=exact, forward=forward, backward=backward,
         centered=centered)).set_name('all')

for fig in forward, backward, centered, all:
    drawing_tool.erase()
    fig.draw()
    mesh.draw()
    drawing_tool.display()
    drawing_tool.savefig('fd_'+fig.get_name())
# Crank-Nicolson around t_n+1/2
drawing_tool.erase()
centered.draw()
mesh_cn.draw()
drawing_tool.display()
drawing_tool.savefig('fd_centered_CN')

input()

