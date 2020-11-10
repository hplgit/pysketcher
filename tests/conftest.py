from typing import Type

import numpy as np
import pytest
from hypothesis.extra.numpy import from_dtype
from hypothesis.strategies import SearchStrategy, builds, floats, from_type

import pysketcher as ps
from pysketcher import Point
from pysketcher.angle import Angle
from pysketcher.backend.matplotlib import MatplotlibBackend
from tests.utils import TypeStrategy

mx = 1e30
mn = 1e-30
atol = 1e-4


@pytest.fixture(scope="session", autouse=True)
def setup_testing(request):
    np.seterr(over="warn", divide="warn")


@pytest.fixture(autouse=True)
def add_np(doctest_namespace):
    doctest_namespace["np"] = np
    doctest_namespace["ps"] = ps
    doctest_namespace["MatplotlibBackend"] = MatplotlibBackend


def isclose(a: np.float64, b: np.float64):
    return np.isclose(a, b, atol=atol)


@TypeStrategy()
def make_angle(typ: Type) -> SearchStrategy[Angle]:
    def flt(a: typ):
        if a != 0.0:
            return abs(a) > mn

    return builds(Angle, make_float(typ)).filter(flt)


@TypeStrategy()
def make_float(typ: Type) -> SearchStrategy[np.float64]:
    strategy = from_dtype(np.dtype(typ), allow_nan=False, allow_infinity=False).filter(
        lambda x: -mx < x < mx
    )
    return strategy


@TypeStrategy()
def make_point(typ: Type) -> SearchStrategy[Point]:
    def flt(a: Point) -> bool:
        retval = True
        if a.x != 0.0:
            retval = retval and a.x > mn
        if a.y != 0.0:
            retval = retval and a.y > mn
        return retval and mx > abs(a) > 0.0

    return builds(Point, make_float(np.float64), make_float(np.float64)).filter(flt)
