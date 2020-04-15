from pysketcher import Point


def test_equality():
    assert (Point(1, 2) == Point(1, 2))
    assert not (Point(1, 2) == Point(1, 3))
    assert not (Point(1, 2) == Point(2, 2))


def test_adding():
    under_test: Point = Point(3, 4)

    assert (under_test + Point(1, 1)) == Point(4, 5)
