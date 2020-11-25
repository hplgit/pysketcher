from typing import Type, Union

from pysketcher._shape import Shape
from pysketcher._text import Text
from pysketcher.composition._composition import Composition

Drawable: Type = Union[Shape, Text, Composition]
