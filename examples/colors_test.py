import logging

import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend

logging.basicConfig(level=logging.INFO)


def main() -> None:
    i = 1
    shapes = {}
    for line_color in ps.Style.Color:
        j = 1
        for fill_color in ps.Style.Color:
            logging.info("Line Color: %s", line_color)
            name: str = "Rectangle.%d.%d" % (i, j)
            rectangle = ps.Rectangle(ps.Point(i, j), 1, 1)
            rectangle.style.line_width = 3.0
            rectangle.style.line_color = line_color
            rectangle.style.fill_color = fill_color
            shapes[name] = rectangle
            j = j + 1
        i = i + 1

    model = ps.Composition(shapes)

    fig = ps.Figure(0, 12, 0, 12, backend=MatplotlibBackend)
    fig.add(model)
    fig.show()


if __name__ == "__main__":
    main()
