import numpy as np

from pysketcher._arc import ArcWithText
from pysketcher._style import Style


class Moment(ArcWithText):
    r"""A symbol which represents a moment.

    This is an ``ArcWithText`` with the ``arc_angle`` fixed at :math:`\pi`.

    Args:
        text: The text to display.
        center: The centre of the moment.
        radius: The radius of the moment.
        start_angle: The angle from the +ve horizontal at which the moment should
            start.
        text_spacing: The spacing of the text.
        resolution: The number of points on the arc.

    Examples:
        >>> moment = ps.Moment("$M$", ps.Point(0, 0), 1.0, 0.0)
        >>> fig = ps.Figure(-1.2, 1.2, -1.2, 1.2, backend=MatplotlibBackend)
        >>> fig.add(moment)
        >>> fig.save("pysketcher/images/moment.png")

        .. figure:: images/moment.png
            :alt: An example of Moment.
            :figclass: align-center

            An example of ``Moment``.
    """

    def __init__(
        self,
        text,
        center,
        radius,
        left=True,
        counter_clockwise=True,
        fontsize=0,
        text_spacing=1 / 3.0,
    ):
        style = Style.ArrowStyle.END if counter_clockwise else Style.ArrowStyle.START
        start_angle = np.pi / 2 if left else -np.pi / 2
        super().__init__(
            text,
            center,
            radius,
            start_angle,
            np.pi,
            text_spacing=text_spacing,
            resolution=180,
        )
        self.set_arrow(style)  # Curve object
