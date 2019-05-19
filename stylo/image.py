import base64
import io

import numpy as np
import PIL.Image

from .color import RGB8

try:
    import matplotlib.pyplot as plt

    MATPLOTLIB = True
except ImportError:
    MATPLOTLIB = False


class MissingDependencyError(ImportError):
    """Raised when a dependency is missing."""

    def __init__(self, missing):

        if isinstance(missing, (list, tuple)):
            missing = ", ".join(missing)

        message = f"Missing required dependencies: {missing}"
        super().__init__(message)


class Image:
    """An image is a container for raw pixel data."""

    def __init__(self, pixels):
        self.pixels = pixels

    def __repr__(self):
        y, x, _ = self.pixels.shape
        return f"Image<{x} x {y}>"

    def __getitem__(self, key):
        return Image(pixels[key])

    def __setitem__(self, key, value):
        self.pixels[key] = value

    @classmethod
    def new(cls, width, height, background=None, colorspace=None):

        if background is None:
            background = "ffffff"

        if colorspace is None:
            colorspace = RGB8

        bg_color = colorspace.parse(background)

        pixels = np.full((height, width, 3), bg_color)
        return cls(pixels)

    def show(self):

        if not MATPLOTLIB:
            raise MissingDependencyError("matplotlib")

        fig, ax = plt.subplots(1)
        fig.axes[0].get_yaxis().set_visible(False)
        fig.axes[0].get_xaxis().set_visible(False)

        ax.imshow(self.pixels)
        return ax

    def _as_pillow_image(self):
        height, width, _ = self.pixels.shape

        return PIL.Image.frombuffer(
            "RGB", (width, height), self.pixels, "raw", "RGB", 0, 1
        )

    def save(self, filename):

        image = self._as_pillow_image()

        with open(filename, "wb") as f:
            image.save(f)

    def encode(self):
        image = self._as_pillow_image()

        with io.BytesIO() as byte_stream:
            image.save(byte_stream, "PNG")
            image_bytes = byte_stream.getvalue()

        return base64.b64encode(image_bytes)


class Region:
    """A region, is something we can draw and produce an image from."""

    def __init__(self, u=-0, v=0, r=0, domain=None, mask=None, color=None):
        self.u = u
        self.v = v
        self.r = r

        self.domain = domain
        self.mask = mask
        self.color = color

    def __call__(self, width, height):

        domain = self.domain(width, height)
        mask = self.mask(**domain)
        pixels = self.color(mask)

        return Image(pixels)

    @property
    def domain(self):
        pass

    @domain.setter
    def domain(self, value):
        self._domain = value

    @property
    def mask(self):
        pass

    @mask.setter
    def mask(self, value):
        self._mask = value

    @property
    def color(self):
        pass

    @color.setter
    def color(self, value):
        self._color = value


class Canvas:
    """A good canvas is what every artist needs."""

    def __call__(self, width, height):
        return Image.new(width, height)
