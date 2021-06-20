import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend

W = 10.0
H = 5.0
a = [0, 3.5, 5]


def main() -> None:
    fig = ps.Figure(-1, W + 1, -1, H + 1, backend=MatplotlibBackend)

    layers = {
        "layer%d" % i: ps.Line(ps.Point(0, a[i]), ps.Point(W, a[i]))
        for i in range(len(a))
    }
    symbols_q = {
        "xi_%d" % i: ps.Text(r"$\xi_%d$" % i, ps.Point(W / 2, 0.5 * (a[i] + a[i + 1])))
        for i in range(len(a) - 1)
    }
    symbols_q["xi_2"] = ps.Text(r"$\xi_2$", ps.Point(-0.5, a[1]))

    sides = {
        "left": ps.Line(ps.Point(0, 0), ps.Point(0, H)),
        "right": ps.Line(ps.Point(W, 0), ps.Point(W, H)),
    }
    d = sides.copy()
    d.update(layers)
    d.update(symbols_q)
    model = ps.Composition(d)

    fig.add(model)
    fig.show()


if __name__ == "__main__":
    main()
