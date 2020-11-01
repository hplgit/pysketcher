from typing import Type, Union

from pysketcher.composition import Composition
from pysketcher.shape import Shape
from pysketcher.text import Text

Drawable: Type = Union[Shape, Text, Composition]
