from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    pass

from pysketcher.angle import Angle
from pysketcher.arc import Arc, ArcWithText
from pysketcher.arrow import Arrow, DoubleArrow
from pysketcher.arrow_with_text import ArrowWithText
from pysketcher.axis import Axis
from pysketcher.beam import SimpleSupport
from pysketcher.circle import Circle
from pysketcher.composition import Composition, ShapeWithText
from pysketcher.curve import Curve
from pysketcher.dashpot import Dashpot
from pysketcher.distance_with_text import DistanceWithText
from pysketcher.drawable import Drawable
from pysketcher.figure import Figure
from pysketcher.force import Force, Gravity
from pysketcher.line import Line
from pysketcher.moment import Moment
from pysketcher.point import Point
from pysketcher.rectangle import Rectangle
from pysketcher.shape import Shape
from pysketcher.sketchy_func import (
    SketchyFunc1,
    SketchyFunc2,
    SketchyFunc3,
    SketchyFunc4,
)
from pysketcher.spline import Spline
from pysketcher.spring import Spring
from pysketcher.style import Style, TextStyle
from pysketcher.text import Text
from pysketcher.triangle import Triangle
from pysketcher.uniform_load import UniformLoad
from pysketcher.velocity_profile import VelocityProfile
from pysketcher.wall import Wall
from pysketcher.wheel import Wheel
