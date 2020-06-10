import base64
import enum
import io
import logging
import pathlib

from typing import Optional

import numpy as np
import PIL.Image as PImage
import PIL.ImageColor as PColor

from arlunio.lib.math import lerp

logger = logging.getLogger(__name__)

# Create a type alias that we're free to change in the future
Image = PImage.Image


class Resolutions(enum.Enum):
    """Enum that defines some common image resolutions

    Members of this enum are tuples containing the width and height which can be
    accessed by name::

       >>> from arlunio.lib.image import Resolutions as R

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


def colorramp(values, start: Optional[str] = None, stop: Optional[str] = None) -> Image:
    """Given a range of values, produce an image mapping those values onto colors."""

    # Scale all the values so that they fall into the range [0, 1]
    minx = np.min(values)
    vs = np.array(values) - minx
    vs = vs / np.max(vs)

    (r, g, b) = PColor.getrgb("#000") if start is None else PColor.getrgb(start)
    (R, G, B) = PColor.getrgb("#fff") if stop is None else PColor.getrgb(stop)

    reds = np.floor(lerp(r, R)(vs))
    greens = np.floor(lerp(g, G)(vs))
    blues = np.floor(lerp(b, B)(vs))

    pixels = np.array(np.dstack([reds, greens, blues]), dtype=np.uint8)
    return PImage.fromarray(pixels)


def fill(
    mask,
    color: Optional[str] = None,
    background: Optional[str] = None,
    image: Optional[Image] = None,
) -> Image:
    """Given a mask, fill it in with a color.

    Parameters
    ----------
    mask:
        The mask used to select the pixels to fill in
    color:
        A string representation of the color to use, this can be in any format that is
        supported by Pillow's |PIL.ImageColor| module. If omitted this will default to
        black.
    background:
        In the case where an existing image is not provided this parameter can be used
        to set the background color of the generated image. This can be any string that
        is accepted by the |PIL.ImageColor| module. If omitted this will default to
        white.
    image:
        The image to color in, if omitted a new image will be generated.

    Returns
    -------
    Image
        An image with the region selected by the mask colored with the given color

    """

    color = "#000" if color is None else color
    fill_color = PColor.getrgb(color)

    mask_img = PImage.fromarray(mask)

    if image is None:
        background = "#fff" if background is None else background

        height, width = mask.shape
        image = PImage.new("RGB", (width, height), color=background)

    else:
        image = image.copy()

    image.paste(fill_color, mask=mask_img)

    return image
