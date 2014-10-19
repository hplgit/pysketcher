import matplotlib.pyplot as mpl
import matplotlib.transforms as transforms

mpl.ion()  # for interactive drawing
fig = mpl.figure()

ax = fig.gca()
xmin, xmax, ymin, ymax = 0.0, 11.0, -2.5, 7.5
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_aspect('equal')



mpl.grid(True)

# line
x = [1.5, 1.5]
y = [0.0, 1.25]
[line] = ax.plot(x, y, 'b', linewidth=2, linestyle='solid')

# line
x = [1.5, 1.5]
y = [5.0, 2.395833333333333]
[line] = ax.plot(x, y, 'b', linewidth=2, linestyle='solid')

# rectangle
x = [1.0833333333333333,
 1.9166666666666665,
 1.9166666666666665,
 1.0833333333333333,
 1.0833333333333333]
y = [2.083333333333333,
 2.083333333333333,
 2.395833333333333,
 2.395833333333333,
 2.083333333333333]
[line] = ax.fill(x, y, 'white', edgecolor='b', linewidth=2, hatch='X')

# pot
x = [1.0, 1.0, 2.0, 2.0]
y = [3.75, 1.25, 1.25, 3.75]
[line] = ax.plot(x, y, 'b', linewidth=2, linestyle='solid')
ax.text(1.5, 5.5, 'Dashpot (default)',
        horizontalalignment='center', fontsize=14)

# line
x = [6.5, 6.5]
y = [0.0, 2.0]
[line] = ax.plot(x, y, 'b', linewidth=2, linestyle='solid')

# line
x = [6.5, 6.5]
y = [6.0, 4.5]
[line] = ax.plot(x, y, 'b', linewidth=2, linestyle='solid')

# rectangle
x = [6.083333333333333,
 6.916666666666666,
 6.916666666666666,
 6.083333333333333,
 6.083333333333333]
y = [4.1875, 4.1875, 4.5, 4.5, 4.1875]
[line] = ax.fill(x, y, 'white', edgecolor='b', linewidth=2, hatch='X')

# pot
x = [6.0, 6.0, 7.0, 7.0]
y = [4.5, 2.0, 2.0, 4.5]
[line] = ax.plot(x, y, 'b', linewidth=2, linestyle='solid')
ax.text(6.5, -1.56667, 'width',
        horizontalalignment='center', fontsize=14)

# line
mpl.arrow(x=6, y=-1.75, dx=1, dy=0,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
mpl.arrow(x=7, y=-1.75, dx=-1, dy=0,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
ax.annotate('start', xy=(6.5, 0), xycoords='data',
            textcoords='data', xytext=(5.75, -0.75),
            horizontalalignment='center',
            verticalalignment='top',
            fontsize=14,
            arrowprops=dict(arrowstyle='->',
                            facecolor='black',
                            linewidth=2,
                            shrinkA=5,
                            shrinkB=5))
ax.annotate('bar_length', xy=[ 5.5  1. ], xycoords='data',
            textcoords='data', xytext=(3.5, 1.5),
            horizontalalignment='left',
            verticalalignment='top',
            fontsize=14,
            arrowprops=dict(arrowstyle='->',
                            facecolor='black',
                            linewidth=2,
                            shrinkA=5,
                            shrinkB=5))

# line
mpl.arrow(x=5.5, y=2, dx=0, dy=-2,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
mpl.arrow(x=5.5, y=0, dx=0, dy=2,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
ax.annotate('total_length', xy=[ 8.5  3. ], xycoords='data',
            textcoords='data', xytext=(8.75, 5.0),
            horizontalalignment='left',
            verticalalignment='top',
            fontsize=14,
            arrowprops=dict(arrowstyle='->',
                            facecolor='black',
                            linewidth=2,
                            shrinkA=5,
                            shrinkB=5))

# line
mpl.arrow(x=8.5, y=6, dx=0, dy=-6,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
mpl.arrow(x=8.5, y=0, dx=0, dy=6,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
ax.annotate('dashpot_length', xy=[ 7.5   3.25], xycoords='data',
            textcoords='data', xytext=(7.0, -0.5),
            horizontalalignment='left',
            verticalalignment='top',
            fontsize=14,
            arrowprops=dict(arrowstyle='->',
                            facecolor='black',
                            linewidth=2,
                            shrinkA=5,
                            shrinkB=5))

# line
mpl.arrow(x=7.5, y=4.5, dx=0, dy=-2.5,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
mpl.arrow(x=7.5, y=2, dx=0, dy=2.5,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
ax.annotate('piston_pos', xy=[ 5.5      3.09375], xycoords='data',
            textcoords='data', xytext=(3.5, 3.6875),
            horizontalalignment='left',
            verticalalignment='top',
            fontsize=14,
            arrowprops=dict(arrowstyle='->',
                            facecolor='black',
                            linewidth=2,
                            shrinkA=5,
                            shrinkB=5))

# line
mpl.arrow(x=5.5, y=4.1875, dx=0, dy=-2.1875,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
mpl.arrow(x=5.5, y=2, dx=0, dy=2.1875,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
mpl.title("Dashpot")
mpl.draw()
mpl.savefig("tmp_Dashpot.png", dpi=None)
mpl.savefig("tmp_Dashpot.pdf")
