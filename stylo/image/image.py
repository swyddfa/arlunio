from abc import ABC, abstractmethod
import PIL as P
import matplotlib.pyplot as plt

from stylo.drawable.drawable import Drawable
from stylo.color.colorspace import ColorSpace


class Image(ABC):
    """The next generation of stylo imaging."""

    def __call__(self, drawable):

        if not isinstance(drawable, (Drawable,)):
            raise TypeError("Expected drawable instance.")

        self.draw(drawable)

    @abstractmethod
    def draw(self, drawable):
        """Take a drawable and convert it to pixels."""
        pass

    @property
    def width(self):
        return self.color.width

    @property
    def height(self):
        return self.color.height

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):

        if not isinstance(value, (ColorSpace,)):
            raise TypeError("Property color: expected Colorspace instance")

        self._color = value

    def show(self):
        return plt.imshow(self.color.as_rgb8())

    def save(self, filename):
        pixels = self.color.as_rgb8()
        width = self.color.width
        height = self.color.height

        image = P.Image.frombuffer("RGB", (width, height), pixels, "raw", "RGB", 0, 1)

        with open(filename, "wb") as f:
            image.save(f)
