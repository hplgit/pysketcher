import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend

W = 10.0
H = 10.0

a = [0, 1.5, 3, 4.5, 6, 8.2, 10]


def main():
    layers = {
        "layer%d" % i: ps.Line(ps.Point(0, a[i]), ps.Point(W, a[i]))
        for i in range(len(a))
    }

    symbols_ell = {
        "l_%d" % i: ps.Text(r"$\ell_%d$" % i, ps.Point(-0.5, a[i]))
        for i in range(1, len(a) - 1)
    }

    for text in symbols_ell.values():
        text.style.font_size = 24

    symbols_a = {
        "a_%d" % i: ps.Text("$a_%d$" % i, ps.Point(W / 2, 0.5 * (a[i] + a[i + 1])))
        for i in range(len(a) - 1)
    }

    for text in symbols_a.values():
        text.style.font_size = 24

    sides = {
        "left": ps.Line(ps.Point(0, 0), ps.Point(0, H)),
        "right": ps.Line(ps.Point(W, 0), ps.Point(W, H)),
    }
    d = sides.copy()
    d.update(layers)
    d.update(symbols_ell)
    d.update(symbols_a)
    model = ps.Composition(d)

    fig = ps.Figure(-1, W + 1, -1, H + 1, backend=MatplotlibBackend)
    fig.add(model)
    fig.show()


if __name__ == "__main__":
    main()
