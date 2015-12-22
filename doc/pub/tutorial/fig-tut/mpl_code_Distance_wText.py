import matplotlib.pyplot as mpl
import matplotlib.transforms as transforms

mpl.ion()  # for interactive drawing
fig = mpl.figure()

ax = fig.gca()
xmin, xmax, ymin, ymax = 0.0, 10.0, 0.0, 6.0
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_aspect('equal')


ax.text(1.13014, 3.14588, '$ 2\\pi R^2 $',
        horizontalalignment='left', fontsize=14)

# line
mpl.arrow(x=2, y=4.5, dx=-2, dy=-2.5,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
mpl.arrow(x=0, y=2, dx=2, dy=2.5,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
ax.text(6, 5.16667, '$ 2\\pi R^2 $',
        horizontalalignment='center', fontsize=14)

# line
mpl.arrow(x=4, y=5, dx=4, dy=0,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
mpl.arrow(x=8, y=5, dx=-4, dy=0,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
ax.text(1.07454, 5.14907, '$ 2\\pi R^2 $',
        horizontalalignment='center', fontsize=14)

# line
mpl.arrow(x=0, y=5.5, dx=2, dy=-1,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
mpl.arrow(x=2, y=4.5, dx=-2, dy=1,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
ax.text(1.11785, 1.11785, '$ 2\\pi R^2 $',
        horizontalalignment='left', fontsize=14)

# line
mpl.arrow(x=0, y=2, dx=2, dy=-2,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
mpl.arrow(x=2, y=0, dx=-2, dy=2,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
ax.text(8.8882, 1.27639, '$ 2\\pi R^2 $',
        horizontalalignment='right', fontsize=14)

# line
mpl.arrow(x=8, y=2, dx=2, dy=-1,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
mpl.arrow(x=10, y=1, dx=-2, dy=1,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
ax.text(8.92546, 3.35093, '$ 2\\pi R^2 $',
        horizontalalignment='center', fontsize=14)

# line
mpl.arrow(x=8, y=4, dx=2, dy=-1,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
mpl.arrow(x=10, y=3, dx=-2, dy=1,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
ax.text(4.16667, 4.5, '$ 2\\pi R^2 $',
        horizontalalignment='left', fontsize=14)

# line
mpl.arrow(x=4, y=5, dx=0, dy=-1,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
mpl.arrow(x=4, y=4, dx=0, dy=1,
          facecolor='k', edgecolor='k',
          linestyle='solid',
          linewidth=1, head_width=0.1,
          length_includes_head=True,
          shape='full')
ax.annotate('text_spacing=-1./40, alignment="right"', xy=(9, 1.2), xycoords='data',
            textcoords='data', xytext=(4, 0.5),
            horizontalalignment='left',
            verticalalignment='top',
            fontsize=10,
            arrowprops=dict(arrowstyle='->',
                            facecolor='black',
                            linewidth=2,
                            shrinkA=5,
                            shrinkB=5))
ax.annotate('text_spacing=-1./60', xy=(9, 3.2), xycoords='data',
            textcoords='data', xytext=(4, 3.5),
            horizontalalignment='left',
            verticalalignment='top',
            fontsize=10,
            arrowprops=dict(arrowstyle='->',
                            facecolor='black',
                            linewidth=2,
                            shrinkA=5,
                            shrinkB=5))
mpl.title("Distance_wText and text positioning")
mpl.draw()
mpl.savefig("tmp_Distance_wText.png", dpi=None)
mpl.savefig("tmp_Distance_wText.pdf")
