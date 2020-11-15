from pysketcher._style import Style, TextStyle


class MatplotlibStyle:
    _style: Style
    LINE_STYLE_MAP = {
        Style.LineStyle.SOLID: "-",
        Style.LineStyle.DOTTED: ":",
        Style.LineStyle.DASHED: "--",
        Style.LineStyle.DASH_DOT: "-.",
    }
    FILL_PATTERN_MAP = {
        Style.FillPattern.CIRCLE: "O",
        Style.FillPattern.CROSS: "x",
        Style.FillPattern.DOT: ".",
        Style.FillPattern.HORIZONTAL: "-",
        Style.FillPattern.SQUARE: "+",
        Style.FillPattern.STAR: "*",
        Style.FillPattern.SMALL_CIRCLE: "o",
        Style.FillPattern.VERTICAL: "|",
        Style.FillPattern.UP_LEFT_TO_RIGHT: "//",
        Style.FillPattern.UP_RIGHT_TO_LEFT: "\\\\",
    }
    COLOR_MAP = {
        Style.Color.GREY: "grey",
        Style.Color.BLACK: "black",
        Style.Color.BLUE: "blue",
        Style.Color.BROWN: "brown",
        Style.Color.CYAN: "cyan",
        Style.Color.GREEN: "green",
        Style.Color.MAGENTA: "magenta",
        Style.Color.ORANGE: "orange",
        Style.Color.PURPLE: "purple",
        Style.Color.RED: "red",
        Style.Color.YELLOW: "yellow",
        Style.Color.WHITE: "white",
    }
    ARROW_MAP = {
        Style.ArrowStyle.DOUBLE: "<->",
        Style.ArrowStyle.START: "<-",
        Style.ArrowStyle.END: "->",
    }

    def __init__(self, style: Style):
        self._style = style

    @property
    def line_width(self) -> float:
        return self._style.line_width

    @property
    def line_style(self) -> str:
        return self.LINE_STYLE_MAP.get(self._style.line_style)

    @property
    def line_color(self):
        return self.COLOR_MAP.get(self._style.line_color)

    @property
    def fill_color(self):
        return self.COLOR_MAP.get(self._style.fill_color)

    @property
    def fill_pattern(self):
        return self.FILL_PATTERN_MAP.get(self._style.fill_pattern)

    @property
    def arrow(self):
        return self.ARROW_MAP.get(self._style.arrow)

    @property
    def shadow(self):
        return self._style.shadow

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


class MatplotlibTextStyle(MatplotlibStyle):
    FONT_FAMILY_MAP = {
        TextStyle.FontFamily.SERIF: "serif",
        TextStyle.FontFamily.SANS: "sans-serif",
        TextStyle.FontFamily.MONO: "monospace",
    }

    ALIGNMENT_MAP = {
        TextStyle.Alignment.LEFT: "left",
        TextStyle.Alignment.RIGHT: "right",
        TextStyle.Alignment.CENTER: "center",
    }

    _style: TextStyle

    def __init__(self, text_style: TextStyle):
        super().__init__(text_style)

    @property
    def font_size(self) -> float:
        return self._style.font_size

    @property
    def font_family(self) -> str:
        return self.FONT_FAMILY_MAP.get(self._style.font_family)

    @property
    def alignment(self) -> str:
        return self.ALIGNMENT_MAP.get(self._style.alignment)
