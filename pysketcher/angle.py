import logging

import numpy as np


class Angle(np.float64):
    def __new__(cls, value: np.float64) -> "Angle":
        """A representation of a 2-Dimensional Angle

        Args:
            value: The value of the angle to create.

        Example:
            >>> Angle(1.0)
            Angle(1.0)
            >>> Angle(np.pi / 2)
            Angle(1.5707963267948966)
            >>> Angle(123)
            Angle(-2.6637061435917175)
            >>> Angle(2*np.pi)
            Angle(0.0)
        """
        value = cls._normalize(value)
        return super(cls, cls).__new__(cls, value)

    @staticmethod
    def _normalize(value: np.float64):
        logging.debug(f"Initial value: {value}")

        def order(x: np.float) -> np.float:
            return np.trunc(x / (2 * np.pi))

        if not (-np.pi < value <= np.pi):
            order_value = order(value)
            # logging.debug(f"Scaling by a factor of {order_value}")
            value = value - order_value * 2 * np.pi
            # logging.debug(f"Value after initial scaling: {value}")
            # TODO: for some reason, ``order`` sometimes overshoots. Need to fix this.
            while value <= -np.pi:
                # logging.debug("Nudging up")
                value = value + 2 * np.pi
            while value > np.pi:
                # logging.debug("Nudging down")
                value = value - 2 * np.pi
        # logging.debug(f"Final value: {value}")
        return value

    def __add__(self, other: np.float64) -> "Angle":
        res = super(self.__class__, self).__add__(other)
        return self.__class__(res)

    def __sub__(self, other: np.float64) -> "Angle":
        res = super(self.__class__, self).__sub__(other)
        return self.__class__(res)

    def __mul__(self, other: np.float64) -> "Angle":
        res = super(self.__class__, self).__mul__(other)
        return self.__class__(res)

    def __truediv__(self, other: np.float64) -> "Angle":
        res = super(self.__class__, self).__truediv__(other)
        return self.__class__(res)

    def __str__(self: np.float64) -> str:
        return f"{float(self)}"

    def __repr__(self: np.float64) -> str:
        return f"Angle({float(self)})"
