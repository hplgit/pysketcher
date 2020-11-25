from pysketcher._curve import Curve
from pysketcher._line import Line
from pysketcher._point import Point
from pysketcher._rectangle import Rectangle
from pysketcher._style import Style
from pysketcher.composition import Composition


class Dashpot(Composition):
    """A representation of a dashpot.

    Specify a vertical dashpot of height `total_length` and `start` as
    bottom/starting point. The first bar part has length `bar_length`.
    Then comes the dashpot as a rectangular construction of total
    width `width` and height `dashpot_length`. The position of the
    piston inside the rectangular dashpot area is given by
    `piston_pos`, which is the distance between the first bar (given
    by `bar_length`) to the piston.
    If some of `dashpot_length`, `bar_length`, `width` or `piston_pos`
    are not given, suitable default values are calculated.

    Args:
        start: The starting point of the Dashpot.
        total_length: The total length of the Dashpot including bar.
        bar_length: The length of the bar.
        width: The width of the dashpot.
        dashpot_length: The length of the Dashpot excluding bar.
        piston_pos: The position of the piston. Defaults to 1/3 length.

    Examples:
        >>> L = 12.0
        >>> H = L / 6.0
        >>> x = L / 2.0
        >>> d_start = ps.Point(0, 0)
        >>> d = ps.Dashpot(d_start, L + x)
        >>> fig = ps.Figure(-3, 3, -1, 13, backend=MatplotlibBackend)
        >>> fig.add(d)
        >>> fig.save("pysketcher/images/dashpot.png")

        .. figure:: images/dashpot.png
            :alt: An example of Dashpot.
            :figclass: align-center
            :scale: 30%

            An example of ``Dashpot``.
    """

    _dashpot_fraction = 1.0 / 2  # fraction of total_length
    _piston_gap_fraction = 1.0 / 6  # fraction of width
    _piston_thickness_fraction = 1.0 / 8  # fraction of dashplot_length

    def __init__(
        self,
        start: Point,
        total_length: float,
        bar_length: float = None,
        width: float = None,
        dashpot_length: float = None,
        piston_pos: float = None,
    ):
        B = start
        L = total_length
        if width is None:
            w = L / 10.0  # total width 1/5 of length
        else:
            w = width / 2.0
        s = bar_length

        shapes = {}
        # dashpot is p0-p1 in y and width 2*w
        if dashpot_length is None:
            if s is None:
                f = Dashpot._dashpot_fraction
                s = L * (1 - f) / 2.0  # default
            p1 = Point(B.x, B.y + L - s)
            dashpot_length = f * L
        else:
            if s is None:
                f = 1.0 / 2  # the bar lengths are taken as f*dashpot_length
                s = f * dashpot_length  # default
            p1 = Point(B.x, B.y + s + dashpot_length)
        p0 = Point(B.x, B.y + s)
        p2 = Point(B.x, B.y + L)

        if not (p2.y > p1.y > p0.y):
            raise ValueError(
                (
                    "Dashpot has inconsistent dimensions! start: %g, "
                    "dashpot begin: %g, dashpot end: %g, very end: %g"
                    % (B.y, p0.y, p1.y, p2.y)
                )
            )

        shapes["line start"] = Line(B, p0)

        shapes["pot"] = Curve(
            [
                Point(p1.x - w, p1.y),
                Point(p0.x - w, p0.y),
                Point(p0.x + w, p0.y),
                Point(p1.x + w, p1.y),
            ]
        )
        piston_thickness = dashpot_length * Dashpot._piston_thickness_fraction
        if piston_pos is None:
            piston_pos = 1 / 3.0 * dashpot_length
        if piston_pos < 0:
            piston_pos = 0
        elif piston_pos > dashpot_length:
            piston_pos = dashpot_length - piston_thickness

        abs_piston_pos = p0.y + piston_pos

        gap = w * Dashpot._piston_gap_fraction
        shapes["piston"] = Composition(
            {
                "line": Line(p2, Point(B.x, abs_piston_pos + piston_thickness)),
                "rectangle": Rectangle(
                    Point(B.x - w + gap, abs_piston_pos),
                    2 * w - 2 * gap,
                    piston_thickness,
                ),
            }
        )
        shapes["piston"]["rectangle"].set_fill_pattern(Style.FillPattern.CROSS)

        super().__init__(shapes)

        # self.bar_length = s
        # self.width = 2 * w
        # self.piston_pos = piston_pos
        # self.dashpot_length = dashpot_length
        #
        # # Dimensions
        # start = Text_wArrow('start', (B[0]-1.5*w,B[1]-1.5*w), B)
        # width = Distance_wText((B[0]-w, B[1]-3.5*w), (B[0]+w, B[1]-3.5*w),
        #                        'width')
        # dplength = Distance_wText((B[0]+2*w, p0[1]), (B[0]+2*w, p1[1]),
        #                           'dashpot_length', text_pos=(B[0]+w,B[1]-w))
        # blength = Distance_wText((B[0]-2*w, B[1]), (B[0]-2*w, p0[1]),
        #                          'bar_length', text_pos=(B[0]-6*w,p0[1]-w))
        # ppos    = Distance_wText((B[0]-2*w, p0[1]), (B[0]-2*w, p0[1]+piston_pos),
        #                          'piston_pos', text_pos=(B[0]-6*w,p0[1]+piston_pos-w))
        # tlength = Distance_wText((B[0]+4*w, B[1]), (B[0]+4*w, B[1]+L),
        #                          'total_length',
        #                          text_pos=(B[0]+4.5*w, B[1]+L-2*w))
        # line = Line((B[0]+w, abs_piston_pos), (B[0]+7*w, abs_piston_pos))
        #   .set_linestyle('dashed')
        #   .set_linecolor('black')
        #   .set_linewidth(1)
        # pp = Text('abs_piston_pos', (B[0]+7*w, abs_piston_pos), alignment='left')
        # dims = {'start': start, 'width': width, 'dashpot_length': dplength,
        #         'bar_length': blength, 'total_length': tlength,
        #         'piston_pos': ppos,}
        # #'abs_piston_pos': Composition({'line': line, 'text': pp})}
        # self.dimensions = dims

    # def geometric_features(self):
    #     """
    #     Recorded geometric features:
    #     ==================== =============================================
    #     Attribute            Description
    #     ==================== =============================================
    #     start                Start point of dashpot.
    #     end                  End point of dashpot.
    #     bar_length           Length of first bar (from start to spring).
    #     dashpot_length       Length of dashpot middle part.
    #     width                Total width of dashpot.
    #     piston_pos           Position of piston in dashpot, relative to
    #                          start[1] + bar_length.
    #     ==================== =============================================
    #     """
    #     d = {'start': self.shapes['line start'].geometric_features()['start'],
    #          'end': self.shapes['piston']['line'].geometric_features()['start'],
    #          'bar_length': self.bar_length,
    #          'piston_pos': self.piston_pos,
    #          'width': self.width,
    #          'dashpot_length': self.dashpot_length,
    #          }
    #     return d
