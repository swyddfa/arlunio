from abc import ABC, abstractmethod

import numpy as np


class ColorSpace(ABC):
    """Abstracts over the representation of colour."""

    def __repr__(self):
        name = self.__class__.__name__
        w, h = self.width, self.height

        return "ColorSpace<{0}, {1}x{2}>".format(name, w, h)

    @property
    @abstractmethod
    def width(self):
        """The width of this block of data"""
        pass

    @property
    @abstractmethod
    def height(self):
        """The height of this block of data"""
        pass

    @property
    @abstractmethod
    def bitdepth(self):
        """The bitdepth in the representation."""
        pass

    @property
    @abstractmethod
    def red(self):
        """The red color channel."""
        pass

    @property
    @abstractmethod
    def green(self):
        """The green color channel."""
        pass

    @property
    @abstractmethod
    def blue(self):
        """The blue color channel."""
        pass

    @property
    @abstractmethod
    def alpha(self):
        """The alpha color channel."""
        pass


class Mono(ColorSpace):
    """Mono color data, black/white."""

    def __init__(self, width, height, fill=False, array=None):

        if array is not None:
            self._data = array

        else:
            self._data = np.full((height, width), fill, dtype=np.bool_)

    def __and__(self, other):

        if not isinstance(other, (Mono,)):
            raise TypeError('Operation only supported between Mono instances')

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
            raise TypeError('Operation only supported between Mono instances')

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
    def fromarray(array):
        return Mono(0, 0, array=array)

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


class RGBA8(ColorSpace):
    """The RGB color space."""

    def __init__(self, width, height, fill=None):

        if fill is None:
            fill = (0, 0, 0, 255)

        self._data = np.full((height, width, 4), fill, dtype=np.uint8)

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


class RGB8(ColorSpace):
    """The RGB color space."""

    def __init__(self, width, height, fill=None):

        if fill is None:
            fill = (0, 0, 0)

        self._data = np.full((height, width, 3), fill, dtype=np.uint8)

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
