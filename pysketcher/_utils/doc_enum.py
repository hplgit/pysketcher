from enum import Enum
from typing import Any


class DocEnum(Enum):
    """Provides a handy way to document Enums."""

    def __new__(cls, value: Any, doc: str = None):
        """Creates an instance of a DocEnum.

        Args:
            value: The enumerate value as would be included in a normal enum.
            doc: A documentation string for the value.

        Returns:
            An instance of the DocEnum class.
        """
        self = object.__new__(cls)  # calling super().__new__(value) here would fail
        self._value_ = value
        if doc is not None:
            self.__doc__ = doc
        return self
