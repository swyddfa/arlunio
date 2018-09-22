from abc import ABC, abstractmethod

from stylo.color.colorspaces import ColorSpace, RGB8


class ColorMap(ABC):
    def __init__(self, colorspace=None):

        if colorspace is None:
            colorspace = RGB8

        self.colorspace = colorspace

    def __call__(self, shape, image_data=None):
        return self._paint(shape, image_data)

    def _parse_color(self, color):
        return self.colorspace.parse(color)

    @abstractmethod
    def _paint(self, shape, image_data):
        pass

    @property
    def colorspace(self):
        return self._colorspace

    @colorspace.setter
    def colorspace(self, value):

        if not issubclass(value, (ColorSpace,)):
            raise TypeError("Expected ColorSpace")

        self._colorspace = value
