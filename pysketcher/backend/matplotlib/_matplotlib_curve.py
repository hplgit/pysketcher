from copy import copy
from typing import List

import matplotlib.pyplot as plt
import numpy as np

import pysketcher as ps
from pysketcher._style import Style
from pysketcher.backend.matplotlib._matplotlib_adapter import MatplotlibAdapter
from pysketcher.backend.matplotlib._matplotlib_style import MatplotlibStyle


class MatplotlibCurve(MatplotlibAdapter):
    types: List[type] = [ps.Curve]

    def plot(self, curve: ps.Curve, axes: plt.Axes) -> None:
        """Draw a curve with coordinates x and y (arrays)."""
        mpl_style = MatplotlibStyle(curve.style)

        xs = curve.xs
        ys = curve.ys

        if len(xs) == 2 and curve.style.arrow == Style.ArrowStyle.DOUBLE:
            # For multi-segment curves we can just make the first segment an
            # arrow if the style is START or DOUBLE and the last segment an
            # arrow if the style is END or DOUBLE. If there is only one segment
            # and the style is DOUBLE this won't work, so we split into two segments
            xs = np.linspace(xs[0], xs[1], 3)
            ys = np.linspace(ys[0], ys[1], 3)

        if curve.style.arrow is not None:
            if curve.style.arrow in [Style.ArrowStyle.START, Style.ArrowStyle.DOUBLE]:
                x_s, y_s = xs[0], ys[0]
                dx_s, dy_s = xs[1] - xs[0], ys[1] - ys[0]
                start_style = copy(curve.style)
                start_style.arrow = Style.ArrowStyle.END
                self._plot_arrow(x_s, y_s, dx_s, dy_s, start_style, axes)
                xs = xs[1:]
                ys = ys[1:]
            if curve.style.arrow in [Style.ArrowStyle.END, Style.ArrowStyle.DOUBLE]:
                x_e, y_e = xs[-2], ys[-2]
                dx_e, dy_e = xs[-1] - xs[-2], ys[-1] - ys[-2]
                end_style = copy(curve.style)
                end_style.arrow = Style.ArrowStyle.START
                self._plot_arrow(x_e, y_e, dx_e, dy_e, end_style, axes)
                xs = xs[:-1]
                ys = ys[:-1]

        if len(xs) >= 2:
            [line] = axes.plot(
                xs,
                ys,
                mpl_style.line_color,
                linewidth=mpl_style.line_width,
                linestyle=mpl_style.line_style,
            )
            if mpl_style.fill_color or mpl_style.fill_pattern:
                [line] = plt.fill(
                    xs,
                    ys,
                    mpl_style.fill_color,
                    edgecolor=mpl_style.line_color,
                    linewidth=mpl_style.line_width,
                    hatch=mpl_style.fill_pattern,
                )

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
        if style.arrow == Style.ArrowStyle.DOUBLE:
            raise ValueError("Only a single ended arrow is supported by this method.")
        mpl_style = MatplotlibStyle(style)
        if style.arrow == Style.ArrowStyle.END:
            x = x + dx
            y = y + dy
            dx = -dx
            dy = -dy
        axes.arrow(
            x,
            y,
            dx,
            dy,
            facecolor=mpl_style.line_color,
            edgecolor=mpl_style.line_color,
            linestyle=mpl_style.line_style,
            linewidth=mpl_style.line_width,
            head_width=0.05,
            # head_width=self.arrow_head_width,
            # width=1,  # width of arrow body in coordinate scale
            length_includes_head=True,
            shape="full",
        )
