import matplotlib.pyplot as plt

from pysketcher._text import Text
from pysketcher.backend.matplotlib._matplotlib_adapter import MatplotlibAdapter
from pysketcher.backend.matplotlib._matplotlib_style import MatplotlibTextStyle


class MatplotlibText(MatplotlibAdapter):
    """Renders a Text primitive."""

    def plot(self, text: Text, axes: plt.Axes):
        """Render a Text primitive.

        Write `text` string at a position (centered, left, right - according
        to the `alignment` string). `position` is a point in the coordinate
        system.

        Args:
            text: the ``Text`` object to be rendered.
            axes: the ``Axes`` to render the text object on.
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
