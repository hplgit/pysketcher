import numpy as np

from pysketcher.arc import ArcWithText
from pysketcher.style import Style


class Moment(ArcWithText):
    def __init__(
        self,
        text,
        center,
        radius,
        left=True,
        counter_clockwise=True,
        fontsize=0,
        text_spacing=1 / 60.0,
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
