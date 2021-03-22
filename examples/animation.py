"""A very simple animation."""
import numpy as np

from pysketcher import Angle, Circle, Figure, Line, Point
from pysketcher.backend.matplotlib import MatplotlibBackend
from pysketcher.composition import Composition


def main():
    circle = Circle(Point(0, 0), 1)
    line = Line(Point(0, 0), Point(0, 1))

    def func(frame: int):
        new_line = line.rotate(Angle(2 * np.pi * frame / 360), Point(0, 0))
        model = Composition({"circle": circle, "line": new_line})
        return model

    fig = Figure(-1.2, 1.2, -1.2, 1.2, backend=MatplotlibBackend)
    fig.animate(func, (0, 360))
    fig.save_animation("animation.mp4")


if __name__ == "__main__":
    main()
