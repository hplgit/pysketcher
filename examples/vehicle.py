from pysketcher import MatplotlibDraw, Circle, Rectangle, Point, Wall, Composition, Style


R = 1    # radius of wheel
L = 4    # distance between wheels
H = 2    # height of vehicle body
w_1 = 5  # position of front wheel
drawing_tool = MatplotlibDraw(0, w_1 + 2*L + 3*R, -1, 2*R + 3*H)

wheel1 = Circle(Point(w_1, R), R).set_fill_color(Style.Color.BLUE).set_line_width(6)
wheel2 = wheel1.translate(Point(L, 0))
under = Rectangle(Point(w_1-2*R, 2*R),2*R + L + 2*R, H)
under.style.fill_color = Style.Color.RED
under.style.line_color = Style.Color.RED
over = Rectangle(Point(w_1, 2*R + H), 2.5*R, 1.25*H).set_fill_color(Style.Color.WHITE)
over.style.line_width = 14
over.style.line_color = Style.Color.RED
over.style.fill_pattern = Style.FillPattern.UP_RIGHT_TO_LEFT

ground = Wall([Point(w_1 - L,0), Point(w_1 + 3*L, 0)], -0.3*R)
ground.style.fill_pattern = Style.FillPattern.UP_LEFT_TO_RIGHT

figure = Composition({
    "wheel1": wheel1,
    "wheel2": wheel2,
    "under": under,
    "over": over,
    "ground": ground
})

figure.draw(drawing_tool)
drawing_tool.display()
