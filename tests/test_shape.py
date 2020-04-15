from pysketcher import Shape
import pytest


def test_cannot_instantiate():
    with pytest.raises(TypeError):
        shape = Shape()
