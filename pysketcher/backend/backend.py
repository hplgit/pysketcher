from abc import ABC, abstractmethod

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
