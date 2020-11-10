from collections import namedtuple
from enum import Enum, auto, unique

Arrow = namedtuple("Arrow", "start end")


class Style:
    @unique
    class LineStyle(Enum):
        SOLID = auto()
        DOTTED = auto()
        DASH_DOT = auto()
        DASHED = auto()

    @unique
    class Color(Enum):
        GREY = auto()
        BLACK = auto()
        BROWN = auto()
        RED = auto()
        ORANGE = auto()
        YELLOW = auto()
        GREEN = auto()
        CYAN = auto()
        BLUE = auto()
        MAGENTA = auto()
        PURPLE = auto()
        WHITE = auto()

    @unique
    class FillPattern(Enum):
        VERTICAL = auto()
        HORIZONTAL = auto()
        CROSS = auto()
        SQUARE = auto()
        STAR = auto()
        DOT = auto()
        CIRCLE = auto()
        SMALL_CIRCLE = auto()
        UP_RIGHT_TO_LEFT = auto()
        UP_LEFT_TO_RIGHT = auto()

    @unique
    class ArrowStyle(Enum):
        START = Arrow(True, False)
        END = Arrow(False, True)
        DOUBLE = Arrow(True, True)

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
        return self._line_style

    @line_style.setter
    def line_style(self, line_style: LineStyle):
        self._line_style = line_style

    @property
    def line_width(self) -> float:
        return self._line_width

    @line_width.setter
    def line_width(self, line_width: float):
        self._line_width = line_width

    @property
    def line_color(self) -> Color:
        return self._line_color

    @line_color.setter
    def line_color(self, color: Color):
        self._line_color = color

    @property
    def fill_color(self) -> Color:
        return self._fill_color

    @fill_color.setter
    def fill_color(self, color: Color):
        self._fill_color = color

    @property
    def fill_pattern(self) -> FillPattern:
        return self._fill_pattern

    @fill_pattern.setter
    def fill_pattern(self, fill_pattern: FillPattern):
        self._fill_pattern = fill_pattern
        if not self.fill_color:
            self.fill_color = self.Color.WHITE

    @property
    def arrow(self) -> ArrowStyle:
        return self._arrow

    @arrow.setter
    def arrow(self, arrow: ArrowStyle):
        self._arrow = arrow

    @property
    def shadow(self) -> float:
        return self._shadow

    @shadow.setter
    def shadow(self, shadow: float):
        self._shadow = shadow

    def __str__(self):
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
    class FontFamily(Enum):
        SERIF = auto()
        SANS = auto()
        MONO = auto()

    class Alignment(Enum):
        LEFT = auto()
        CENTER = auto()
        RIGHT = auto()

    _font_size: float
    _font_family: FontFamily
    _alignment: Alignment

    def __init__(self,):
        super().__init__()
        self._font_size = 12
        self._font_family = self.FontFamily.SANS
        self._alignment = self.Alignment.CENTER

    @property
    def font_size(self) -> float:
        return self._font_size

    @font_size.setter
    def font_size(self, font_size: float):
        self._font_size = font_size

    @property
    def font_family(self) -> FontFamily:
        return self._font_family

    @font_family.setter
    def font_family(self, font_family: FontFamily):
        self._font_family = font_family

    @property
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, alignment: Alignment):
        self._alignment = alignment
