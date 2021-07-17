"""
Modified version of pendulum1.py:
A function draws the free body diagram, given the angle.
This function can be coupled to a numerical solver
for the motion. Videos of the motion are made.
"""

import numpy as np
import pysketcher as ps
from scipy.integrate import odeint
from pysketcher.backend.matplotlib import MatplotlibBackend

H = 8.0
W = 8.0
L = 5 * H / 7  # length


def pendulum(theta, S, mg, drag) -> ps.Composition:
    """Draw a free body animation of a pendulum.

    params:
        theta: the angle from the vertical at which the pendulum is.
        S: the force exerted toward the pivot.
        mg: the force owing to gravity.
        drag: the force acting against the motion of the pendulum.

    return: A composition of the pendulum
    """
    a = theta
    P = ps.Point(W / 2, 0.9 * H)  # rotation point

    path = ps.Arc(P, L, -ps.Angle(np.pi / 2), a)
    mass_pt = path.end
    rod = ps.Line(P, mass_pt)

    theta = ps.AngularDimension(
        r"$\theta$", P + ps.Point(0, -L / 4), P + (mass_pt - P).unit_vector * (L / 4), P
    )
    theta.extension_lines = False

    mass = ps.Circle(mass_pt, L / 30.0).set_fill_color(ps.Style.Color.BLUE)
    rod_vec = rod.end - rod.start

    length = ps.LinearDimension("$L$", mass_pt, P)
    # Displace length indication
    length = length.translate(ps.Point(-np.cos(a), -np.sin(a)) * (L / 15.0))
    length.style.line_width = 0.1
    gravity_start = ps.Point(0.8 * L, 0)
    gravity = ps.Gravity(P + gravity_start, L / 3)

    dashed_thin_black_line = ps.Style()
    dashed_thin_black_line.line_style = ps.Style.LineStyle.DASHED
    dashed_thin_black_line.line_color = ps.Style.Color.BLACK
    dashed_thin_black_line.line_width = 1.0

    path.style = dashed_thin_black_line
    vertical = ps.Line(rod.start, rod.start + ps.Point(0, -L))
    vertical.style = dashed_thin_black_line
    rod.style = dashed_thin_black_line

    comp = ps.Composition(
        {
            "body": mass,
            "rod": rod,
            "vertical": vertical,
            "theta": theta,
            "path": path,
            "g": gravity,
            # "L": length,
        }
    )

    magnitude = 1.2 * L / 6  # length of a unit force in figure
    force = mg  # constant (scaled eq: about 1)
    force *= magnitude
    mg_force = (
        ps.Force(
            "$mg$",
            mass_pt,
            mass_pt + ps.Point(0, 1) * force,
            text_position=ps.TextPosition.END,
        )
        if force != 0
        else None
    )

    force = S
    force *= magnitude
    rod_force = (
        ps.Force(
            "S",
            mass_pt,
            mass_pt - rod_vec.unit_vector * force,
            text_position=ps.TextPosition.END,
        )
        if force != 0
        else None
    )

    force = drag
    force *= magnitude
    air_force = (
        ps.Force(
            "",
            mass_pt,
            mass_pt - rod_vec.normal * force,
        )
        if force != 0
        else None
    )

    x0y0 = ps.Text("$(x_0,y_0)$", P + ps.Point(-0.4, -0.1))

    ir = ps.Force(
        r"$\mathbf{i}_r$",
        P,
        P + rod_vec.unit_vector * (L / 10),
        text_position=ps.TextPosition.END,
        # spacing=ps.Point(0.015, 0)
    )
    ith = ps.Force(
        r"$\mathbf{i}_{\theta}$",
        P,
        P + rod_vec.normal * (L / 10),
        text_position=ps.TextPosition.END,
        # spacing=ps.Point(0.02, 0.005)
    )

    body_diagram = ps.Composition(
        {
            "mg": mg_force,
            "S": rod_force,
            "air": air_force,
            "ir": ir,
            "ith": ith,
            "origin": x0y0,
        }
    )

    comp = comp.merge(body_diagram)
    return comp


def simulate_pendulum():
    """Simulate a pendulum."""

    # The second order differential equation for the angle theta
    # of a pendulum acted on by gravity with friction can be written:
    #
    # theta''(t) + b*theta'(t) + c*sin(theta(t)) = 0
    #
    # where b and c are positive constants, and a prime (‘) denotes a derivative.
    #
    # To solve this equation with `odeint`, we must first convert it to a system of
    # first order equations. By defining the angular velocity omega(t) = theta'(t),
    # we obtain the system:
    #
    # theta'(t) = omega(t)
    # omega'(t) = -b*omega(t) - c*sin(theta(t))
    #
    # so let y be the vector [theta, omega]. We implement this system in Python as:

    def pend(y, t, b, c):
        theta, omega = y
        dydt = [omega, -b * omega - c * np.sin(theta)]
        return dydt

    # Set the pendulum off at pi/6 from the vertical and stationary:
    y0 = [-np.pi / 6, 0.0]

    # give b and c some values:
    b = 0.25
    c = 5

    # generate a linear space over time for us to solve against:
    t = np.linspace(0, 10, 101)

    return odeint(pend, y0, t, args=(b, c))


def main():
    t = np.linspace(0, 10, 101)
    sol = simulate_pendulum()

    def anim_func(i: float) -> ps.Composition:
        return pendulum(ps.Angle(sol[i, 0]), 1, -1, sol[i, 1])

    fig = ps.Figure(0.0, W, 0.0, H, backend=MatplotlibBackend)
    fig.animate(anim_func, (0, 101))
    fig.save_animation("pendulum.mp4")


if __name__ == "__main__":
    main()
