from typing import List

from pytest import approx

from pysketcher import Point
import numpy as np
import numpy.testing as npt
import pytest

x_data = [
    (Point(1, 2), 1),
    (Point(2, 3), 2),
    (Point(-1, 0), -1)
]


@pytest.mark.parametrize("a, expected", x_data)
def test_x(a: Point, expected: float):
    assert a.x == expected


y_data = [
    (Point(1, 2), 2),
    (Point(2, 3), 3),
    (Point(-1, 0), 0)
]


@pytest.mark.parametrize("a, expected", y_data)
def test_y(a: Point, expected: float):
    assert a.y == expected


def test_equality():
    assert (Point(1, 2) == Point(1, 2))
    assert not (Point(1, 2) == Point(1, 3))
    assert not (Point(1, 2) == Point(2, 2))


addition_data = [
    (Point(0, 0), Point(1, 1), Point(1, 1))
]


@pytest.mark.parametrize("a,b,expected", addition_data)
def test_adding(a: Point, b: Point, expected: Point):
    assert a + b == expected


@pytest.mark.parametrize("a,b,expected", addition_data)
def test_translation(a: Point, b: Point, expected: Point):
    assert a.translate(b) == expected


subtraction_data = [
    (Point(0, 0), Point(1, 1), Point(-1, -1))
]


@pytest.mark.parametrize("a,b,expected", subtraction_data)
def test_subtraction(a: Point, b: Point, expected: Point):
    assert (a - b) == expected


multiplication_data = [
    (Point(1, 2), 2, Point(2, 4)),
    (Point(1, 2), 4, Point(4, 8))
]


@pytest.mark.parametrize("a,b,expected", multiplication_data)
def test_multiplication(a: Point, b: float, expected: Point):
    assert a * b == expected


@pytest.mark.parametrize("a,b,expected", multiplication_data)
def test_scale(a: Point, b: float, expected: Point):
    assert a.scale(b) == expected


abs_data = [
    (Point(3, 4), 5),
    (Point(1, 1), np.sqrt(2))
]


@pytest.mark.parametrize("a, expected", abs_data)
def test_abs(a: Point, expected: float):
    assert abs(a) == expected


angle_data = [
    (Point(np.sqrt(3), 1), np.pi / 6),
    (Point(1, 1), np.pi / 4)
]


@pytest.mark.parametrize("a, expected", angle_data)
def test_angle(a: Point, expected: float):
    npt.assert_allclose(a.angle(), expected, rtol=1e-14)


unit_vector_data = [
    (Point(1, 0), Point(1, 0)),
    (Point(0, 1), Point(0, 1)),
    (Point(2, 2), Point(1.0 / np.sqrt(2), 1.0 / np.sqrt(2)))
]


@pytest.mark.parametrize("a, expected", unit_vector_data)
def test_unit_vector(a: Point, expected: Point):
    assert a.unit_vector() == expected


def test_unit_vector_failure():
    with pytest.raises(ZeroDivisionError):
        Point(0, 0).unit_vector()


normal_vector_data = [
    (Point(1, 0), Point(0, 1)),
    (Point(1, 1), Point(-1/np.sqrt(2), 1/np.sqrt(2)))
]


@pytest.mark.parametrize("a, expected", normal_vector_data)
def test_normal_vector(a, expected):
    assert a.normal() == expected


rotation_data = [
    (Point(1, 0), np.pi / 2, Point(0, 0), Point(0, 1)),
    (Point(2, 2), - np.pi, Point(2, 1), Point(2, 0))
]


@pytest.mark.parametrize("a, angle, center, expected", rotation_data)
def test_rotation(a, angle, center, expected):
    assert a.rotate(angle, center).x == approx(expected.x)
    assert a.rotate(angle, center).y == approx(expected.y)


from_coordinate_lists_data = [
    ([1,2,3,4],[1,2,3,4],[Point(1,1), Point(2,2), Point(3,3), Point(4,4)])
]


@pytest.mark.parametrize("xs, ys, expected", from_coordinate_lists_data)
def test_from_coordinate_lists(xs: List[float], ys: List[float], expected: List[Point]):
    assert Point.from_coordinate_lists(xs, ys) == expected


@pytest.mark.parametrize("xs, ys, expected", from_coordinate_lists_data)
def test_to_coordinate_lists(xs, ys, expected):
    assert Point.to_coordinate_lists(expected) == (xs, ys)
