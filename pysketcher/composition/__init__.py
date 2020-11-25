"""Provides a means to group primitive shapes.

Primitives can be combined together to form reusable
groups which can then be transformed. This module also
provides a set of pre-baked primitives for convenience.
"""

from pysketcher.composition._composition import Composition, ShapeWithText

__all__ = ["Composition", "ShapeWithText"]
