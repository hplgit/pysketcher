import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend
from pysketcher.dimension import LinearDimension


def main() -> None:
    rect = ps.Rectangle(ps.Point(1, 1), 4, 6)

    dim_w = LinearDimension(r"$w$", rect.lower_left, rect.lower_right)
    dim_h = LinearDimension(r"$h$", rect.lower_right, rect.upper_right)

    fig = ps.Figure(0, 8, 0, 8, backend=MatplotlibBackend)
    fig.add(rect)
    fig.add(dim_w)
    fig.add(dim_h)
    fig.show()


if __name__ == "__main__":
    main()
