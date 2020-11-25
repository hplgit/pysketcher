from typing import List

import matplotlib.pyplot as plt

import pysketcher as ps
from pysketcher._style import Style
from pysketcher.backend.matplotlib._matplotlib_adapter import MatplotlibAdapter
from pysketcher.backend.matplotlib._matplotlib_style import MatplotlibStyle


class MatplotlibCurve(MatplotlibAdapter):
    types: List[type] = [ps.Curve]

    def plot(self, curve: ps.Curve, axes: plt.Axes) -> None:
        """Draw a curve with coordinates x and y (arrays)."""
        mpl_style = MatplotlibStyle(curve.style)

        x = curve.xs
        y = curve.ys

        [line] = axes.plot(
            x,
            y,
            mpl_style.line_color,
            linewidth=mpl_style.line_width,
            linestyle=mpl_style.line_style,
        )
        if mpl_style.fill_color or mpl_style.fill_pattern:
            [line] = plt.fill(
                x,
                y,
                mpl_style.fill_color,
                edgecolor=mpl_style.line_color,
                linewidth=mpl_style.line_width,
                hatch=mpl_style.fill_pattern,
            )

        if curve.style.arrow is not None:
            if curve.style.arrow in [Style.ArrowStyle.START, Style.ArrowStyle.DOUBLE]:
                x_s, y_s = x[0], y[0]
                dx_s, dy_s = x[1] - x[0], y[1] - y[0]
                self._plot_arrow(x_s, y_s, dx_s, dy_s, curve.style, axes)
            if curve.style.arrow in [Style.ArrowStyle.END, Style.ArrowStyle.DOUBLE]:
                x_e, y_e = x[-1], y[-1]
                dx_e, dy_e = x[-2] - x[-1], y[-2] - y[-1]
                self._plot_arrow(x_e, y_e, dx_e, dy_e, curve.style, axes)

        # if mpl_style.shadow:
        # http://matplotlib.sourceforge.net/users/transforms_tutorial.html
        # #using-offset-transforms-to-create-a-shadow-effect
        # shift the object over 2 points, and down 2 points
        #     dx, dy = mpl_style.shadow / 72.0, -mpl_style.shadow / 72.0
        #     offset = transforms.ScaledTranslation(dx, dy, fig.dpi_scale_trans)
        #     shadow_transform = axes.transData + offset
        #     # now plot the same data with our offset transform;
        #     # use the zorder to make sure we are below the line
        #     axes.plot(
        #         x,
        #         y,
        #         linewidth=mpl_style.line_width,
        #         color="gray",
        #         transform=shadow_transform,
        #         zorder=0.5 * line.get_zorder(),
        #     )

    def _plot_arrow(self, x, y, dx, dy, style: Style, axes: plt.Axes):
        """Draw arrow (dx,dy) at (x,y). `style` is '->', '<-' or '<->'."""
        mpl_style = MatplotlibStyle(style)
        if style.arrow in [Style.ArrowStyle.START, Style.ArrowStyle.DOUBLE]:
            axes.arrow(
                x,
                y,
                dx,
                dy,
                facecolor=mpl_style.line_color,
                edgecolor=mpl_style.line_color,
                linestyle=mpl_style.line_style,
                linewidth=mpl_style.line_width,
                # head_width=self.arrow_head_width,
                # head_width=0.1,
                # width=1,  # width of arrow body in coordinate scale
                length_includes_head=True,
                shape="full",
            )
        if style.arrow in [Style.ArrowStyle.END, Style.ArrowStyle.DOUBLE]:
            axes.arrow(
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
