from collections import namedtuple
from enum import auto, unique

from pysketcher._utils import DocEnum

Arrow = namedtuple("Arrow", "start end")


class Style:
    """Represents the visual characteristics of a Drawable object."""

    @unique
    class LineStyle(DocEnum):
        """Represents the manner of line to be drawn."""

        SOLID = auto(), "An unbroken line."
        DOTTED = auto(), "A dotted line."
        DASH_DOT = auto(), "An alternating dash dot line."
        DASHED = auto(), "A dashed line."

    @unique
    class Color(DocEnum):
        """Represents the color in which something should be rendered."""

        GREY = auto(), "The color grey."
        BLACK = auto(), "The color black."
        BROWN = auto(), "The color brown."
        RED = auto(), "The color red."
        ORANGE = auto(), "The color orange."
        YELLOW = auto(), " The color yellow."
        GREEN = auto(), "The color green."
        CYAN = auto(), "The color cyan."
        BLUE = auto(), "The color blue."
        MAGENTA = auto(), "The color magenta."
        PURPLE = auto(), "The color purple."
        WHITE = auto(), "The color white."

    @unique
    class FillPattern(DocEnum):
        """Represents the pattern in which something can be shaded."""

        VERTICAL = auto(), "A pattern made up for vertical lines."
        HORIZONTAL = auto(), "A pattern made up of horizontal lines."
        CROSS = auto(), "A pattern made of crossing diagonal lines."
        SQUARE = auto(), "A pattern made of crossing horizontal and vertical lines."
        STAR = auto(), "A pattern made of stars."
        DOT = auto(), "A pattern made of dots,"
        CIRCLE = auto(), "A pattern made of circles."
        SMALL_CIRCLE = auto(), "A pattern made of small circles."
        UP_RIGHT_TO_LEFT = auto(), "A pattern made of diagonal lines from SE to NW."
        UP_LEFT_TO_RIGHT = auto(), "A pattern made of diagonal lines from SW to NE."

    @unique
    class ArrowStyle(DocEnum):
        """Represents the style of arrow which can adorn a line."""

        START = Arrow(True, False), "Place an arrowhead at the start of the line."
        END = Arrow(False, True), "Place an arrowhead at the end of the line."
        DOUBLE = Arrow(True, True), "Place an arrowhead at both ends of the line."

    _line_style: LineStyle
    _line_width: float
    _line_color: Color
    _fill_pattern: FillPattern
    _fill_color: Color
    _arrow: ArrowStyle
    _shadow: int

    def __init__(self):
        self._line_style = self.LineStyle.SOLID
        self._line_width = 1.0
        self._line_color = self.Color.BLACK
        self._fill_pattern = None
        self._fill_color = None
        self._arrow = None
        self._shadow = None

    @property
    def line_style(self) -> LineStyle:
        """The style of line."""
        return self._line_style

    @line_style.setter
    def line_style(self, line_style: LineStyle):
        self._line_style = line_style

    @property
    def line_width(self) -> float:
        """The width of line."""
        return self._line_width

    @line_width.setter
    def line_width(self, line_width: float):
        self._line_width = line_width

    @property
    def line_color(self) -> Color:
        """The color of line."""
        return self._line_color

    @line_color.setter
    def line_color(self, color: Color):
        self._line_color = color

    @property
    def fill_color(self) -> Color:
        """The color of fill."""
        return self._fill_color

    @fill_color.setter
    def fill_color(self, color: Color):
        self._fill_color = color

    @property
    def fill_pattern(self) -> FillPattern:
        """The pattern of fill."""
        return self._fill_pattern

    @fill_pattern.setter
    def fill_pattern(self, fill_pattern: FillPattern):
        self._fill_pattern = fill_pattern
        if not self.fill_color:
            self.fill_color = self.Color.WHITE

    @property
    def arrow(self) -> ArrowStyle:
        """The arrow which should adorn the line."""
        return self._arrow

    @arrow.setter
    def arrow(self, arrow: ArrowStyle):
        self._arrow = arrow

    @property
    def shadow(self) -> float:
        """The shadow which the object should cast."""
        return self._shadow

    @shadow.setter
    def shadow(self, shadow: float):
        self._shadow = shadow

    def __str__(self):
        """Returns a representation of the style in string form."""
        return (
            "line_style: %s, line_width: %s, line_color: %s,"
            " fill_pattern: %s, fill_color: %s, arrow: %s shadow: %s"
            % (
                self.line_style,
                self.line_width,
                self.line_color,
                self.fill_pattern,
                self.fill_color,
                self.arrow,
                self.shadow,
            )
        )


class TextStyle(Style):
    """Represents the visual style of a text object."""

    class FontFamily(DocEnum):
        """Represents the font which should be used to render text."""

        SERIF = auto(), "A font with serifs."
        SANS = auto(), "A font without serifs."
        MONO = auto(), "An equally spaced font."

    class Alignment(DocEnum):
        """Represents the horizontal alignment of text."""

        LEFT = auto(), "Align text to the left."
        CENTER = auto(), "Align text to the center."
        RIGHT = auto(), "Align text to the right."

    _font_size: float
    _font_family: FontFamily
    _alignment: Alignment

    def __init__(
        self,
    ):
        super().__init__()
        self._font_size = 12
        self._font_family = self.FontFamily.SANS
        self._alignment = self.Alignment.CENTER

    @property
    def font_size(self) -> float:
        """The size of text."""
        return self._font_size

    @font_size.setter
    def font_size(self, font_size: float):
        self._font_size = font_size

    @property
    def font_family(self) -> FontFamily:
        """The family of font in which text is rendered."""
        return self._font_family

    @font_family.setter
    def font_family(self, font_family: FontFamily):
        self._font_family = font_family

    @property
    def alignment(self):
        """The alignment to be used when text is rendered."""
        return self._alignment

    @alignment.setter
    def alignment(self, alignment: Alignment):
        self._alignment = alignment
