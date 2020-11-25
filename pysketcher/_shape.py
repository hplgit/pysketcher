from abc import ABC, abstractmethod

from pysketcher._point import Point
from pysketcher._style import Style


class Stylable(ABC):
    """Abstract Superclass for objects which can accept a style."""

    _style: Style

    @abstractmethod
    def __init__(self):
        self._style = Style()

    @property
    def style(self):
        """The style.

        Returns:
            The style associated with the class.
        """
        return self._style

    @style.setter
    def style(self, style: Style):
        self._style = style

    def set_line_width(self, line_width: float) -> "Stylable":
        """Set the line width.

        Args:
            line_width: The width of the line.

        Returns:
            The object with its style modified with the new value of ``line_width``.
        """
        self.style.line_width = line_width
        return self

    def set_line_style(self, line_style: Style.LineStyle) -> "Stylable":
        """Set the line style.

        Args:
            line_style: The width of the line.

        Returns:
            The object with its style modified with the new value of ``line_style``.
        """
        self.style.line_style = line_style
        return self

    def set_line_color(self, line_color: Style.Color) -> "Stylable":
        """Set the line color.

        Args:
            line_color: The color of the line.

        Returns:
            The object with its style modified with the new value of ``line_color``.
        """
        self.style.line_color = line_color
        return self

    def set_fill_pattern(self, fill_pattern: Style.FillPattern) -> "Stylable":
        """Set the fill_pattern style.

        Args:
            fill_pattern: The width of the line.

        Returns:
            The object with its style modified with the new value of ``line_style``.
        """
        self.style.fill_pattern = fill_pattern
        return self

    def set_fill_color(self, fill_color: Style.Color) -> "Stylable":
        """Set the fill color.

        Args:
            fill_color: The width of the line.

        Returns:
            The object with its style modified with the new value of ``fill_color``.
        """
        self.style.fill_color = fill_color
        return self

    def set_arrow(self, arrow: Style.ArrowStyle) -> "Stylable":
        """Set the arrows which should adorn the object.

        Args:
            arrow: The nature of the arrow.

        Returns:
            The object with its style modified with the new value of ``arrow``.
        """
        self.style.arrow = arrow
        return self

    def set_shadow(self, shadow: float) -> "Stylable":
        """Set the shadow.

        Args:
            shadow: The distance of the shadow from the object.

        Returns:
            The object with its style modified with the new value of ``shadow``.
        """
        self.style.shadow = shadow
        return self


class Shape(Stylable):
    """Superclass for drawing different geometric shapes.

    Subclasses define shapes, but drawing, rotation, translation,
    etc. are done in generic functions in this superclass.
    """

    @abstractmethod
    def __init__(self):
        super().__init__()

    @abstractmethod
    def rotate(self, angle: float, center: Point) -> "Shape":
        """Rotate the shape.

        Args:
            angle: The ``Angle`` in radians through which the shape should be rotated.
            center: The ``Point`` about which the rotation should be performed.

        Raises:
            NotImplementedError: when shape does not implement ``rotate``.
        """
        raise NotImplementedError

    def translate(self, vec) -> "Shape":
        """Translate the shape.

        Args:
            vec: The vector through which the ``Shape`` should be translated.

        Raises:
            NotImplementedError: when shape does not implement ``translate``.
        """
        raise NotImplementedError

    def scale(self, factor) -> "Shape":
        """Scale the shape.

        Args:
            factor: The factor by which the ``Shape`` should be scaled.

        Raises:
            NotImplementedError: when shape does not implement ``scale``.
        """
        raise NotImplementedError
