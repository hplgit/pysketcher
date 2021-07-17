from enum import auto, Enum, unique


@unique
class TextPosition(Enum):
    """Specifies the position of text in Annotations."""

    START = auto()
    MIDDLE = auto()
    END = auto()
