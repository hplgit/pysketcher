from hypothesis import assume, HealthCheck, settings

from pysketcher import Line, Point
from tests.utils import given_inferred


class TestLine:
    @given_inferred
    @settings(suppress_health_check=[HealthCheck.filter_too_much])
    def test_start(self, a: Point, b: Point) -> None:
        assume(a != b)
        line = Line(a, b)
        assert line.start == a
        assert line.end == b

    # def test_rotate(self, line: Line, center: Point, theta: float, expected: Line):
    #     result = line.rotate(theta, center)
    #     assert abs(result.start - expected.start) < 1e-14
    #     assert abs(result.end - expected.end) < 1e-14
