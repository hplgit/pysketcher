import numpy as np
from hypothesis import assume, given, infer
from hypothesis.strategies import builds

from pysketcher import Line, Point
from tests.conftest import make_float
from tests.utils import given_inferred


class TestLine:
    @given_inferred
    def test_start(self, a: Point, b: Point) -> None:
        assume(a != b)
        line = Line(a, b)
        assert line.start == a
        assert line.end == b

    # def test_rotate(self, line: Line, center: Point, theta: float, expected: Line):
    #     result = line.rotate(theta, center)
    #     assert abs(result.start - expected.start) < 1e-14
    #     assert abs(result.end - expected.end) < 1e-14
