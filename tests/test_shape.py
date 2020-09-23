import contextlib
import logging
from abc import abstractmethod

import pytest
from hypothesis import example, given, note
from hypothesis.strategies import (
    SearchStrategy,
    composite,
    floats,
    from_type,
    sampled_from,
)

from pysketcher import Arrow, Axis, Force, Line, Point, Shape, Style

from .test_point import nfloats


def test_cannot_instantiate():
    with pytest.raises(TypeError):
        shape = Shape()


class TestShape:
    @given(from_type(Shape))
    @example(Line(Point(1.0, 1.0), Point(0.0, 1.0)))
    def test_style(self, caplog, shape: Shape):
        note(shape)
        style = Style()
        shape.style = style
        assert shape.style == style

    @given(from_type(Shape), nfloats())
    def test_set_line_width(self, shape: Shape, line_width: float):
        new_shape = shape.set_line_width(line_width)
        assert new_shape == shape
        assert new_shape.style.line_width == line_width

    @given(from_type(Shape), sampled_from(Style.LineStyle))
    def test_set_line_style(self, shape: Shape, line_style: Style.LineStyle):
        new_shape = shape.set_line_style(line_style)
        assert new_shape == shape
        assert new_shape.style.line_style == line_style

    @given(from_type(Shape), sampled_from(Style.Color))
    def test_set_line_color(self, shape: Shape, color: Style.Color):
        new_shape = shape.set_line_color(color)
        assert new_shape == shape
        assert new_shape.style.line_color == color

    @given(from_type(Shape), sampled_from(Style.Color))
    def test_set_fill_color(self, shape: Shape, color: Style.Color):
        new_shape = shape.set_fill_color(color)
        assert new_shape == shape
        assert new_shape.style.fill_color == color

    @given(from_type(Shape), sampled_from(Style.FillPattern))
    def test_set_fill_pattern(self, shape: Shape, fill_pattern: Style.FillPattern):
        new_shape = shape.set_fill_pattern(fill_pattern)
        assert new_shape == shape
        assert new_shape.style.fill_pattern == fill_pattern

    @given(from_type(Shape), sampled_from(Style.ArrowStyle))
    def test_set_arrow(self, shape: Shape, arrow: Style.ArrowStyle):
        new_shape = shape.set_arrow(arrow)
        assert new_shape == shape
        assert new_shape.style.arrow == arrow

    @given(from_type(Shape), floats(allow_nan=False, allow_infinity=False))
    def test_set_shadow(self, shape: Shape, shadow: float):
        new_shape = shape.set_shadow(shadow)
        assert new_shape == shape
        assert new_shape.style.shadow == shadow
