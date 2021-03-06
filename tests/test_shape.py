from hypothesis import HealthCheck, settings

from pysketcher import Shape, Style
from tests.utils import given_inferred


class TestShape:
    @given_inferred
    @settings(suppress_health_check=[HealthCheck.filter_too_much, HealthCheck.too_slow])
    def test_style(self, shape: Shape):
        style = Style()
        shape.style = style
        assert shape.style == style

    @given_inferred
    def test_set_line_width(self, shape: Shape, line_width: float):
        new_shape = shape.set_line_width(line_width)
        assert new_shape == shape
        assert new_shape.style.line_width == line_width

    @given_inferred
    def test_set_line_style(self, shape: Shape, line_style: Style.LineStyle):
        new_shape = shape.set_line_style(line_style)
        assert new_shape == shape
        assert new_shape.style.line_style == line_style

    @given_inferred
    def test_set_line_color(self, shape: Shape, color: Style.Color):
        new_shape = shape.set_line_color(color)
        assert new_shape == shape
        assert new_shape.style.line_color == color

    @given_inferred
    def test_set_fill_color(self, shape: Shape, color: Style.Color):
        new_shape = shape.set_fill_color(color)
        assert new_shape == shape
        assert new_shape.style.fill_color == color

    @given_inferred
    def test_set_fill_pattern(self, shape: Shape, fill_pattern: Style.FillPattern):
        new_shape = shape.set_fill_pattern(fill_pattern)
        assert new_shape == shape
        assert new_shape.style.fill_pattern == fill_pattern

    @given_inferred
    def test_set_arrow(self, shape: Shape, arrow: Style.ArrowStyle):
        new_shape = shape.set_arrow(arrow)
        assert new_shape == shape
        assert new_shape.style.arrow == arrow

    @given_inferred
    def test_set_shadow(self, shape: Shape, shadow: float):
        new_shape = shape.set_shadow(shadow)
        assert new_shape == shape
        assert new_shape.style.shadow == shadow
