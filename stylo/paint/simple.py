from stylo.color.mono import Mono
from stylo.paint.painter import Painter


class SimplePainter(Painter):
    """As simple as they come, all this painter does is convert a single
    bitmask into a black and white image.
    """

    def __init__(self, bitmask):
        self.bitmask = bitmask

    def paint(self):
        return Mono.fromarray(self.bitmask)
