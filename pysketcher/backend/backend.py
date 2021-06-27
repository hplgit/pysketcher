from abc import ABC, abstractmethod
from typing import Callable, Tuple, Union

from pysketcher._drawable import Drawable


class Backend(ABC):
    pass

    @abstractmethod
    def add(self, shape: Drawable) -> None:
        pass

    @abstractmethod
    def erase(self) -> None:
        pass

    @abstractmethod
    def show(self) -> None:
        pass

    @abstractmethod
    def save(self, filename: str) -> None:
        pass

    def animate(
        self,
        func: Callable[[float], Drawable],
        interval: Union[Tuple[float, float], Tuple[float, float, float]],
    ):
        raise NotImplementedError("This backend doesn't implement animation.")

    def save_animation(self, filename: str):
        raise NotImplementedError("This backend doesn't implement animation.")
