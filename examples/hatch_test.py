import logging

import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend


def main() -> None:
    i = 1
    shapes_dict = {}
    for fill_pattern in ps.Style.FillPattern:
        logging.info("Fill Pattern: %s", fill_pattern)
        name: str = "Rectangle.%d" % i
        rectangle = ps.Rectangle(ps.Point(i, 1), 1, 1).set_fill_pattern(fill_pattern)
        shapes_dict[name] = rectangle
        i = i + 1.5

    shapes = ps.Composition(shapes_dict)

    fig = ps.Figure(0.0, 20.0, 0.0, 3.0, backend=MatplotlibBackend)
    fig.add(shapes)
    fig.show()


if __name__ == "__main__":
    main()
