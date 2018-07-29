import re
import struct
import numpy as np

from stylo.color.colorspace import ColorSpace


rgb_pattern = re.compile("\A[a-fA-F0-9]{6}\Z")


class RGB8(ColorSpace):
    """The RGB color space."""

    def __init__(self, width, height, fill=None):

        if fill is None:
            fill = RGB8.parse("000000")

        self._data = np.full((height, width, 3), fill, dtype=np.uint8)

    @staticmethod
    def parse(color):

        if rgb_pattern.match(color):
            return struct.unpack("BBB", bytes.fromhex(color))

    @property
    def data(self):
        return self._data

    @property
    def bitdepth(self):
        return 8

    @property
    def width(self):
        return self._data.shape[1]

    @property
    def height(self):
        return self._data.shape[0]

    @property
    def red(self):
        return self._data[:, :, 0]

    @property
    def green(self):
        return self._data[:, :, 1]

    @property
    def blue(self):
        return self._data[:, :, 2]

    @property
    def alpha(self):
        return np.full((self.height, self.width), 255, dtype=np.uint8)

    def as_rgb8(self):
        return self._data[:, :, 0:2]