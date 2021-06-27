from hypothesis import given
from hypothesis.strategies import floats, sampled_from
import pytest

from pysketcher import Line, Point, Shape, Style, Text
from pysketcher.composition import Composition


class TestCompositionStyle:
    @pytest.fixture(scope="module")
    def composition(self):
        shape1 = Line(Point(0, 1), Point(1, 1))
        shape2 = Line(Point(1, 1), Point(0, 2))
        text = Text("This is a test.", Point(2, 2))
        composition = Composition(
            {
                "shape1": shape1,
                "shape2": shape2,
                "test": text,
            }
        )
        return composition

    @given(sampled_from(Style.LineStyle))
    def test_line_style(self, composition: Composition, line_style: Style.LineStyle):
        composition.style.line_style = line_style
        assert composition["shape1"].style.line_style == line_style
        assert composition["shape2"].style.line_style == line_style

    @given(floats(allow_nan=False, allow_infinity=False))
    def test_line_width(self, composition: Composition, line_width: float):
        composition.style.line_width = line_width
        assert composition["shape1"].style.line_width == line_width
        assert composition["shape2"].style.line_width == line_width

    @given(sampled_from(Style.Color))
    def test_line_color(self, composition: Composition, line_color: Style.Color):
        composition.style.line_color = line_color
        assert composition["shape1"].style.line_color == line_color
        assert composition["shape2"].style.line_color == line_color

    @given(sampled_from(Style.Color))
    def test_fill_color(self, composition: Composition, fill_color: Style.Color):
        composition.style.fill_color = fill_color
        assert composition["shape1"].style.fill_color == fill_color
        assert composition["shape2"].style.fill_color == fill_color

    @given(sampled_from(Style.FillPattern))
    def test_fill_pattern(
        self, composition: Composition, fill_pattern: Style.FillPattern
    ):
        composition.style.fill_pattern = fill_pattern
        assert composition["shape1"].style.fill_pattern == fill_pattern
        assert composition["shape2"].style.fill_pattern == fill_pattern

    @given(sampled_from(Style.ArrowStyle))
    def test_arrow(self, composition: Composition, arrow: Style.ArrowStyle):
        composition.style.arrow = arrow
        assert composition["shape1"].style.arrow == arrow
        assert composition["shape2"].style.arrow == arrow

    @given(floats(allow_nan=False, allow_infinity=False))
    def test_shadow(self, composition: Composition, shadow: float):
        composition.style.shadow = shadow
        assert composition["shape1"].style.shadow == shadow
        assert composition["shape2"].style.shadow == shadow

    def test_iteration(self, composition: Composition):
        for shape in composition:
            assert isinstance(shape, Shape)
