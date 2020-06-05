import pytest
import numpy as np

from pysketcher import Shape, Line, Point
from .test_shape import ShapeContract


class TestLine(ShapeContract):
    @pytest.fixture
    def shape(self, request) -> Shape:
        return Line(Point(0, 1), Point(1, 1))

    def test_start(self, shape: Shape):
        assert shape.start == Point(0, 1)

    def test_end(self, shape: Shape):
        assert shape.end == Point(1, 1)

    rotate_data = [
        (Line(Point(0, 0), Point(1, 0)), np.pi / 2,     Point(0, 0), Line(Point(0, 0), Point(0, 1)) ),
        (Line(Point(0, 0), Point(1, 0)), np.pi,         Point(0, 0), Line(Point(0, 0), Point(-1, 0))),
        (Line(Point(0, 0), Point(1, 0)), 3 * np.pi / 2, Point(0, 0), Line(Point(0, 0), Point(0, -1))),
        (Line(Point(0, 0), Point(1, 0)), 2 * np.pi,     Point(0, 0), Line(Point(0, 0), Point(1, 0)))
    ]

    @pytest.mark.parametrize("line, theta, center, expected", rotate_data)
    def test_rotate(self, line: Line, center: Point, theta: float, expected: Line):
        result = line.rotate(theta, center)
        assert abs(result.start - expected.start) < 1E-14
        assert abs(result.end - expected.end) < 1E-14
