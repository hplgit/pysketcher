"""Provides a means to annotate shapes.

Annotations are text objects which are positioned using the dimensions
of a provide shape.
"""

from pysketcher.annotation._arc_annotation import ArcAnnotation
from pysketcher.annotation._line_annotation import LineAnnotation
from pysketcher.annotation._text_position import TextPosition

__all__ = ["ArcAnnotation", "LineAnnotation", "TextPosition"]
