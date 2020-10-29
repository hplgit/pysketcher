import logging
import os
from typing import Callable, List

import matplotlib.pyplot as mpl
import matplotlib.transforms as transforms
import numpy as np

from .drawing_tool import DrawingTool
from .point import Point
from .style import Style, TextStyle


class MatplotlibDraw(DrawingTool):
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

    def __init__(self, xmin, xmax, ymin, ymax, axis=False, new_figure=True):
        self.instruction_file = None
        self.allow_screen_graphics = True  # does not work yet
        self._mpl = mpl
        self._set_coordinate_system(xmin, xmax, ymin, ymax, axis, new_figure)

    def ok(self):
        """
        Return True if set_coordinate_system is called and
        objects can be drawn.
        """

    def _set_coordinate_system(
        self, xmin, xmax, ymin, ymax, axis=False, new_figure=True
    ):
        """
        Define the drawing area [xmin,xmax]x[ymin,ymax].
        axis: None or False means that axes with tickmarks
        are not drawn.
        instruction_file: name of file where all the instructions
        for the plotting program are stored (useful for debugging
        a figure or tailoring plots).
        """

        self.x_min, self.x_max, self.y_min, self.y_max = (
            float(xmin),
            float(xmax),
            float(ymin),
            float(ymax),
        )
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
        self.arrow_head_width = 0.2 * self.x_range / 16
        self._make_axes(new_figure=new_figure)

    def _make_axes(self, new_figure=False):
        if new_figure:
            self.fig = self._mpl.figure()
        self.ax = self.fig.gca()
        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)
        self.ax.set_aspect("equal")  # extent of 1 unit is the same on the axes

        if not self.axis:
            self._mpl.axis("off")

    def inside(self, point: Point):
        tol = 1e-14
        return (
            False
            if self.x_min - tol <= point.x <= self.x_max + tol
            or self.y_min - tol <= point.y <= self.y_max + tol
            else True
        )

    def inside_plot_area(self, points: List[Point], verbose=True):
        """Check that all coordinates are within drawing_tool's area."""
        for point in points:
            if not self.inside(point):
                return False
        return True

    def set_grid(self, on=False):
        self._mpl.grid(on)

    def erase(self):
        """Erase the current figure."""
        self._mpl.delaxes()
        self._make_axes(new_figure=False)

    def plot_curve(self, points: List[Point], style: Style):
        """Draw a curve with coordinates x and y (arrays)."""
        mpl_style = MatplotlibStyle(style)
        logging.info("Given %i points, style: %s" % (len(points), mpl_style))

        x = [point.x for point in points]
        y = [point.y for point in points]

        logging.info("plot: %d coords, %s" % (len(x), mpl_style))
        [line] = self.ax.plot(
            x,
            y,
            mpl_style.line_color,
            linewidth=mpl_style.line_width,
            linestyle=mpl_style.line_style,
        )
        if mpl_style.fill_color or mpl_style.fill_pattern:
            logging.info("fill: %d coords, %s" % (len(x), mpl_style))
            [line] = self.ax.fill(
                x,
                y,
                mpl_style.fill_color,
                edgecolor=mpl_style.line_color,
                linewidth=mpl_style.line_width,
                hatch=mpl_style.fill_pattern,
            )

        if style.arrow is not None:
            if style.arrow.value.start:
                x_s, y_s = x[1], y[1]
                dx_s, dy_s = x[0] - x[1], y[0] - y[1]
                self._plot_arrow(x_s, y_s, dx_s, dy_s, style)
            if style.arrow.value.end:
                x_e, y_e = x[-2], y[-2]
                dx_e, dy_e = x[-1] - x[-2], y[-1] - y[-2]
                self._plot_arrow(x_e, y_e, dx_e, dy_e, style)

        if mpl_style.shadow:
            # http://matplotlib.sourceforge.net/users/transforms_tutorial.html#using-offset-transforms-to-create-a-shadow-effect
            # shift the object over 2 points, and down 2 points
            dx, dy = mpl_style.shadow / 72.0, -mpl_style.shadow / 72.0
            offset = transforms.ScaledTranslation(dx, dy, self.fig.dpi_scale_trans)
            shadow_transform = self.ax.transData + offset
            # now plot the same data with our offset transform;
            # use the zorder to make sure we are below the line
            self.ax.plot(
                x,
                y,
                linewidth=mpl_style.line_width,
                color="gray",
                transform=shadow_transform,
                zorder=0.5 * line.get_zorder(),
            )

    def display(self, title=None, show=True):
        """Display the figure."""
        if title is not None:
            self._mpl.title(title)

        if show:
            self._mpl.draw()

    def savefig(self, filename, dpi=None, crop=True):
        """Save figure in file. Set dpi=300 for really high resolution."""
        # If filename is without extension, generate all important formats
        ext = os.path.splitext(filename)[1]
        if not ext:
            # Create both PNG and PDF file
            self._mpl.savefig(filename + ".png", dpi=dpi)
            self._mpl.savefig(filename + ".pdf")
            if crop:
                # Crop the PNG file
                failure = os.system(
                    "convert -trim %s.png %s.png" % (filename, filename)
                )
                if failure:
                    print(
                        "convert from ImageMagick is not installed - needed for cropping PNG files"
                    )
                failure = os.system("pdfcrop %s.pdf %s.pdf" % (filename, filename))
                if failure:
                    print("pdfcrop is not installed - needed for cropping PDF files")
        else:
            self._mpl.savefig(filename, dpi=dpi)
            if ext == ".png":
                if crop:
                    failure = os.system("convert -trim %s %s" % (filename, filename))
                    if failure:
                        print(
                            "convert from ImageMagick is not installed - needed for cropping PNG files"
                        )
            elif ext == ".pdf":
                if crop:
                    failure = os.system("pdfcrop %s %s" % (filename, filename))
                    if failure:
                        print(
                            "pdfcrop is not installed - needed for cropping PDF files"
                        )

    def text(
        self,
        text: str,
        position: Point,
        direction: Point = Point(1, 0),
        style: TextStyle = TextStyle(),
    ):
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
        mpl_style = MatplotlibTextStyle(style)
        kwargs = {}
        if mpl_style.font_family is not None:
            kwargs["family"] = mpl_style.font_family
        if mpl_style.fill_color is not None:
            kwargs["backgroundcolor"] = mpl_style.fill_color
        if mpl_style.line_color is not None:
            kwargs["color"] = mpl_style.line_color

        rotation_angle = direction.angle()
        if rotation_angle != 0.0:
            kwargs["rotation"] = rotation_angle
        logging.info("kwargs: %s", kwargs)

        self.ax.text(
            position.x,
            position.y,
            text,
            horizontalalignment=mpl_style.alignment,
            fontsize=mpl_style.font_size,
            **kwargs
        )

    def _plot_arrow(self, x, y, dx, dy, style: Style):
        """Draw arrow (dx,dy) at (x,y). `style` is '->', '<-' or '<->'."""
        mpl_style = MatplotlibStyle(style)
        if style.arrow.value.end:
            self._mpl.arrow(
                x,
                y,
                dx,
                dy,
                facecolor=mpl_style.line_color,
                edgecolor=mpl_style.line_color,
                linestyle=mpl_style.line_style,
                linewidth=mpl_style.line_width,
                head_width=self.arrow_head_width,
                # head_width=0.1,
                # width=1,  # width of arrow body in coordinate scale
                length_includes_head=True,
                shape="full",
            )
        if style.arrow.value.start:
            self._mpl.arrow(
                x + dx,
                y + dy,
                -dx,
                -dy,
                facecolor=mpl_style.line_color,
                edgecolor=mpl_style.line_color,
                linewidth=mpl_style.line_width,
                head_width=0.1,
                # width=1,
                length_includes_head=True,
                shape="full",
            )

    def arrow2(self, x, y, dx, dy, style="->"):
        """Draw arrow (dx,dy) at (x,y). `style` is '->', '<-' or '<->'."""
        self.ax.annotate(
            "",
            xy=(x + dx, y + dy),
            xytext=(x, y),
            arrowprops=dict(
                arrowstyle=style, facecolor="black", linewidth=1, shrinkA=0, shrinkB=0
            ),
        )


