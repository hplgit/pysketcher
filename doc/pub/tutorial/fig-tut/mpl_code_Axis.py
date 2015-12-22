import matplotlib.pyplot as mpl
import matplotlib.transforms as transforms

mpl.ion()  # for interactive drawing
fig = mpl.figure()

ax = fig.gca()
xmin, xmax, ymin, ymax = 0.0, 15.0, -7.0, 8.0
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_aspect('equal')



# line
x = [12.240192378864668, 12.5]
y = [2.150000000000001, 2.0000000000000004]
[line] = ax.plot(x, y, 'r', linewidth=2, linestyle='solid')

# line
x = [7.5, 12.5]
y = [2.0, 2.0000000000000004]
[line] = ax.plot(x, y, 'r', linewidth=2, linestyle='solid')

# line
x = [12.240192378864668, 12.5]
y = [1.8499999999999999, 2.0000000000000004]
[line] = ax.plot(x, y, 'r', linewidth=2, linestyle='solid')
ax.text(12.8333, 2, 'x',
        horizontalalignment='center', fontsize=14)

# line
x = [7.35, 7.5]
y = [6.740192378864668, 7.0]
[line] = ax.plot(x, y, 'r', linewidth=2, linestyle='solid')

# line
x = [7.5, 7.5]
y = [2.0, 7.0]
[line] = ax.plot(x, y, 'r', linewidth=2, linestyle='solid')

# line
x = [7.65, 7.5]
y = [6.740192378864668, 7.0]
[line] = ax.plot(x, y, 'r', linewidth=2, linestyle='solid')
ax.text(7.5, 7.33333, 'y',
        horizontalalignment='center', fontsize=14)
mpl.draw()

# line
x = [11.034779889691228, 11.33022221559489]
y = [5.161843595132618, 5.213938048432697]
[line] = ax.plot(x, y, 'r', linewidth=2, linestyle='dashed')

# line
x = [7.5, 11.33022221559489]
y = [2.0, 5.213938048432697]
[line] = ax.plot(x, y, 'r', linewidth=2, linestyle='dashed')

# line
x = [11.22761617259719, 11.33022221559489]
y = [4.932030262196924, 5.213938048432697]
[line] = ax.plot(x, y, 'r', linewidth=2, linestyle='dashed')
ax.text(11.5856, 5.4282, 'x',
        horizontalalignment='center', fontsize=14)

# line
x = [4.338156404867384, 4.286061951567303]
y = [5.534779889691228, 5.83022221559489]
[line] = ax.plot(x, y, 'r', linewidth=2, linestyle='dashed')

# line
x = [7.5, 4.286061951567303]
y = [2.0, 5.83022221559489]
[line] = ax.plot(x, y, 'r', linewidth=2, linestyle='dashed')

# line
x = [4.567969737803077, 4.286061951567303]
y = [5.727616172597189, 5.83022221559489]
[line] = ax.plot(x, y, 'r', linewidth=2, linestyle='dashed')
ax.text(4.0718, 6.08557, 'y',
        horizontalalignment='center', fontsize=14)
mpl.draw()

# line
x = [6.824595394571309, 6.631759111665348]
y = [-2.694225432125347, -2.92403876506104]
[line] = ax.plot(x, y, 'r', linewidth=2, linestyle='dotted')

# line
x = [7.5, 6.631759111665348]
y = [2.0, -2.92403876506104]
[line] = ax.plot(x, y, 'r', linewidth=2, linestyle='dotted')

# line
x = [6.5291530686676476, 6.631759111665348]
y = [-2.642130978825267, -2.92403876506104]
[line] = ax.plot(x, y, 'r', linewidth=2, linestyle='dotted')
ax.text(6.57388, -3.25231, 'x',
        horizontalalignment='center', fontsize=14)

# line
x = [12.194225432125346, 12.424038765061042]
y = [1.3245953945713098, 1.1317591116653478]
[line] = ax.plot(x, y, 'r', linewidth=2, linestyle='dotted')

# line
x = [7.5, 12.424038765061042]
y = [2.0, 1.1317591116653478]
[line] = ax.plot(x, y, 'r', linewidth=2, linestyle='dotted')

# line
x = [12.142130978825266, 12.424038765061042]
y = [1.029153068667647, 1.1317591116653478]
[line] = ax.plot(x, y, 'r', linewidth=2, linestyle='dotted')
ax.text(12.7523, 1.07388, 'y',
        horizontalalignment='center', fontsize=14)
mpl.draw()
mpl.title("Axis")
mpl.draw()
mpl.savefig("tmp_Axis.png", dpi=None)
mpl.savefig("tmp_Axis.pdf")
