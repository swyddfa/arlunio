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

    def __init__(self, pixels, mask=None):
        self.pixels = pixels
        self._mask = mask

    def __repr__(self):
        y, x, _ = self.pixels.shape
        return f"Image<{x} x {y}>"

    def __getitem__(self, key):
        return Image(self.pixels[key])

    def __setitem__(self, key, value):
        self.pixels[key] = value

    @property
    def mask(self):

        if self._mask is None:
            return tuple([slice(None, None, None) for _ in range(3)])

        return self._mask

    @mask.setter
    def mask(self, value):
        self._mask = value

    @classmethod
    def new(cls, width, height, background=None, colorspace=None):

        if background is None:
            background = "ffffff"

        if colorspace is None:
            colorspace = RGB8

        bg_color = colorspace.parse(background)

        pixels = np.full((height, width, 3), bg_color, dtype=np.uint8)
        return cls(pixels)

    def show(self, figsize=None):

        if not MATPLOTLIB:
            raise MissingDependencyError("matplotlib")

        if figsize is None:
            figsize = (12, 12)

        fig, ax = plt.subplots(1, figsize=figsize)
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
