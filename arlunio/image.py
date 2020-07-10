import base64
import io
import logging
import pathlib
from typing import Optional

import numpy as np
import PIL.Image as PImage

import arlunio.color as color
import arlunio.mask as mask
import arlunio.math as math

logger = logging.getLogger(__name__)


class Image:
    """Our representation of an image, implemented as a wrapper around a standard
    Pillow image."""

    def __init__(self, img: PImage.Image):
        self.img = img
        """The wrapped pillow image object."""

    def __eq__(self, other):

        if not isinstance(other, Image):
            return False

        a = np.asarray(self.img)
        b = np.asarray(other.img)

        return (a == b).all()

    def __add__(self, other):

        if isinstance(other, Image):
            other = other.img

        if not isinstance(other, PImage.Image):
            raise TypeError("Addition is only supported between images.")

        img = self.copy()
        img.alpha_composite(other)

        return img

    @property
    def __array_interface__(self):
        # Ensure that our version of an image also plays nice with numpy.
        return self.img.__array_interface__

    def _repr_png_(self):
        # Give nice previews in jupyter notebooks
        return self.img._repr_png_()

    @property
    def size(self):
        return self.img.size

    def alpha_composite(self, im, *args, **kwargs):
        """Composites an image onto this image.

        See :meth:`pillow:PIL.Image.Image.alpha_composite`
        """

        if isinstance(im, Image):
            im = im.img

        self.img.alpha_composite(im, *args, **kwargs)

    def copy(self):
        """Return a copy of the image.
        See :meth:`pillow:PIL.Image.Image.copy`
        """
        return Image(self.img.copy())

    def paste(self, *args, **kwargs):
        """Paste another image into this image.

        See :meth:`pillow:PIL.Image.Image.paste`
        """
        self.img.paste(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Save the image with the given filename.

        See :meth:`pillow:PIL.Image.Image.save`
        """
        self.img.save(*args, **kwargs)

    def thumbnail(self, *args, **kwargs):
        """Convert this image into a thumbail.

        See :meth:`pillow:PIL.Image.Image.thumbnail`
        """

        self.img.thumbnail(*args, **kwargs)


def new(size, *args, mode="RGBA", **kwargs) -> Image:
    """Creates a new image with the given size.

    This function by default will return a new :code:`RGBA` image with the given
    dimensions. Dimensions can be specified either using a tuple :code:`(width, height)`
    or by passing in :code:`width` and :code:`height` individually as positional
    parameters.

    This makes use of pillow's :func:`pillow:PIL.Image.new` function, additional keyword
    arguments passed to this function will be passed onto it.

    Parameters
    ----------
    size:
        The dimensions of the image, :code:`(width, height)`
    mode:
        The type of image to create, default :code:`RGBA`. See
        :ref:`pillow:concept-modes` for more details.

    """

    if isinstance(size, int):
        if len(args) == 0:
            raise ValueError("You must specify a width and a height")

        height, args = args[0], args[1:]
        size = (size, height)

    return Image(PImage.new(mode, size, *args, **kwargs))


def fromarray(*args, **kwargs):
    """Create an image from an array

    See :func:`pillow:PIL.Image.fromarray`
    """
    return Image(PImage.fromarray(*args, **kwargs))


def load(*args, **kwargs) -> Image:
    """Load an image from the given file.

    See :func:`pillow:PIL.Image.open`
    """
    return Image(PImage.open(*args, **kwargs))


def save(image: Image, filename: str, mkdirs: bool = False) -> None:
    """Save an image in PNG format.

    :param filename: The filepath to save the image to.
    :param mkdirs: If true, make any parent directories
    """
    path = pathlib.Path(filename)

    if not path.parent.exists() and mkdirs:
        path.parent.mkdir(parents=True)

    with open(filename, "wb") as f:
        image.save(f)


def encode(image: Image) -> bytes:
    """Return the image encoded as a base64 string.

    Parameters
    ----------
    image:
       The image to encode.

    Example
    -------
    ::

       >>> import arlunio.image as image
       >>> img = image.new((8, 8), color='red')
       >>> image.encode(img)
       b'iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAFklEQVR4nGP8z8DwnwEPYMInOXwUAAASWwIOH0pJXQAAAABJRU5ErkJggg=='

    """

    with io.BytesIO() as byte_stream:
        image.save(byte_stream, "PNG")
        image_bytes = byte_stream.getvalue()

        return base64.b64encode(image_bytes)


def decode(bytestring: bytes) -> Image:
    """Decode the image represented by the given bytestring into an image object.

    Parameters
    ----------
    bytestring:
       The bytestring to decode.

    Example
    -------

    .. arlunio-image:: Decode Example
       :include-code:

       ::

          import arlunio.image as image

          bytestring = b'iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAFklEQVR4nGP8z8DwnwEPYMInOXwUAAASWwIOH0pJXQAAAABJRU5ErkJggg=='  # noqa: E501
          img = image.decode(bytestring)
    """

    data = base64.b64decode(bytestring)
    bytes_ = io.BytesIO(data)

    return Image(load(bytes_))


def colorramp(values, start: Optional[str] = None, stop: Optional[str] = None) -> Image:
    """Given a 2d array of values, produce an image gradient based on them.

    .. arlunio-image:: Colorramp Demo
       :align: right

       ::

          import arlunio.image as image
          import arlunio.math as math
          import numpy as np

          cartesian = math.Cartesian()
          p = cartesian(width=256, height=256)
          x, y = p[:, :, 0], p[:, :, 1]

          values = np.sin(2*x*np.pi) * np.sin(2*y* np.pi)
          img = image.colorramp(values)

    First this function will scale the input array so that all values fall in the range
    :math:`[0, 1]`. It will then produce an image with the same dimensions as the
    original array. The color of each pixel will be chosen based on the corresponding
    value of the scaled array.

    - If the value is :math:`0` the color will be given by the :code:`start` parameter

    - If the value is :math:`1` the color will be given by the :code:`stop` parameter

    - Otherwise the color will be some mix between the two.

    Parameters
    ----------
    values:
       The array of values used to decide on the color.
    start:
       The color to use for values near :math:`0` (default, :code:`black`)
    stop:
       The color to use for values near :math:`1` (default, :code:`white`)

    Examples
    --------

    .. arlunio-image:: Colorramp Demo 2
       :include-code:

       ::

          import arlunio.image as image
          import arlunio.math as math
          import numpy as np

          cartesian = math.Cartesian()
          p = cartesian(width=256, height=256)

          x = image.colorramp(p[:, :, 0], start="#0000", stop="#f007")
          y = image.colorramp(p[:, :, 1], start="#0000", stop="#00f7")

          img = x + y
    """

    # Scale all the values so that they fall into the range [0, 1]
    minx = np.min(values)
    vs = np.array(values) - minx
    vs = vs / np.max(vs)

    if start is None:
        start = "black"

    if stop is None:
        stop = "white"

    start = color.getcolor(start, "RGBA")
    stop = color.getcolor(stop, "RGBA")

    funcs = [math.lerp(a, b) for a, b in zip(start, stop)]
    channels = [np.floor(func(vs)) for func in funcs]

    pixels = np.array(np.dstack(channels), dtype=np.uint8)
    return fromarray(pixels)


def fill(
    mask: mask.Mask,
    foreground: Optional[str] = None,
    background: Optional[str] = None,
    image: Optional[Image] = None,
) -> Image:
    """Apply color to an image, as specified by a mask.

    Parameters
    ----------
    mask:
        The mask that selects the region to be coloured
    foreground:
        A string representation of the color to use, this can be in any format that is
        supported by the :mod:`pillow:PIL.ImageColor` module. If omitted this will
        default to black.
    background:
        In the case where an existing image is not provided this parameter can be used
        to set the background color of the generated image. This can be any string that
        is accepted by the :mod:`pillow:PIL.ImageColor` module. If omitted this will
        default to transparent
    image:
        The image to color in, if omitted a blank image will be used.

    Example
    --------

    .. arlunio-image:: Fill Demo
       :include-code:

       ::

          import arlunio.image as image
          import arlunio.shape as shape

          circle = shape.Circle(x0=-0.5, y0=0.25, r=0.6)
          img = image.fill(circle(width=512, height=256), foreground='red')

          circle.x0, circle.y0 = 0, 0
          img = image.fill(circle(width=512, height=256), foreground='#0f0', image=img)

          circle.x0, circle.y0 = 0.5, -0.25
          img = image.fill(circle(width=512, height=256), foreground='blue', image=img)

    """

    foreground = "#000" if foreground is None else foreground
    fill_color = color.getcolor(foreground, "RGBA")

    mask_img = PImage.fromarray(mask)

    if image is None:
        background = "#0000" if background is None else background

        height, width = mask.shape
        image = new((width, height), color=background)

    else:
        image = image.copy()

    image.paste(fill_color, mask=mask_img)

    return image
