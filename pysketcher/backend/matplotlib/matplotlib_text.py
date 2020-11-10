import matplotlib.pyplot as plt

from pysketcher.backend.matplotlib.matplotlib_adapter import MatplotlibAdapter
from pysketcher.backend.matplotlib.matplotlib_style import MatplotlibTextStyle
from pysketcher.text import Text


class MatplotlibText(MatplotlibAdapter):
    def plot(self, text: Text, axes: plt.Axes):
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
        mpl_style = MatplotlibTextStyle(text.style)
        kwargs = {}
        if mpl_style.font_family is not None:
            kwargs["family"] = mpl_style.font_family
        if mpl_style.fill_color is not None:
            kwargs["backgroundcolor"] = mpl_style.fill_color
        if mpl_style.line_color is not None:
            kwargs["color"] = mpl_style.line_color

        rotation_angle = text.direction.angle()
        if rotation_angle != 0.0:
            kwargs["rotation"] = rotation_angle

        axes.text(
            text.position.x,
            text.position.y,
            text.text,
            horizontalalignment=mpl_style.alignment,
            fontsize=mpl_style.font_size,
            **kwargs
        )
