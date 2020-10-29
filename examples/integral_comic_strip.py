"""Comic strip for illustrating numerical integration."""

from pysketcher import *

xkcd = True  # True: XKCD copic strip, False: ordinary Matplotlib figure


def f(x):
    return 3 * np.exp(-(x ** 4))


xmin = -2
drawing_tool._set_coordinate_system(
    xmin=xmin, xmax=4, ymin=0, ymax=4, axis=True, xkcd=xkcd
)
drawing_tool.set_linecolor("blue")

import numpy as np

x = np.linspace(xmin, 3, 201)
y = f(x)
curve = Curve(x)

x2 = np.linspace(xmin, 0.2, 201)
y2 = f(x2)
x2 = x2.tolist()
y2 = y2.tolist()
x2.append(x2[-1])
y2.append(0)
x2.append(xmin)
y2.append(0)
# x2 = np.array(x2)
# y2 = np.array(y2)
filled = Curve(x2).set_filled_curves(pattern="/")

text1 = ArrowWithText(
    "The integral $\int_{-\infty}^{0.2} 3e^{-x^4}dx$\nis impossible to calculate\nby hand but so easy with\na program!",
    (1.5, 3.5),
    (-0.2, 1),
    alignment="left",
)

fig = Composition(dict(curve=curve, integral=filled, comment=text1))
fig.draw()
drawing_tool.display()
drawing_tool.savefig("tmp1")

# input()

# Draw piecewise curve for midpoint rule
def piecewise_curve_for_midpoint_rule(N):
    dx = (0.2 - xmin) / float(N)
    x3_double = []
    y3_double = []
    y_prev = 0
    for i in range(N):
        x = xmin + i * dx
        x3_double.append(x)
        y3_double.append(y_prev)
        x3_double.append(x)
        y_next = 0.5 * (f(x) + f(xmin + (i + 1) * dx))
        y3_double.append(y_next)
        y_prev = y_next
    x = xmin + (i + 1) * dx
    x3_double.append(x)
    y3_double.append(y_prev)
    x3_double.append(x)
    y3_double.append(0)
    # Back to start
    x3_double.append(xmin)
    y3_double.append(0)
    midpoint_curve = (
        Curve(x3_double).set_filled_curves(pattern="/").set_linecolor("red")
    )
    return midpoint_curve


text2 = ArrowWithText(
    "We just draw some rectangles\nto approximate the area\nunder the curve and sum up\nthe rectangular areas!",
    (1.2, 3.5),
    (-0.2, 1),
    alignment="left",
)

drawing_tool.erase()
fig = Composition(
    dict(curve=curve, integral=piecewise_curve_for_midpoint_rule(N=4), comment=text2)
)
fig.draw()
drawing_tool.display()
drawing_tool.savefig("tmp2")

text3 = ArrowWithText(
    "Just add more rectangles\ngo get the integral\nmore accurate!",
    (1.5, 3.5),
    (-0.2, 1),
    alignment="left",
)

drawing_tool.erase()
fig = Composition(
    dict(curve=curve, integral=piecewise_curve_for_midpoint_rule(N=10), comment=text3)
)
fig.draw()
drawing_tool.display()
drawing_tool.savefig("tmp3")

import os

comic = "comic" if xkcd else "non_comic"
os.system("doconce combine_images pdf -3 tmp1 tmp2 tmp3 integral_%s_strip" % comic)
os.system("doconce combine_images png -3 tmp1 tmp2 tmp3 integral_%s_strip" % comic)

input()
