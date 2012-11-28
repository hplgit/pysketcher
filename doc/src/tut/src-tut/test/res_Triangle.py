import matplotlib.pyplot as mpl

mpl.ion()  # for interactive drawing
fig = mpl.figure()

ax = fig.gca()
xmin, xmax, ymin, ymax = 0.0, 8.0, -1.5, 3.6
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_aspect('equal')



mpl.grid(True)
x = [2.0, 6.0, 3.2, 2.0]
y = [0.0, 2.0, 3.0, 0.0]
ax.plot(x, y, 'b', linewidth=2, linestyle='solid')
ax.text(6, 2, 'p2',
        horizontalalignment='center', fontsize=14)
ax.text(3.2, 3, 'p3',
        horizontalalignment='center', fontsize=14)
ax.text(2, 0, 'p1',
        horizontalalignment='center', fontsize=14)
mpl.title("Triangle")
mpl.draw()
mpl.savefig("tmp_Triangle.png")
