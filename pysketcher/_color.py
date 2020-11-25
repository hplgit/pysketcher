from enum import auto, Enum, unique


@unique
class Color(Enum):
    """A set of colors supported across all backends."""

    RED = auto()
    GREEN = auto()
    BLUE = auto()
    CYAN = auto()
    MAGENTA = auto()
    YELLOW = auto()
    WHITE = auto()
    BLACK = auto()
