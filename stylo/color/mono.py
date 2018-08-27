import numpy as np

from stylo.color.colorspace import ColorSpace


class Mono(ColorSpace):
    """Mono color data, black/white."""

    def __init__(self, width, height, fill=False, array=None):

        if array is not None:
            self._data = array

        else:
            self._data = np.full((height, width), fill, dtype=np.bool_)

    def __and__(self, other):

        if not isinstance(other, (Mono,)):
            raise TypeError("Operation only supported between Mono instances")

        width_ok = self.width == other.width
        height_ok = self.height == other.height

        if not (width_ok and height_ok):
            message = "Dimensions of the two Mono instances must match!"
            raise TypeError(message)

        a = self._data
        b = other._data

        result = np.logical_and(a, b)
        return Mono.fromarray(result)

    def __or__(self, other):

        if not isinstance(other, (Mono,)):
            raise TypeError("Operation only supported between Mono instances")

        width_ok = self.width == other.width
        height_ok = self.height == other.height

        if not (width_ok and height_ok):
            message = "Dimensions of the two Mono instances must match!"
            raise TypeError(message)

        a = self._data
        b = other._data

        result = np.logical_or(a, b)
        return Mono.fromarray(result)

    def __neg__(self):

        result = np.logical_not(self._data)
        return Mono.fromarray(result)

    @staticmethod
    def parse(color):
        pass

    @staticmethod
    def fromarray(array):
        return Mono(0, 0, array=array)

    @property
    def data(self):
        return self._data

    @property
    def width(self):
        """The width of this block of data"""
        return self._data.shape[1]

    @property
    def height(self):
        """The height of this block of data"""
        return self._data.shape[0]

    @property
    def bitdepth(self):
        """The bitdepth in the representation."""
        return 1

    @property
    def red(self):
        """The red color channel."""
        return self._data[:, :]

    @property
    def green(self):
        """The green color channel."""
        return self._data[:, :]

    @property
    def blue(self):
        """The blue color channel."""
        return self._data[:, :]

    @property
    def alpha(self):
        """The alpha color channel."""
        return np.full((self.height, self.width), True, dtype=np.bool_)

    def as_rgb8(self):

        rgb8 = np.full((self.height, self.width, 3), (255, 255, 255), dtype=np.uint8)

        # All the true values are now black
        rgb8[self._data] = (0, 0, 0)
        return rgb8
