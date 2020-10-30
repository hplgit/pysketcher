import numpy as np
from hypothesis import assume

from pysketcher.angle import Angle
from tests.utils import given_inferred


class TestAngle:
    @given_inferred
    def test_range(self, x: Angle):
        assert -np.pi <= x <= np.pi

    @given_inferred
    def test_equality(self, x: np.float64):
        if -np.pi < x < np.pi:
            assert x == Angle(x)
        else:
            assert Angle(x) == Angle(x)

    @given_inferred
    def test_addition(self, a: Angle, b: Angle):
        c = a + b
        assert type(c) == Angle
        assert -np.pi <= a <= np.pi

    @given_inferred
    def test_subtraction(self, a: Angle, b: Angle):
        c = a - b
        assert type(c) == Angle
        assert -np.pi <= a <= np.pi

    @given_inferred
    def test_multiplication(self, a: Angle, b: np.float64):
        c = a * b
        assert type(c) == Angle
        assert -np.pi <= a <= np.pi

    @given_inferred
    def test_division(self, a: Angle, b: np.float64):
        assume(1e-6 < abs(b) < 1e6)
        assume(b != 0.0)
        c = a / b
        assert type(c) == Angle
        assert -np.pi <= a <= np.pi
