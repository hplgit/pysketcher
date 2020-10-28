import pytest
from hypothesis import given
from hypothesis.strategies import floats, from_type, integers, sampled_from

from pysketcher import Style, TextStyle


class TestStyle(object):
    @given(from_type(Style), sampled_from(Style.LineStyle))
    def test_line_style(self, style: Style, line_style: Style.LineStyle):
        style.line_style = line_style
        assert style.line_style == line_style

    @given(from_type(Style), floats(allow_nan=False, allow_infinity=False))
    def test_line_width(self, style: Style, width: float):
        style.line_width = width
        assert style.line_width == width

    @given(from_type(Style), sampled_from(Style.Color))
    def test_line_color(self, style: Style, line_color: Style.Color):
        style.line_color = line_color
        assert style.line_color == line_color

    @given(from_type(Style), sampled_from(Style.Color))
    def test_fill_color(self, style: Style, fill_color: Style.Color):
        style.fill_color = fill_color
        assert style.fill_color == fill_color

    @given(from_type(Style), sampled_from(Style.FillPattern))
    def test_fill_pattern(self, style: Style, fill_pattern: Style.FillPattern):
        style.fill_pattern = fill_pattern
        assert style.fill_pattern == fill_pattern

    @given(from_type(Style), sampled_from(Style.ArrowStyle))
    def test_arrow(self, style: Style, arrow: Style.ArrowStyle):
        style.arrow = arrow
        assert style.arrow == arrow

    @given(from_type(Style), floats(allow_nan=False, allow_infinity=False))
    def test_shadow(self, style: Style, shadow: float):
        style.shadow = shadow
        assert style.shadow == shadow


class TestTextStyle(TestStyle):
    @given(from_type(Style), floats(allow_infinity=False, allow_nan=False))
    def test_font_size(self, style: TextStyle, font_size: float):
        style.font_size = font_size
        assert style.font_size == font_size

    @given(from_type(Style), sampled_from(TextStyle.FontFamily))
    def test_font_family(self, style: TextStyle, font_family: TextStyle.FontFamily):
        style.font_family = font_family
        assert style.font_family == font_family

    @given(from_type(Style), sampled_from(TextStyle.Alignment))
    def test_alignment(self, style: TextStyle, alignment: TextStyle.Alignment):
        style.alignment = alignment
        assert style.alignment == alignment
