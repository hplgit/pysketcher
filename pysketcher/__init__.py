"""Tool for creating sketches of physical and mathematical problems in Python code."""
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    pass

from pysketcher._angle import Angle
from pysketcher._arc import Arc, ArcWithText
from pysketcher._arrow import Arrow, DoubleArrow
from pysketcher._arrow_with_text import ArrowWithText
from pysketcher._axis import Axis
from pysketcher._circle import Circle
from pysketcher._cubic_bezier_curve import CubicBezier
from pysketcher._curve import Curve
from pysketcher._dashpot import Dashpot
from pysketcher._distance_with_text import DistanceWithText
from pysketcher._drawable import Drawable
from pysketcher._figure import Figure
from pysketcher._force import Force, Gravity
from pysketcher._line import Line
from pysketcher._moment import Moment
from pysketcher._point import Point
from pysketcher._rectangle import Rectangle
from pysketcher._shape import Shape
from pysketcher._simple_support import SimpleSupport
from pysketcher._sketchy_func import (
    SketchyFunc1,
    SketchyFunc2,
    SketchyFunc3,
    SketchyFunc4,
)
from pysketcher._spline import Spline
from pysketcher._spring import Spring
from pysketcher._style import Style, TextStyle
from pysketcher._text import Text
from pysketcher._triangle import Triangle
from pysketcher._uniform_load import UniformLoad
from pysketcher._velocity_profile import VelocityProfile
from pysketcher._wall import Wall
from pysketcher._wheel import Wheel
from pysketcher.composition import Composition, ShapeWithText

__all__ = [
    "Angle",
    "Arc",
    "ArcWithText",
    "Arrow",
    "DoubleArrow",
    "ArrowWithText",
    "Axis",
    "SimpleSupport",
    "Circle",
    "CubicBezier",
    "Composition",
    "ShapeWithText",
    "Curve",
    "Dashpot",
    "DistanceWithText",
    "Drawable",
    "Figure",
    "Force",
    "Gravity",
    "Line",
    "Moment",
    "Point",
    "Rectangle",
    "Shape",
    "SketchyFunc1",
    "SketchyFunc2",
    "SketchyFunc3",
    "SketchyFunc4",
    "Spline",
    "Spring",
    "Style",
    "TextStyle",
    "Text",
    "Triangle",
    "UniformLoad",
    "VelocityProfile",
    "Wall",
    "Wheel",
]
