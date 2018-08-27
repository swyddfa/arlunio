import numpy as np

from stylo.color.mono import Mono
from stylo.image.image import Image


class BitMask(Image):
    """A black/white image."""

    def __init__(self, width, height, color=None):

        if color is not None:

            if not isinstance(color, (Mono,)):
                raise TypeError("Argument mask: Expected Mono instance")

            self.color = color
            return

        self.color = Mono(width, height)

    def __and__(self, other):
        return self._logical_op(other, np.logical_and, "AND")

    def __or__(self, other):
        return self._logical_op(other, np.logical_or, "OR")

    def __xor__(self, other):
        return self._logical_op(other, np.logical_xor, "XOR")

    def _logical_op(self, other, operation, operation_name):

        if not isinstance(other, (BitMask,)):
            message = "Bitmasks can only be {}ed with other Bitmasks"
            raise TypeError(message.format(operation_name))

        if (self.width != other.width) or (self.height != other.height):
            raise ValueError("Bitmasks must be the same size")

        mask = self.color.data
        other_mask = other.color.data

        new_mask = operation(mask, other_mask)
        return BitMask.frommask(new_mask)

    @classmethod
    def frommask(cls, mask):
        return cls(0, 0, Mono.fromarray(mask))

    def draw(self, shape):
        pass