class MatplotlibStyle:
    _style: Style
    LINE_STYLE_MAP = {
        Style.LineStyle.SOLID: "-",
        Style.LineStyle.DOTTED: ":",
        Style.LineStyle.DASHED: "--",
        Style.LineStyle.DASH_DOT: "-.",
    }
    FILL_PATTERN_MAP = {
        Style.FillPattern.CIRCLE: "O",
        Style.FillPattern.CROSS: "x",
        Style.FillPattern.DOT: ".",
        Style.FillPattern.HORIZONTAL: "-",
        Style.FillPattern.SQUARE: "+",
        Style.FillPattern.STAR: "*",
        Style.FillPattern.SMALL_CIRCLE: "o",
        Style.FillPattern.VERTICAL: "|",
        Style.FillPattern.UP_LEFT_TO_RIGHT: "//",
        Style.FillPattern.UP_RIGHT_TO_LEFT: "\\\\",
    }
    COLOR_MAP = {
        Style.Color.GREY: "grey",
        Style.Color.BLACK: "black",
        Style.Color.BLUE: "blue",
        Style.Color.BROWN: "brown",
        Style.Color.CYAN: "cyan",
        Style.Color.GREEN: "green",
        Style.Color.MAGENTA: "magenta",
        Style.Color.ORANGE: "orange",
        Style.Color.PURPLE: "purple",
        Style.Color.RED: "red",
        Style.Color.YELLOW: "yellow",
        Style.Color.WHITE: "white",
    }
    ARROW_MAP = {
        Style.ArrowStyle.DOUBLE: "<->",
        Style.ArrowStyle.START: "<-",
        Style.ArrowStyle.END: "->",
    }

    def __init__(self, style: Style):
        self._style = style

    @property
    def line_width(self) -> float:
        return self._style.line_width

    @property
    def line_style(self) -> str:
        return self.LINE_STYLE_MAP.get(self._style.line_style)

    @property
    def line_color(self):
        return self.COLOR_MAP.get(self._style.line_color)

    @property
    def fill_color(self):
        return self.COLOR_MAP.get(self._style.fill_color)

    @property
    def fill_pattern(self):
        return self.FILL_PATTERN_MAP.get(self._style.fill_pattern)

    @property
    def arrow(self):
        return self.ARROW_MAP.get(self._style.arrow)

    @property
    def shadow(self):
        return self._style.shadow

    def __str__(self):
        return (
            "line_style: %s, line_width: %s, line_color: %s,"
            " fill_pattern: %s, fill_color: %s, arrow: %s shadow: %s"
            % (
                self.line_style,
                self.line_width,
                self.line_color,
                self.fill_pattern,
                self.fill_color,
                self.arrow,
                self.shadow,
            )
        )


