import base64
import enum
import io
import logging
import pathlib

import numpy as np
import PIL.Image as Image
import PIL.ImageColor as Color

from ._expressions import lerp

logger = logging.getLogger(__name__)


class Resolutions(enum.Enum):
    """Enum that defines some common image resolutions

    Members of this enum are tuples containing the width and height which can be
    accessed by name::

       >>> from arlunio import Resolutions as R

       >>> hd = R.HD
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


def save(image, filename: str, mkdirs: bool = False) -> None:
    """Save an image in PNG format.

    :param filename: The filepath to save the image to.
    :param mkdirs: If true, make any parent directories
    """
    path = pathlib.Path(filename)

    if not path.parent.exists() and mkdirs:
        path.parent.mkdir(parents=True)

    with open(filename, "wb") as f:
        image.save(f)


def encode(image) -> bytes:
    """Return the image encoded as a base64 string."""

    with io.BytesIO() as byte_stream:
        image.save(byte_stream, "PNG")
        image_bytes = byte_stream.getvalue()

        return base64.b64encode(image_bytes)


def colorramp(values, start=None, stop=None):
    """Given a range of values, produce an image mapping those values onto colors."""

    (r, g, b) = Color.getrgb("#000") if start is None else Color.getrgb(start)
    (R, G, B) = Color.getrgb("#fff") if stop is None else Color.getrgb(stop)

    reds = np.floor(lerp(r, R)(values))
    greens = np.floor(lerp(g, G)(values))
    blues = np.floor(lerp(b, B)(values))

    pixels = np.array(np.dstack([reds, greens, blues]), dtype=np.uint8)
    return Image.fromarray(pixels)


def fill(mask, color=None, background=None):
    """Given a mask, fill it in with a color."""

    color = "#000" if color is None else color
    background = "#fff" if background is None else background

    mask_img = Image.fromarray(mask)
    fill_color = Color.getrgb(color)

    height, width = mask.shape

    image = Image.new("RGB", (width, height), color=background)
    image.paste(fill_color, mask=mask_img)

    return image
