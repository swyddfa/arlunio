import re
import struct
import numpy as np

from stylo.color.colorspace import ColorSpace


rgba_pattern = re.compile("\A[a-fA-F0-9]{8}\Z")


class RGBA8(ColorSpace):
    """The RGB color space."""

    def __init__(self, width, height, fill=None):

        if fill is None:
            fill = RGBA8.parse("000000ff")

        self._data = np.full((height, width, 4), fill, dtype=np.uint8)

    @staticmethod
    def parse(color):

        if rgba_pattern.match(color):
            return struct.unpack("BBBB", bytes.fromhex(color))

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
        return self._data[:, :, 3]

    def as_rgb8(self):
        return self._data