class MatplotlibTextStyle(MatplotlibStyle):
    FONT_SIZE_MAP = {TextStyle.FontSize.MEDIUM: "medium"}

    FONT_FAMILY_MAP = {
        TextStyle.FontFamily.SERIF: "serif",
        TextStyle.FontFamily.SANS: "sans-serif",
        TextStyle.FontFamily.MONO: "monospace",
    }

    ALIGNMENT_MAP = {
        TextStyle.Alignment.LEFT: "left",
        TextStyle.Alignment.RIGHT: "right",
        TextStyle.Alignment.CENTER: "center",
    }

    _style: TextStyle

    def __init__(self, text_style: TextStyle):
        super().__init__(text_style)

    @property
    def font_size(self) -> str:
        return self.FONT_SIZE_MAP.get(self._style.font_size)

    @property
    def font_family(self) -> str:
        return self.FONT_FAMILY_MAP.get(self._style.font_family)

    @property
    def alignment(self) -> str:
        return self.ALIGNMENT_MAP.get(self._style.alignment)


def _test():
    d = MatplotlibDraw(0, 10, 0, 5, axis=True)
    d.set_linecolor("magenta")
    d.set_linewidth(6)
    # triangle
    x = np.array([1, 4, 1, 1])
    y = np.array([1, 1, 4, 1])
    d.set_filled_curves("magenta")
    d.plot_curve(x, y)
    d.set_filled_curves(False)
    d.plot_curve(x + 4, y)
    d.text(
        "some text1", position=(8, 4), arrow_tip=(6, 1), alignment="left", fontsize=18
    )
    pos = np.array((7, 4.5))  # numpy points work fine
    d.text(
        "some text2", position=pos, arrow_tip=(6, 1), alignment="center", fontsize=12
    )
    d.set_linewidth(2)
    d.arrow(0.25, 0.25, 0.45, 0.45)
    d.arrow(0.25, 0.25, 0.25, 4, style="<->")
    d.arrow2(4.5, 0, 0, 3, style="<->")
    x = np.linspace(0, 9, 201)
    y = 4.5 + 0.45 * np.cos(0.5 * np.pi * x)
    d.plot_curve(x, y, arrow="end")
    d.display()
    input()


if __name__ == "__main__":
    _test()
