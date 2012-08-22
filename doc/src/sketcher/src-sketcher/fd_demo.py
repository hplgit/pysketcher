from pysketcher import *

#test_test()
drawing_tool.set_coordinate_system(0, 7, 2, 6, axis=False)

f = SketchyFunc1('$f(x)$')
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
domain = [1, 5]
domain2 = [2, 5]
lf = Line(p, pf).new_interval(x=domain2).set_linestyle('dashed').set_linecolor('red')
lb = Line(pb, p).new_interval(x=domain).set_linestyle('dashed').set_linecolor('green')
lc = Line(pb, pf).new_interval(x=domain).set_linestyle('dashed').set_linecolor('blue')
h = 1E-3
le = Line((x+h, f(x+h)), (x-h, f(x-h))).new_interval(x=domain).set_linestyle('dotted').set_linecolor('black')

forward = Composition(dict(tangent=lf, point1=c, point2=cf,
                      name=Text('forward',
                                lf.geometric_features()['end'] + point(0.1,0),
                                alignment='left')))
backward = Composition(dict(tangent=lb, point1=c, point2=cb,
                      name=Text('backward',
                                lb.geometric_features()['end'] + point(0.1,0),
                                alignment='left')))
centered = Composition(dict(tangent=lc, point1=cb, point2=cf,
                       name=Text('centered',
                                 lc.geometric_features()['end'] + point(0.1,0),
                                 alignment='left')))

exact = Composition(dict(graph=f, tangent=le))
forward = Composition(dict(difference=forward, exact=exact)).set_name('forward')
backward = Composition(dict(difference=backward, exact=exact)).set_name('backward')
centered = Composition(dict(difference=centered, exact=exact)).set_name('centered')
all = Composition(dict(exact=exact, forward=forward, backward=backward,
                       centered=centered)).set_name('all')

for fig in all, forward, backward, centered:
    drawing_tool.erase()
    fig.draw()
    drawing_tool.display()
    drawing_tool.savefig(fig.get_name())
raw_input()

