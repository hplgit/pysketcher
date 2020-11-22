from typing import List, Type

from pysketcher._drawable import Drawable
from pysketcher.backend.backend import Backend


class Figure:
    """Provides the developer interface to the pysketcher backends.

    Provides the means to render models into either viewable, or
    savable (or both) images depending on which backend is chosen.

    Args:
        x_min: The minimum x-coordinate that will be rendered.
        x_max: The maximum x-coordinate that will be rendered.
        y_min: The minimum y-coordinate that will be rendered.
        y_max: The maximum y-coordinate that will be rendered.

    Examples:
        >>> circle = ps.Circle(ps.Point(1.5, 1.5), 1)
        >>> fig = ps.Figure(0, 3, 0, 3, backend=MatplotlibBackend)
        >>> fig.add(circle)
        >>> fig.save("pysketcher/images/figure.png")

        .. figure:: images/figure.png
            :alt: An example of the use of a Figure.
            :figclass: align-center

            An example of ``Figure``.
    """

    _shapes: List[Drawable]
    _backend: Backend

    def __init__(
        self,
        x_min: float,
        x_max: float,
        y_min: float,
        y_max: float,
        backend: Type[Backend],
    ):
        self._backend = backend(x_min, x_max, y_min, y_max)
        self._shapes = []

    def add(self, shape: Drawable) -> None:
        """Adds a shape to the Figure.

        Once the shape is added, when :method:``save`` or :method:``show`` is
        called, the portion of the shape which is within the bounds of the figure
        will be included in the image.

        Args:
            shape: The shape which should be added to the figure.

        """
        self._shapes.append(shape)
        self._backend.add(shape)

    def show(self):
        """Shows an interactive view of the figure.

        If the backend supports it, then an interactive figure will be shown in a
        UI window.
        """
        self._backend.show()

    def save(self, filename: str) -> None:
        """Saves the rendered figure to a file.

        If the backed supports it, then an image will be saved to the location
        specified in ``filename``.

        Args:
            filename: The location to which the figure should be saved.
        """
        self._backend.save(filename)

    def erase(self):
        """Removes all the shapes from the figure."""
        self._backend.erase()

    # def animate(
    #     self,
    #     drawing_tool: DrawingTool,
    #     time_points: List[float],
    #     action: Callable[["Shape", float, float], "Shape"],
    #     pause_per_frame: float = 0.5,
    #     dt: float = 0.5,
    #     title=None,
    # ):
    #
    #     for n, t in enumerate(time_points):
    #         drawing_tool.erase()
    #
    #         fig: Shape = action(self, t, dt)
    #         fig.draw(drawing_tool)
