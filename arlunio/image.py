import base64
import enum
import io
import logging
import string

import numpy as np
import PIL.Image

from .color import RGB8

logger = logging.getLogger(__name__)


class Resolutions(enum.Enum):
    """Enum that defines some common image resolutions

    Members of this enum are tuples containing the width and height which can be
    accessed by name::

       >>> import arlunio as st

       >>> hd = st.Resolutions.HD
       >>> hd.width
       1280

       >>> hd.height
       720

    Resolutions can also unpacked::

       >>> width, height = hd
       >>> width
       1280

       >>> height
       720

    Members are also available via the :code:`R` shortcut::

       >>> st.R.HD
       <Resolutions.HD: (1280, 720)>

    """

    HD = (1280, 720)
    """1280 x 720"""

    FHD = (1920, 1080)
    """1920 x 1080"""

    QHD = (2560, 1440)
    """2560 x 1440"""

    def __iter__(self):
        value = self.value
        return iter([value[0], value[1]])

    @property
    def width(self):
        return self.value[0]

    @property
    def height(self):
        return self.value[1]


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
              .arlunio-image {
                  width: 50%;
                  margin: auto;
                  image-rendering: crisp-edges;
                  image-rendering: pixelated;
                  border: solid 1px #ddd;
              }
            </style>
            <img class="arlunio-image" src="data:image/png;base64,$data"></img>
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

        This creates an "empty" image of a given width and height with a solid
        background color. This color can be set using the :code:`background` color
        argument, or if :code:`None` then the background will default to white.

        The :code:`background` argument should be in the form of a string
        representing the color as an RGB hex code (like those used in web design
        e.g. :code:`#ffbb00`)

        The :code:`colorspace` parameter can be used to change the colorspace used when
        drawing the image. By default this is the :code:`RGB8` colorspace.

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
