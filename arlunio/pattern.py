import logging

import numpy as np

import arlunio as ar
from arlunio.mask import Empty
from arlunio.mask import Mask
from arlunio.math import X
from arlunio.math import Y

logger = logging.getLogger(__name__)


@ar.definition
def Checker(x: X, y: Y) -> Mask:
    """
    .. arlunio-image:: Checker
       :align: center

       ::

          from arlunio.pattern import Checker
          from arlunio.image import fill

          checker = Checker()
          image = fill(checker(width=256, height=256))

    A simple checker pattern
    """
    return x * y > 0


@ar.definition
def Grid(width: int, height: int, *, n=4, m=None, defn=None) -> Mask:
    """
    .. arlunio-image:: Simple Grid

       ::

          from arlunio.image import fill
          from arlunio.pattern import Grid
          from arlunio.shape import Circle

          pattern = Grid(defn=Circle())
          image = fill(pattern(width=512, height=256))

    Repeatedly draw the given defintition in a grid.

    This works by splitting the resolution of the final image into an :code:`n` by
    :code:`m` grid and rendering the given definition instance once and tiling the
    result across the remaining grid squares.

    .. note::

       Due to a limitation in the current implementation of this, you will get the best
       results if your :code:`n` by :code:`m` grid divides cleanly into the resolution
       of the final image.

    Attributes
    ----------
    n:
        The number of times to repeat the shape horizontally across the image
    m:
        The number of times to repeat the shape vertically across the image. If
        :code:`None` this defaults to the value of :code:`n`
    defn:
        The instance of the definition to draw.

    Examples
    --------

    .. arlunio-image:: Circular Pattern
       :include-code:
       :gallery: examples

       A pattern generated from circles::

          import arlunio as ar
          import numpy as np

          from arlunio.image import fill
          from arlunio.math import X, Y
          from arlunio.shape import Circle
          from arlunio.pattern import Grid

          @ar.definition
          def Template(x:X, y: Y):
              c = Circle(xc=.4, yc=.4, pt=.02)
              return c(x=np.abs(x), y=np.abs(y))

          pattern = Grid(defn=Template(scale=1.))
          image = fill(
              pattern(width=512, height=512), background="#000", color="#ff0"
          )

    A checkerboard like pattern

    .. arlunio-image:: Checker Pattern
       :include-code:

       A checkerboard like pattern::

          import arlunio as ar
          import numpy as np

          from arlunio.image import fill
          from arlunio.math import X, Y
          from arlunio.pattern import Grid

          @ar.definition
          def Template(x: X, y: Y):
              return np.abs(x) - np.abs(y) < 0

          grid = Grid(defn=Template(), n=16, m=8)
          image = fill(grid(width=512, height=256))
    """
    if m is None:
        m = n

    bg = np.full((height, width), False)

    # Draw the shape at a size determined by the size of the grid
    s_height, s_width = height // m, width // n
    mask = defn(width=s_width, height=s_height)

    # Let numpy handle the repeating of the shape across the image.
    pattern = np.tile(mask, (m, n))

    # Apply the pattern to the background, depending on the grid size and
    # image dimensions align, the generated grid may not perfectly fill the
    # image.
    p_height, p_width = pattern.shape

    bg[:p_height, :p_width] = pattern

    return bg


