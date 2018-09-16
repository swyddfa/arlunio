import numpy as np
from abc import ABC, abstractmethod


class ColorMap(ABC):
    def __call__(self, shape):
        return self._paint(shape)

    def __rrshift__(self, shape):
        return self(shape[0])

    @abstractmethod
    def _paint(self, shape):
        pass


class FillColor(ColorMap):
    def __init__(self, color=None, background=None):

        if color is None:
            color = (0, 0, 0)

        if background is None:
            background = (255, 255, 255)

        self.color = color
        self.background = background

    def _paint(self, shape):

        height, width = shape.shape
        dimensions = (height, width, 3)

        colors = np.full(dimensions, self.background, np.uint8)
        colors[shape] = self.color

        return colors
