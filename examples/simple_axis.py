import logging

import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend

logging.basicConfig(level=logging.INFO)


def main():
    code = ps.Axis(ps.Point(1, 1), 3, "x")
    code2 = ps.Axis(ps.Point(1, 1), 3, "y")
    model = ps.Composition(dict(x=code, y=code2))

    fig = ps.Figure(0, 5, 0, 5, backend=MatplotlibBackend)
    fig.add(model)
    fig.show()


if __name__ == "__main__":
    main()
