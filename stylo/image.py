import base64
import io
import logging
import string

import numpy as np
import PIL.Image

from .color import RGB8

logger = logging.getLogger(__name__)


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

    def _repr_html_(self):

        data = self.encode().decode("utf-8")
        html = """\
            <style>
              .stylo-image {
                  width: 50%;
                  margin: auto;
                  image-rendering: crisp-edges;
                  border: solid 1px #ddd;
              }
            </style>
            <img class="stylo-image" src="data:image/png;base64,$data"></img>
        """
        template = string.Template(html)

        return template.safe_substitute({"data": data})

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
    def new(cls, width: int, height: int, background: str = None, colorspace=None):
        """Create a new Image with the given width and height.

        :param width: The width of the image in pixels
        :param height: The height of the image in pixels
        :param background: The background color to use.
        :param colorspace: The colorspace to use.
        """

        if background is None:
            background = "ffffff"

        if colorspace is None:
            colorspace = RGB8

        bg_color = colorspace.parse(background)

        pixels = np.full((height, width, 3), bg_color, dtype=np.uint8)
        return cls(pixels)

    def _as_pillow_image(self):
        height, width, _ = self.pixels.shape

        return PIL.Image.frombuffer(
            "RGB", (width, height), self.pixels, "raw", "RGB", 0, 1
        )

    def save(self, filename: str) -> None:
        """Save an image in PNG format.

        :param filename: The filepath to save the image to.
        """

        image = self._as_pillow_image()

        with open(filename, "wb") as f:
            image.save(f)

    def encode(self) -> bytes:
        """Return the image encoded as a base64 string."""
        logger.debug("Encoding image as base64")
        image = self._as_pillow_image()

        with io.BytesIO() as byte_stream:
            image.save(byte_stream, "PNG")
            image_bytes = byte_stream.getvalue()

            return base64.b64encode(image_bytes)
