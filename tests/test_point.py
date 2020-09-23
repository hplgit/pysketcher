from math import inf, isclose, sqrt
from typing import List

import numpy as np
import pytest
from hypothesis import assume, given
from hypothesis.extra.numpy import from_dtype

from pysketcher import Point


def nfloats():
    return (
        from_dtype(np.dtype("float64"))
        .filter(lambda x: not np.isnan(x))
        .filter(lambda x: not np.isinf(x))
    )


@given(nfloats(), nfloats())
def test_coordinates(x, y):
    p = Point(x, y)
    assert p.x == x
    assert p.y == y


@given(nfloats(), nfloats())
def test_equality(x, y):
    assert Point(x, y) == Point(x, y)


@given(nfloats(), nfloats(), nfloats(), nfloats())
def test_adding(x1, x2, y1, y2):
    a = Point(x1, y1)
    b = Point(x2, y2)
    assert a + b == Point(x1 + x2, y1 + y2)


@given(nfloats(), nfloats(), nfloats(), nfloats())
def test_translation(x1, x2, y1, y2):
    a = Point(x1, y1)
    b = Point(x2, y2)
    assert a + b == Point(x1 + x2, y1 + y2)


@given(nfloats(), nfloats(), nfloats(), nfloats())
def test_subtraction(x1, x2, y1, y2):
    a = Point(x1, y1)
    b = Point(x2, y2)
    assert a - b == Point(x1 - x2, y1 - y2)


@given(nfloats(), nfloats(), nfloats())
def test_multiplication(x: float, y: float, s: float):
    a = Point(x, y)
    assert a * s == Point(x * s, y * s)


@given(nfloats(), nfloats(), nfloats())
def test_multiplication(x: float, y: float, s: float):
    a = Point(x, y)
    assert a.scale(s) == Point(x * s, y * s)


@given(nfloats(), nfloats())
def test_abs(x: float, y: float):
    assume(x * x != inf)
    assume(y * y != inf)
    a = Point(x, y)
    assert abs(a) == sqrt(x * x + y * y)


@given(nfloats(), nfloats())
def test_angle(x: float, y: float):
    assume(not isclose(x, 0.0))
    a = Point(x, y)
    b = Point(abs(a), 0.0).rotate(a.angle(), Point(0.0, 0.0))
    assume(b.x != np.nan)
    assume(b.y != np.nan)
    assume(a.angle() != np.nan)
    assert np.isclose(a.x, b.x)
    assert np.isclose(a.y, b.y)
    assert a == b


@given(nfloats(), nfloats())
def test_unit_vector(x: float, y: float):
    a = Point(x, y)
    assume(abs(a) != 0)
    b = a.unit_vector()
    assert isclose(a.angle(), b.angle())
    assert isclose(abs(b), 1)


def test_unit_vector_failure():
    with pytest.raises(ZeroDivisionError):
        Point(0, 0).unit_vector()


normal_vector_data = [
    (Point(1, 0), Point(0, 1)),
    (Point(1, 1), Point(-1 / np.sqrt(2), 1 / np.sqrt(2))),
]


@pytest.mark.parametrize("a, expected", normal_vector_data)
def test_normal_vector(a, expected):
    assert a.normal() == expected


rotation_data = [
    (Point(1, 0), np.pi / 2, Point(0, 0), Point(0, 1)),
    (Point(2, 2), -np.pi, Point(2, 1), Point(2, 0)),
]


@pytest.mark.parametrize("a, angle, center, expected", rotation_data)
def test_rotation(a, angle, center, expected):
    assert abs(a.rotate(angle, center) - expected) < 1e-14


from_coordinate_lists_data = [
    ([1, 2, 3, 4], [1, 2, 3, 4], [Point(1, 1), Point(2, 2), Point(3, 3), Point(4, 4)])
]


@pytest.mark.parametrize("xs, ys, expected", from_coordinate_lists_data)
def test_from_coordinate_lists(xs: List[float], ys: List[float], expected: List[Point]):
    assert Point.from_coordinate_lists(xs, ys) == expected


@pytest.mark.parametrize("xs, ys, expected", from_coordinate_lists_data)
def test_to_coordinate_lists(xs, ys, expected):
    assert Point.to_coordinate_lists(expected) == (xs, ys)