@ar.definition
def Map(width: int, height: int, *, layout=None, legend=None) -> Mask:
    """For more complex layouts.

    .. note::

       Due to a limitation in the current implementation, you will get best results
       if the dimenions of the :code:`layout` grid divide cleanly into the dimensions
       of the final image.

    Attributes
    ----------
    layout:
        A 2D numpy array of values detailing what to draw where.
    legened:
        A dictionary that maps values from the layout to definition instances to draw

    Example
    -------
    .. arlunio-image:: Simple Map
       :include-code:
       :width: 50%
       :gallery: examples

       ::

          import arlunio as ar
          import numpy as np

          from arlunio.image import fill
          from arlunio.mask import any_
          from arlunio.pattern import Map
          from arlunio.shape import Rectangle

          @ar.definition
          def Wall(width: int, height: int, *, sides=None):
              r = 50
              d = 1
              walls = {
                  'top': {"yc": d, "ratio": r},
                  'bottom': {"yc": -d, "ratio": r},
                  'left': {"xc": -d, "ratio": 1/r},
                  "right": {"xc": d, "ratio": 1/r}
              }

              mask = False
              for side in sides.split('-'):
                  wall = Rectangle(size=0.2, **walls[side])
                  mask = any_(mask, wall(width=width, height=height))

              return mask

          legend = {
              "tt": Wall(sides="top"),
              "bb": Wall(sides="bottom"),
              "ll": Wall(sides="left"),
              "rr": Wall(sides="right"),
              "tl": Wall(sides="top-left"),
              "tr": Wall(sides="top-right"),
              "bl": Wall(sides='bottom-left'),
              "br": Wall(sides="bottom-right")
          }

          layout = np.array([
              ["tt", "tt", "tt", "tt", "tr"],
              [  "", "tl", "tt", "tr", "rr"],
              [  "", "ll", "bl", "br", "rr"],
              [  "", "bl", "bb", "bb", "br"],
              [  "",   "",   "",   "",   ""]
          ])

          map_ = Map(legend=legend, layout=layout)
          image = fill(map_(width=1080, height=1080), color="blue")
    """

    # TODO: Handle divisions with rounding errors
    nx, ny = len(layout), len(layout[0])
    size = {"height": height // ny, "width": width // nx}

    # Build a new dict with the values being the shapes drawn at the appropriate res
    # to ensure we only draw them once.
    items = {k: v(**size) for k, v in legend.items()}
    default = Empty()(**size)

    return np.block([[items.get(key, default) for key in row] for row in layout])


@ar.definition
def Pixelize(
    width: int, height: int, *, pixels=None, defn=None, n=None, m=None
) -> Mask:
    """
    .. arlunio-image:: Pixelise
       :align: center

       Draw a pixelated version of a definition::

          from arlunio.image import fill
          from arlunio.pattern import Pixelize
          from arlunio.shape import Circle

          pix = Pixelize(defn=Circle(), n=16, m=16)
          image = fill(pix(width=256, height=256))


    .. note::

       Due to a limitation in the current implementation you will get the best results
       if your values for :code:`n` and :code:`m` cleanly divides into the resolution of
       the final image. This also applies to the dimensions of your array if you are
       providing the :code:`pixels` attribute directly.

    .. note::

       Due to how each enlarged pixel in the final image is mapped onto a rectangular
       region of real pixels, unless your :code:`n` by :code:`m` grid matches the aspect
       ratio of the final image you will find your original shape will be distorted as
       it is strectched to cover the final image.

    Attributes
    ----------
    pixels:
        A 2D boolean numpy array that specifies which pixels to color in.
    defn:
        An instance of a definition to use to generate the grid of pixels from.
    n:
        Required when specifying the :code:`defn` attribute, sets the number of pixels
        to generate horizontally
    m:
        Required when specifying the :code:`defn` attribute, set the number of pixels
        to generate vertically

    Examples
    --------
    This definition can be used to render a simple pixel pattern at a higher resolution

    .. arlunio-image:: Simple Pixelise
       :include-code:
       :width: 50%

       This definition can be used to render a simple pixel pattern at a higher
       resolution::

          import numpy as np

          from arlunio.image import fill
          from arlunio.pattern import Pixelize

          pixels = np.array([
              [False,  True,  True, False],
              [ True, False, False,  True],
              [ True, False, False,  True],
              [False,  True,  True, False]
          ])
          defn = Pixelize(pixels=pixels)
          image = fill(defn(width=512, height=512))


    .. arlunio-image:: Ghost
       :include-code:
       :width: 50%
       :gallery: examples

       We can also generate the pixels from an instance of another definition::

          import arlunio as ar
          import numpy as np

          from arlunio.image import fill
          from arlunio.mask import all_
          from arlunio.math import X, Y
          from arlunio.pattern import Pixelize
          from arlunio.shape import Circle

          @ar.definition
          def Ghost(x: X, y: Y):
              head = Circle(yc=0.5, r=0.7)
              eyes = Circle(xc=0.2, yc=0.6, r=0.3)

              body = all_(
                  y < 0.5,
                  np.abs(x) < 0.49,
                  0.1 * np.cos(5 * np.pi * x) - 0.3 < y
              )

              return (head(x=x, y=y) - eyes(x=np.abs(x), y=y)) + body

          ghost = Pixelize(defn=Ghost(y0=-0.3), n=32, m=32)
          image = fill(ghost(width=1080, height=1080), color="#f00")
    """

    if defn is None and pixels is None:
        raise ValueError("You must either provide a shape or a pixel pattern.")

    if defn is not None:

        if n is None or m is None:
            raise ValueError("You must also provide the `n` and `m` attributes")

        pixels = defn(width=n, height=m)

    n, m = len(pixels), len(pixels[0])
    size = (height // m, width // n)  # TODO: Handle divisions with rounding errors

    fill = np.full(size, True)
    empty = np.full(size, False)

    return np.block([[fill if col else empty for col in row] for row in pixels])
