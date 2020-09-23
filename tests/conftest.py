import logging

import hypothesis.strategies as hst
import numpy as np
import pytest
from hypothesis.extra.numpy import from_dtype
from hypothesis.strategies import SearchStrategy, composite

from pysketcher import Line, Point, Shape


@pytest.fixture(scope="session", autouse=True)
def do_something(request):
    hst.register_type_strategy(Shape, make_line)


@composite
def make_line(draw) -> Line:
    x1 = draw(from_dtype(np.dtype("float64")))
    y1 = draw(from_dtype(np.dtype("float64")))
    x2 = draw(from_dtype(np.dtype("float64")))
    y2 = draw(from_dtype(np.dtype("float64")))
    return Line(Point(x1, y1), Point(x2, y2))
