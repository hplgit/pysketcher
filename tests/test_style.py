import pytest

from pysketcher import Style, TextStyle
from hypothesis import given
from hypothesis.strategies import floats, integers, sampled_from


class TestStyle(object):
    @pytest.fixture(scope="module")
    def style(self):
        return Style()

    @given(sampled_from(Style.LineStyle))
    def test_line_style(self, style: Style, line_style: Style.LineStyle):
        style.line_style = line_style
        assert style.line_style == line_style

    @given(floats(allow_nan=False, allow_infinity=False))
    def test_line_width(self, style: Style, width: float):
        style.line_width = width
        assert style.line_width == width

    @given(sampled_from(Style.Color))
    def test_line_color(self, style: Style, line_color: Style.Color):
        style.line_color = line_color
        assert style.line_color == line_color

    @given(sampled_from(Style.Color))
    def test_fill_color(self, style: Style, fill_color: Style.Color):
        style.fill_color = fill_color
        assert style.fill_color == fill_color

    @given(sampled_from(Style.FillPattern))
    def test_fill_pattern(self, style: Style, fill_pattern: Style.FillPattern):
        style.fill_pattern = fill_pattern
        assert style.fill_pattern == fill_pattern

    @given(sampled_from(Style.ArrowStyle))
    def test_arrow(self, style: Style, arrow: Style.ArrowStyle):
        style.arrow = arrow
        assert style.arrow == arrow

    @given(floats(allow_nan=False, allow_infinity=False))
    def test_shadow(self, shadow: float):
        under_test = Style()
        under_test.shadow = shadow
        assert under_test.shadow == shadow


class TestTextStyle(TestStyle):
    @pytest.fixture
    def style(self):
        return TextStyle()

    @given(floats(allow_infinity=False, allow_nan=False))
    def test_font_size(self, style: TextStyle, font_size: float):
        style.font_size = font_size
        assert style.font_size == font_size

    @given(sampled_from(TextStyle.FontFamily))
    def test_font_family(self, style: TextStyle, font_family: TextStyle.FontFamily):
        style.font_family = font_family
        assert style.font_family == font_family

    @given(sampled_from(TextStyle.Alignment))
    def test_alignment(self, style: TextStyle, alignment: TextStyle.Alignment):
        style.alignment = alignment
        assert style.alignment == alignment
