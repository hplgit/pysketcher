from typing import Type

import numpy as np
import pytest
from hypothesis.extra.numpy import from_dtype
from hypothesis.strategies import SearchStrategy, builds, floats, from_type

import pysketcher as ps
from pysketcher.angle import Angle
from pysketcher.backend.matplotlib import MatplotlibBackend
from tests.utils import TypeStrategy

mx = 1e12
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
    return builds(Angle, make_float(typ))


@TypeStrategy()
def make_float(typ: Type) -> SearchStrategy[np.float64]:
    strategy = from_dtype(np.dtype(typ), allow_nan=False, allow_infinity=False).filter(
        lambda x: -mx < x < mx
    )
    return strategy
