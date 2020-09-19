"""
Modified version of pendulum1.py:
A function draws the free body diagram, given the angle.
This function can be coupled to a numerical solver
for the motion. Videos of the motion are made.
"""
from pysketcher import *

H = 15.0
W = 17.0

drawing_tool._set_coordinate_system(xmin=0, xmax=W, ymin=0, ymax=H, axis=False)


def pendulum(theta, S, mg, drag, t, time_level):

    drawing_tool.set_linecolor("blue")
    import math

    a = math.degrees(theta[time_level])
    L = 0.4 * H  # length
    P = (W / 2, 0.8 * H)  # rotation point

    vertical = Line(P, P - point(0, L))
    path = Arc(P, L, -90, a)
    angle = Arc_wText(r"$\theta$", P, L / 4, -90, a, text_spacing=1 / 30.0)

    mass_pt = path.geometric_features()["end"]
    rod = Line(P, mass_pt)

    mass = Circle(center=mass_pt, radius=L / 20.0)
    mass.set_filled_curves(color="blue")
    rod_vec = rod.geometric_features()["end"] - rod.geometric_features()["start"]
    unit_rod_vec = unit_vec(rod_vec)
    mass_symbol = Text("$m$", mass_pt + L / 10 * unit_rod_vec)

    length = DistanceWithText(P, mass_pt, "$L$")
    # Displace length indication
    length.translate(L / 15 * point(cos(radians(a)), sin(radians(a))))
    gravity = Gravity(start=P + point(0.8 * L, 0), length=L / 3)

    def set_dashed_thin_blackline(*objects):
        """Set linestyle of objects to dashed, black, width=1."""
        for obj in objects:
            obj.set_linestyle("dashed")
            obj.set_linecolor("black")
            obj.set_linewidth(1)

    set_dashed_thin_blackline(vertical, path)

    fig = Composition(
        {
            "body": mass,
            "rod": rod,
            "vertical": vertical,
            "theta": angle,
            "path": path,
            "g": gravity,
            "L": length,
        }
    )

    # fig.draw()
    # drawing_tool.display()
    # drawing_tool.savefig('tmp_pendulum1')

    drawing_tool.set_linecolor("black")

    rod_start = rod.geometric_features()["start"]  # Point P
    vertical2 = Line(rod_start, rod_start + point(0, -L / 3))
    set_dashed_thin_blackline(vertical2)
    set_dashed_thin_blackline(rod)
    angle2 = Arc_wText(r"$\theta$", rod_start, L / 6, -90, a, text_spacing=1 / 30.0)

    magnitude = 1.2 * L / 2  # length of a unit force in figure
    force = mg[time_level]  # constant (scaled eq: about 1)
    force *= magnitude
    mg_force = Force(mass_pt, mass_pt + force * point(0, -1), "", text_pos="end")
    force = S[time_level]
    force *= magnitude
    rod_force = Force(
        mass_pt,
        mass_pt - force * unit_vec(rod_vec),
        "",
        text_pos="end",
        text_spacing=(0.03, 0.01),
    )
    force = drag[time_level]
    force *= magnitude
    # print('drag(%g)=%g' % (t, drag[time_level]))
    air_force = Force(
        mass_pt,
        mass_pt - force * unit_vec((rod_vec[1], -rod_vec[0])),
        "",
        text_pos="end",
        text_spacing=(0.04, 0.005),
    )

    body_diagram = Composition(
        {
            "mg": mg_force,
            "S": rod_force,
            "air": air_force,
            "rod": rod,
            "vertical": vertical2,
            "theta": angle2,
            "body": mass,
        }
    )

    x0y0 = Text("$(x_0,y_0)$", P + point(-0.4, -0.1))
    ir = Force(
        P,
        P + L / 10 * unit_vec(rod_vec),
        r"$\boldsymbol{i}_r$",
        text_pos="end",
        text_spacing=(0.015, 0),
    )
    ith = Force(
        P,
        P + L / 10 * unit_vec((-rod_vec[1], rod_vec[0])),
        r"$\boldsymbol{i}_{\theta}$",
        text_pos="end",
        text_spacing=(0.02, 0.005),
    )

    # body_diagram['ir'] = ir
    # body_diagram['ith'] = ith
    # body_diagram['origin'] = x0y0

    drawing_tool.erase()
    body_diagram.draw(verbose=0)
    # drawing_tool.display('Free body diagram')
    drawing_tool.savefig("tmp_%04d.png" % time_level, crop=False)
    # No cropping: otherwise movies will be very strange


def simulate_pendulum(alpha, theta0, dt, T):
    import odespy

    def f(u, t, alpha):
        omega, theta = u
        return [-alpha * omega * abs(omega) - sin(theta), omega]

    import numpy as np

    Nt = int(round(T / float(dt)))
    t = np.linspace(0, Nt * dt, Nt + 1)
    solver = odespy.RK4(f, f_args=[alpha])
    solver.set_initial_condition([0, theta0])
    u, t = solver.solve(t, terminate=lambda u, t, n: abs(u[n, 1]) < 1e-3)
    omega = u[:, 0]
    theta = u[:, 1]
    S = omega ** 2 + np.cos(theta)
    drag = -alpha * np.abs(omega) * omega
    return t, theta, omega, S, drag


def animate():
    # Clean up old plot files
    import os, glob

    for filename in glob.glob("tmp_*.png") + glob.glob("movie.*"):
        os.remove(filename)
    # Solve problem
    from math import pi, radians, degrees
    import numpy as np

    alpha = 0.4
    period = 2 * pi
    T = 12 * period
    dt = period / 40
    a = 70
    theta0 = radians(a)
    t, theta, omega, S, drag = simulate_pendulum(alpha, theta0, dt, T)
    mg = np.ones(S.size)
    # Visualize drag force 5 times as large
    drag *= 5
    print("NOTE: drag force magnified 5 times!!")

    # Draw animation
    import time

    for time_level, t_ in enumerate(t):
        pendulum(theta, S, mg, drag, t_, time_level)
        time.sleep(0.2)

    # Make videos
    prog = "ffmpeg"
    filename = "tmp_%04d.png"
    fps = 6
    codecs = {"flv": "flv", "mp4": "libx264", "webm": "libvpx", "ogg": "libtheora"}
    for ext in codecs:
        lib = codecs[ext]
        cmd = "%(prog)s -i %(filename)s -r %(fps)s " % vars()
        cmd += "-vcodec %(lib)s movie.%(ext)s" % vars()
        print(cmd)
        os.system(cmd)


if __name__ == "__main__":
    animate()
