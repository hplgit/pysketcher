import matplotlib.pyplot as mpl

mpl.ion()  # for interactive drawing
fig = mpl.figure()

ax = fig.gca()
xmin, xmax, ymin, ymax = 0.0, 8.0, -1.5, 6.0
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_aspect('equal')



mpl.grid(True)
x = [2.0, 6.0, 6.0, 2.0, 2.0]
y = [0.0, 0.0, 3.0, 3.0, 0.0]
ax.plot(x, y, 'b', linewidth=2, linestyle='solid')
ax.text(4, -0.466667, 'width',
        horizontalalignment='center', fontsize=14)
x = [6.0, 2.0]
y = [-0.6, -0.6]
ax.plot(x, y, 'k', linewidth=1, linestyle='solid')
mpl.arrow(x=2, y=-0.6, dx=4, dy=0,
          facecolor='k', edgecolor='k',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
mpl.arrow(x=6, y=-0.6, dx=-4, dy=0,
          facecolor='k', edgecolor='k',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
ax.annotate('lower_left_corner', xy=[ 2.  0.], xycoords='data',
            textcoords='data', xytext=[ 1.2 -0.6],
            horizontalalignment='center',
            verticalalignment='top',
            fontsize=14,
            arrowprops=dict(arrowstyle='->',
                            facecolor='black',
                            linewidth=2,
                            shrinkA=5,
                            shrinkB=5))
ax.text(6.93333, 1.5, 'height',
        horizontalalignment='left', fontsize=14)
x = [6.8, 6.8]
y = [0.0, 3.0]
ax.plot(x, y, 'k', linewidth=1, linestyle='solid')
mpl.arrow(x=6.8, y=3, dx=0, dy=-3,
          facecolor='k', edgecolor='k',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
mpl.arrow(x=6.8, y=0, dx=0, dy=3,
          facecolor='k', edgecolor='k',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
mpl.title("Rectangle")
mpl.draw()
mpl.savefig("tmp_Rectangle.png")
