from math import inf, sqrt

import numpy as np
import pytest
from hypothesis import assume, given, infer, note

from pysketcher import Point
from tests.utils import given_inferred

from .conftest import isclose, mx


class TestPoint:
    @given_inferred
    def test_coordinates(self, x: np.float64, y: np.float64) -> None:
        p = Point(x, y)
        assert p.x == x
        assert p.y == y

    @given_inferred
    def test_equality(self, x: np.float64, y: np.float64) -> None:
        assert Point(x, y) == Point(x, y)

    @given_inferred
    def test_adding(
        self, x1: np.float64, x2: np.float64, y1: np.float64, y2: np.float64
    ):
        a = Point(x1, y1)
        b = Point(x2, y2)
        assert a + b == Point(x1 + x2, y1 + y2)

    @given_inferred
    def test_translation(
        self, x1: np.float64, x2: np.float64, y1: np.float64, y2: np.float64
    ):
        a = Point(x1, y1)
        b = Point(x2, y2)
        assert a + b == Point(x1 + x2, y1 + y2)

    @given_inferred
    def test_subtraction(
        self, x1: np.float64, x2: np.float64, y1: np.float64, y2: np.float64
    ):
        a = Point(x1, y1)
        b = Point(x2, y2)
        assert a - b == Point(x1 - x2, y1 - y2)

    @given_inferred
    def test_multiplication(self, x: np.float64, y: np.float64, s: np.float64):
        a = Point(x, y)
        assert a * s == Point(x * s, y * s)

    @given_inferred
    def test_multiplication(self, x: np.float64, y: np.float64, s: np.float64):
        a = Point(x, y)
        assert a.scale(s) == Point(x * s, y * s)

    @given_inferred
    def test_abs(self, x: np.float64, y: np.float64):
        assume(x * x != inf)
        assume(y * y != inf)
        a = Point(x, y)
        assert abs(a) == sqrt(x * x + y * y)

    @given_inferred
    def test_angle(self, a: Point):
        angle = a.angle()
        b = Point(abs(a), 0.0).rotate(angle, Point(0.0, 0.0))
        assume(abs(a) < mx)
        note(f"The angle is : {np.format_float_scientific(a.angle())}")
        note(f"The length is : {np.format_float_scientific(abs(a))}")
        assert a == b
        assert -np.pi <= angle <= np.pi

    @given_inferred
    def test_unit_vector(self, x: np.float64, y: np.float64):
        a = Point(x, y)
        if isclose(abs(a), 0.0):
            with pytest.raises(ZeroDivisionError):
                a.unit_vector()
        else:
            b = a.unit_vector()
            note(f"angle of a: {np.format_float_scientific(a.angle())}")
            note(f"angle of b: {np.format_float_scientific(b.angle())}")
            assert isclose(a.angle(), b.angle())
            note(f"magnitude of b: {abs(b)}")
            assert isclose(abs(b), 1.0)

    @given_inferred
    def test_normal_vector(self, a: Point):
        if isclose(abs(a), 0.0):
            with pytest.raises(ZeroDivisionError):
                a.normal()
        else:
            angle = a.normal().angle() - a.angle()
            # TODO: write an angle class which deals with this crap!
            while not abs(angle) <= np.pi:
                if angle < -np.pi:
                    angle = angle + 2 * np.pi
                elif angle > np.pi:
                    angle = angle - 2 * np.pi
            assert isclose(angle, np.pi / 2.0)

    #
    # @given_inferred
    # def test_rotation_about_zero(self, a: Point, angle: np.float64):
    #     b = a.rotate(angle, Point(0., 0.))
    #     assert isclose(b.angle() - a.angle(), angle)
    #
    # @given_inferred
    # def test_rotation(self, a: Point, angle: np.float64, center: Point):
    #     b = a.rotate(angle, center)
    #     assert isclose((b - center).angle() - (a - center).angle(), angle)


#
#
# from_coordinate_lists_data = [
#     ([1, 2, 3, 4], [1, 2, 3, 4], [Point(1, 1), Point(2, 2), Point(3, 3), Point(4, 4)])
# ]
#
#
# @pytest.mark.parametrize("xs, ys, expected", from_coordinate_lists_data)
# def test_from_coordinate_lists(xs: List[float], ys: List[float], expected: List[Point]):
#     assert Point.from_coordinate_lists(xs, ys) == expected
#
#
# @pytest.mark.parametrize("xs, ys, expected", from_coordinate_lists_data)
# def test_to_coordinate_lists(xs, ys, expected):
#     assert Point.to_coordinate_lists(expected) == (xs, ys)
