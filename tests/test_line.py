import numpy as np
import pytest
from hypothesis import given
from hypothesis.strategies import from_type

from pysketcher import Line, Point, Shape
from tests.test_point import nfloats


class TestLine:
    @given(nfloats(), nfloats(), nfloats(), nfloats())
    def test_start(self, x1, y1, x2, y2):
        line = Line(Point(x1, y1), Point(x2, y2))
        assert line.start == Point(x1, y1)
        assert line.end == Point(x2, y2)

    # def test_rotate(self, line: Line, center: Point, theta: float, expected: Line):
    #     result = line.rotate(theta, center)
    #     assert abs(result.start - expected.start) < 1e-14
    #     assert abs(result.end - expected.end) < 1e-14
