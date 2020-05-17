import os
import logging
from typing import List

import matplotlib.pyplot as mpl
import matplotlib.transforms as transforms
import numpy as np

from .point import Point


class MatplotlibDraw(object):
    """
    Simple interface for plotting. This interface makes use of
    Matplotlib for plotting.

    Some attributes that must be controlled directly (no set_* method
    since these attributes are changed quite seldom).

    ========================== ============================================
    Attribute                  Description
    ========================== ============================================
    allow_screen_graphics      False means that no plot is shown on
                               the screen. (Does not work yet.)
    arrow_head_width           Size of arrow head.
    ========================== ============================================
    """
    line_colors = {'red': 'r', 'green': 'g', 'blue': 'b', 'cyan': 'c',
                   'magenta': 'm', 'purple': 'p',
                   'yellow': 'y', 'black': 'k', 'white': 'w',
                   'brown': 'brown', '': ''}

    def __init__(self, xmin, xmax, ymin, ymax, axis=False, new_figure=True):
        self.instruction_file = None
        self.allow_screen_graphics = True  # does not work yet
        self._mpl = mpl
        self.set_coordinate_system(xmin, xmax, ymin, ymax, axis, new_figure)

    def ok(self):
        """
        Return True if set_coordinate_system is called and
        objects can be drawn.
        """

    def adjust_coordinate_system(self, minmax, occupation_percent=80):
        """
        Given a dict of xmin, xmax, ymin, ymax values, and a desired
        filling of the plotting area of `occupation_percent` percent,
        set new axis limits.
        """
        x_range = minmax['xmax'] - minmax['xmin']
        y_range = minmax['ymax'] - minmax['ymin']
        new_x_range = x_range * 100. / occupation_percent
        x_space = new_x_range - x_range
        new_y_range = y_range * 100. / occupation_percent
        y_space = new_y_range - y_range
        self.ax.set_xlim(minmax['xmin'] - x_space / 2., minmax['xmax'] + x_space / 2.)
        self.ax.set_ylim(minmax['ymin'] - y_space / 2., minmax['ymax'] + y_space / 2.)

    def set_coordinate_system(self, xmin, xmax, ymin, ymax, axis=False, new_figure=True):
        """
        Define the drawing area [xmin,xmax]x[ymin,ymax].
        axis: None or False means that axes with tickmarks
        are not drawn.
        instruction_file: name of file where all the instructions
        for the plotting program are stored (useful for debugging
        a figure or tailoring plots).
        """

        self.x_min, self.x_max, self.y_min, self.y_max = \
            float(xmin), float(xmax), float(ymin), float(ymax)
        self.x_range = self.x_max - self.x_min
        self.y_range = self.y_max - self.y_min
        self.axis = axis

        # Compute the right X11 geometry on the screen based on the
        # x-y ratio of axis ranges
        ratio = (self.y_max - self.y_min) / (self.x_max - self.x_min)
        self.x_size = 800  # pixel size
        self.y_size = self.x_size * ratio

        self._mpl.ion()  # important for interactive drawing and animation

        # Default properties
        self.set_linecolor('red')
        self.set_linewidth(2)
        self.set_linestyle('solid')
        self.set_filled_curves()  # no filling
        self.set_fontsize(14)
        self.arrow_head_width = 0.2 * self.x_range / 16
        self._make_axes(new_figure=new_figure)

    def _make_axes(self, new_figure=False):
        if new_figure:
            self.fig = self._mpl.figure()
        self.ax = self.fig.gca()
        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)
        self.ax.set_aspect('equal')  # extent of 1 unit is the same on the axes

        if not self.axis:
            self._mpl.axis('off')

    def inside(self, point: Point):
        tol = 1E-14
        return False if self.x_min - tol <= point.x <= self.x_max + tol or \
                        self.y_min - tol <= point.y <= self.y_max + tol else True

    def inside_plot_area(self, points: List[Point], verbose=True):
        """Check that all coordinates are within drawing_tool's area."""
        for point in points:
            if not self.inside(point):
                return False
        return True

    def set_linecolor(self, color):
        """
        Change the color of lines. Available colors are
        'black', 'white', 'red', 'blue', 'green', 'yellow',
        'magenta', 'cyan'.
        """
        self.line_color = MatplotlibDraw.line_colors[color]

    def set_linestyle(self, style):
        """Change line style: 'solid', 'dashed', 'dashdot', 'dotted'."""
        if not style in ('solid', 'dashed', 'dashdot', 'dotted'):
            raise ValueError('Illegal line style: %s' % style)
        self.line_style = style

    def set_linewidth(self, width):
        """Change the line width (int, starts at 1)."""
        self.line_width = width

    def set_filled_curves(self, color='', pattern=''):
        """
        Fill area inside curves with specified color and/or pattern.
        A common pattern is '/' (45 degree lines). Other patterns
        include '-', '+', 'x', '\\', '*', 'o', 'O', '.'.
        """
        if color is False:
            self.fill_color = ''
            self.fill_pattern = ''
        else:
            self.fill_color = color if len(color) == 1 else \
                MatplotlibDraw.line_colors[color]
            self.fill_pattern = pattern

    def set_fontsize(self, fontsize=18):
        """
        Method for setting a common fontsize for text, unless
        individually specified when calling ``text``.
        """
        self.fontsize = fontsize

    def set_grid(self, on=False):
        self._mpl.grid(on)

    def erase(self):
        """Erase the current figure."""
        self._mpl.delaxes()
        self._make_axes(new_figure=False)

    def plot_curve(self, points: List[Point],
                   line_style=None, line_width=None,
                   line_color=None, arrow=None,
                   fill_color=None, fill_pattern=None,
                   shadow=0):
        """Draw a curve with coordinates x and y (arrays)."""

        logging.info("Given %i points, line_style: %s, line_width: %s "
                     "line_color: %s, arrow: %s, fill_color: %s, fill_pattern: %s, shadow: %s",
                     len(points), line_style, line_width, line_color, arrow, fill_color, fill_pattern, shadow)

        x = [point.x for point in points]
        y = [point.y for point in points]

        print(x)
        print(y)

        if line_style is None:
            # use "global" linestyle
            line_style = self.line_style
        if line_color is None:
            line_color = self.line_color
        if line_width is None:
            line_width = self.line_width
        if fill_color is None:
            fill_color = self.fill_color
        if fill_pattern is None:
            fill_pattern = self.fill_pattern

        # We can plot fillcolor/fillpattern, arrow or line

        if fill_color or fill_pattern:
            if fill_pattern != '':
                fill_color = 'white'
            print('%d coords, fillcolor="%s" linecolor="%s" fillpattern="%s"' % (
                len(x), fill_color, line_color, fill_pattern))
            [line] = self.ax.fill(x, y, fill_color, edgecolor=line_color,
                                  linewidth=line_width, hatch=fill_pattern)
        else:
            # Plain line
            print('%d coords, fillcolor="%s" linecolor="%s" fillpattern="%s"' % (
                len(x), fill_color, line_color, fill_pattern))
            [line] = self.ax.plot(x, y, line_color, linewidth=line_width,
                                  linestyle=line_style)

        if arrow:
            # Note that a Matplotlib arrow is a line with the arrow tip
            if arrow not in ('->', '<-', '<->'):
                raise ValueError("arrow argument must be '->', '<-', or '<->', not %s" % repr(arrow))

            # Add arrow to first and/or last segment
            start = arrow == '<-' or arrow == '<->'
            end = arrow == '->' or arrow == '<->'
            if start:
                x_s, y_s = x[1], y[1]
                dx_s, dy_s = x[0] - x[1], y[0] - y[1]
                self._plot_arrow(x_s, y_s, dx_s, dy_s, '->',
                                 line_style, line_width, line_color)
            if end:
                x_e, y_e = x[-2], y[-2]
                dx_e, dy_e = x[-1] - x[-2], y[-1] - y[-2]
                self._plot_arrow(x_e, y_e, dx_e, dy_e, '->',
                                 line_style, line_width, line_color)
        if shadow:
            # http://matplotlib.sourceforge.net/users/transforms_tutorial.html#using-offset-transforms-to-create-a-shadow-effect
            # shift the object over 2 points, and down 2 points
            dx, dy = shadow / 72., -shadow / 72.
            offset = transforms.ScaledTranslation(
                dx, dy, self.fig.dpi_scale_trans)
            shadow_transform = self.ax.transData + offset
            # now plot the same data with our offset transform;
            # use the zorder to make sure we are below the line
            if line_width is None:
                line_width = 3
            self.ax.plot(x, y, linewidth=line_width, color='gray',
                         transform=shadow_transform,
                         zorder=0.5 * line.get_zorder())

    def display(self, title=None, show=True):
        """Display the figure."""
        if title is not None:
            self._mpl.title(title)
            if self.instruction_file:
                self.instruction_file.write('mpl.title("%s")\n' % title)

        if show:
            self._mpl.draw()

    def savefig(self, filename, dpi=None, crop=True):
        """Save figure in file. Set dpi=300 for really high resolution."""
        # If filename is without extension, generate all important formats
        ext = os.path.splitext(filename)[1]
        if not ext:
            # Create both PNG and PDF file
            self._mpl.savefig(filename + '.png', dpi=dpi)
            self._mpl.savefig(filename + '.pdf')
            if crop:
                # Crop the PNG file
                failure = os.system('convert -trim %s.png %s.png' %
                                    (filename, filename))
                if failure:
                    print('convert from ImageMagick is not installed - needed for cropping PNG files')
                failure = os.system('pdfcrop %s.pdf %s.pdf' %
                                    (filename, filename))
                if failure:
                    print('pdfcrop is not installed - needed for cropping PDF files')
        else:
            self._mpl.savefig(filename, dpi=dpi)
            if ext == '.png':
                if crop:
                    failure = os.system('convert -trim %s %s' % (filename, filename))
                    if failure:
                        print('convert from ImageMagick is not installed - needed for cropping PNG files')
            elif ext == '.pdf':
                if crop:
                    failure = os.system('pdfcrop %s %s' % (filename, filename))
                    if failure:
                        print('pdfcrop is not installed - needed for cropping PDF files')

    def text(self,
             text: str,
             position: Point,
             alignment='center',
             fontsize=0,
             arrow_tip: Point = None,
             bgcolor=None,
             fgcolor=None,
             fontfamily=None,
             direction: Point = Point(1, 0)):
        """
        Write `text` string at a position (centered, left, right - according
        to the `alignment` string). `position` is a point in the coordinate
        system.
        If ``arrow+tip != None``, an arrow is drawn from the text to a point
        (on a curve, for instance). The arrow_tip argument is then
        the (x,y) coordinates for the arrow tip.
        fontsize=0 indicates use of the default font as set by
        ``set_fontsize``.
        """
        if fontsize == 0:
            if hasattr(self, 'fontsize'):
                fontsize = self.fontsize
            else:
                raise AttributeError(
                    'No self.fontsize attribute to be used when text(...)\n'
                    'is called with fontsize=0. Call set_fontsize method.')

        kwargs = {}
        if fontfamily is not None:
            kwargs['family'] = fontfamily
        if bgcolor is not None:
            kwargs['backgroundcolor'] = bgcolor
        if fgcolor is not None:
            kwargs['color'] = fgcolor

        x = position.x
        y = position.y

        rotation_angle = direction.angle()

        if arrow_tip is None:
            self.ax.text(x, y, text, horizontalalignment=alignment,
                         fontsize=fontsize, **kwargs)
        else:
            self.ax.annotate(text, xy=(arrow_tip.x, arrow_tip.y), xycoords='data',
                             textcoords='data', xytext=(position.x, position.y),
                             horizontalalignment=alignment,
                             verticalalignment='top',
                             fontsize=fontsize,
                             arrowprops=dict(arrowstyle='->',
                                             facecolor='black',
                                             # linewidth=2,
                                             linewidth=1,
                                             shrinkA=5,
                                             shrinkB=5))

    # Drawing annotations with arrows:
    # http://matplotlib.sourceforge.net/users/annotations_intro.html
    # http://matplotlib.sourceforge.net/mpl_examples/pylab_examples/annotation_demo2.py
    # http://matplotlib.sourceforge.net/users/annotations_intro.html
    # http://matplotlib.sourceforge.net/users/annotations_guide.html#plotting-guide-annotation

    def _plot_arrow(self, x, y, dx, dy, style='->',
                    linestyle=None, linewidth=None, linecolor=None):
        """Draw arrow (dx,dy) at (x,y). `style` is '->', '<-' or '<->'."""
        if linestyle is None:
            # use "global" linestyle
            linestyle = self.line_style
        if linecolor is None:
            linecolor = self.line_color
        if linewidth is None:
            linewidth = self.line_width

        if style == '->' or style == '<->':
            self._mpl.arrow(x, y, dx, dy,
                            facecolor=linecolor,
                            edgecolor=linecolor,
                            linestyle=linestyle,
                            linewidth=linewidth,
                            head_width=self.arrow_head_width,
                            # head_width=0.1,
                            # width=1,  # width of arrow body in coordinate scale
                            length_includes_head=True,
                            shape='full')
        if style == '<-' or style == '<->':
            self._mpl.arrow(x + dx, y + dy, -dx, -dy,
                            facecolor=linecolor,
                            edgecolor=linecolor,
                            linewidth=linewidth,
                            head_width=0.1,
                            # width=1,
                            length_includes_head=True,
                            shape='full')

    def arrow2(self, x, y, dx, dy, style='->'):
        """Draw arrow (dx,dy) at (x,y). `style` is '->', '<-' or '<->'."""
        self.ax.annotate('', xy=(x + dx, y + dy), xytext=(x, y),
                         arrowprops=dict(arrowstyle=style,
                                         facecolor='black',
                                         linewidth=1,
                                         shrinkA=0,
                                         shrinkB=0))


def _test():
    d = MatplotlibDraw(0, 10, 0, 5, axis=True)
    d.set_linecolor('magenta')
    d.set_linewidth(6)
    # triangle
    x = np.array([1, 4, 1, 1]);
    y = np.array([1, 1, 4, 1])
    d.set_filled_curves('magenta')
    d.plot_curve(x, y)
    d.set_filled_curves(False)
    d.plot_curve(x + 4, y)
    d.text('some text1', position=(8, 4), arrow_tip=(6, 1), alignment='left',
           fontsize=18)
    pos = np.array((7, 4.5))  # numpy points work fine
    d.text('some text2', position=pos, arrow_tip=(6, 1), alignment='center',
           fontsize=12)
    d.set_linewidth(2)
    d.arrow(0.25, 0.25, 0.45, 0.45)
    d.arrow(0.25, 0.25, 0.25, 4, style='<->')
    d.arrow2(4.5, 0, 0, 3, style='<->')
    x = np.linspace(0, 9, 201)
    y = 4.5 + 0.45 * np.cos(0.5 * np.pi * x)
    d.plot_curve(x, y, arrow='end')
    d.display()
    input()


if __name__ == '__main__':
    _test()
