import numpy as np
from .arc import ArcWithText


class Moment(ArcWithText):
    def __init__(self, text, center, radius,
                 left=True, counter_clockwise=True,
                 fontsize=0, text_spacing=1 / 60.):
        style = '->' if counter_clockwise else '<-'
        start_angle = np.pi / 2 if left else - np.pi / 2
        super().__init__(text, center, radius, start_angle, np.pi,
                         fontsize=fontsize,
                         text_spacing=text_spacing,
                         resolution=180)
        self._shapes['arc'].set_arrow(style)  # Curve object
