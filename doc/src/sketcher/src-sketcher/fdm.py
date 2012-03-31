from pysketcher import *

#test_test()
drawing_tool.set_coordinate_system(0, 7, 0, 8, axis=True)

f = SketchyFunc('$f(x)$')
x = 3
xb = 2
xf = 4
p = (x, f(x))
pf = (xf, f(xf))
pb = (xb, f(xb))
r = 0.1
c = Circle(p, r).set_linecolor('blue')
cf = Circle(pf, r).set_linecolor('blue')
cb = Circle(pb, r).set_linecolor('blue')
domain = [1, 5]
domain2 = [2, 5]
lf = Line(p, pf).new_interval(x=domain2).set_linestyle('dashed').set_linecolor('blue')
lb = Line(pb, p).new_interval(x=domain).set_linestyle('dashed').set_linecolor('blue')
lc = Line(pb, pf).new_interval(x=domain).set_linestyle('dashed').set_linecolor('blue')
h = 1E-3
le = Line((x+h, f(x+h)), (x-h, f(x-h))).new_interval(x=domain).set_linestyle('dotted').set_linecolor('black')

f.draw()
c.draw()
cb.draw()
cf.draw()
lf.draw()
lb.draw()
lc.draw()
le.draw()
drawing_tool.display()
raw_input()

