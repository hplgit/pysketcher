from abc import ABC, abstractmethod
from typing import List

from .point import Point
from .style import Style, TextStyle


class DrawingTool(ABC):
    @abstractmethod
    def text(
        self,
        text: str,
        position: Point,
        direction: Point = Point(1, 0),
        style: TextStyle = TextStyle(),
    ):
        pass

    @abstractmethod
    def plot_curve(self, points: List[Point], style: Style):
        pass

    @abstractmethod
    def erase(self):
        pass
