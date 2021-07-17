from pysketcher._arc import Arc
from pysketcher._text import Text
from pysketcher.annotation._text_position import TextPosition


class ArcAnnotation(Text):
    """Annotates an arc with the provided text."""

    # TODO: write an example for ArcAnnotation
    _DEFAULT_OFFSET = 0.25

    def __init__(
        self, text: str, arc: Arc, text_position: TextPosition = TextPosition.MIDDLE
    ):
        self._arc = arc
        self._offset = self._DEFAULT_OFFSET
        radial = (arc.center - arc.mid).unit_vector
        text_pos = arc.mid - (radial * self._offset)
        super().__init__(text, text_pos)
