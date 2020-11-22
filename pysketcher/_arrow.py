from pysketcher._line import Line
from pysketcher._point import Point
from pysketcher._style import Style


class Arrow(Line):
    """Draw an arrow as Line with arrow pointing towards end.

    Args:
        start: The start of the arrow.
        end: The end of the arrow.

    Examples:
        >>> arrow = ps.Arrow(
        ...     ps.Point(1.0, 1.0),
        ...     ps.Point(
        ...         3.0,
        ...         1.0,
        ...     ),
        ... )
        >>> fig = ps.Figure(0.0, 4.0, 0.0, 2.0, backend=MatplotlibBackend)
        >>> fig.add(arrow)
        >>> fig.save("pysketcher/images/arrow.png")

    .. figure:: images/arrow.png
        :alt: An example of Arrow.
        :figclass: align-center

        An example of ``Arrow``.
    """

    def __init__(self, start: Point, end: Point):
        super().__init__(start, end)
        self.style.arrow = Style.ArrowStyle.END


class DoubleArrow(Line):
    """Draw an arrow as Line with arrow pointing towards start and end.

    Args:
        start: The start of the double arrow.
        end: The end of the double arrow.

    Examples:
        >>> double_arrow = ps.DoubleArrow(
        ...     ps.Point(1.0, 1.0),
        ...     ps.Point(
        ...         3.0,
        ...         1.0,
        ...     ),
        ... )
        >>> fig = ps.Figure(0.0, 4.0, 0.0, 2.0, backend=MatplotlibBackend)
        >>> fig.add(double_arrow)
        >>> fig.save("pysketcher/images/double_arrow.png")

    .. figure:: images/double_arrow.png
        :alt: An example of DoubleArrow.
        :figclass: align-center

        An example of ``DoubleArrow``.
    """

    def __init__(self, start: Point, end: Point):
        super().__init__(start, end)
        self.style.arrow = Style.ArrowStyle.DOUBLE
