import logging

import arlunio as ar
import numpy as np

logger = logging.getLogger(__name__)


@ar.definition
def Grid(width, height, *, n=4, m=None, defn=None) -> ar.Mask:
    """
    .. arlunio-image::

       import arlunio as ar
       from arlunio.lib import Circle, Grid

       pattern = Grid(defn=Circle())
       image = ar.fill(pattern(1920, 1080))

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
    Pattern generated from circles

    .. arlunio-image::
       :include-code: before

       import arlunio as ar
       import numpy as np

       from arlunio.lib import Circle, Grid, X, Y

       @ar.definition
       def Template(x:X, y: Y):
           c = Circle(xc=.4, yc=.4, pt=.02)
           return c(x=np.abs(x), y=np.abs(y))

       pattern = Grid(defn=Template(scale=1.))
       image = ar.fill(pattern(1080,1080), background="#000", color="#ff0")

    A checkerboard like pattern

    .. arlunio-image::
       :include-code: before

       import arlunio as ar
       import numpy as np

       from arlunio.lib import Grid, X, Y

       @ar.definition
       def Template(x: X, y: Y):
           return np.abs(x) - np.abs(y) < 0

       grid = Grid(defn=Template(), n=22, m=13)
       image = ar.fill(grid(1920, 1080))
    """
    if m is None:
        m = n

    bg = np.full((height, width), False)

    # Draw the shape at a size determined by the size of the grid
    s_height, s_width = height // m, width // n
    mask = defn(s_width, s_height)

    # Let numpy handle the repeating of the shape across the image.
    pattern = np.tile(mask, (m, n))

    # Apply the pattern to the background, depending on the grid size and
    # image dimensions align, the generated grid may not perfectly fill the
    # image.
    p_height, p_width = pattern.shape

    bg[:p_height, :p_width] = pattern

    return bg


@ar.definition
def Map(width, height, *, layout=None, legend=None) -> ar.Mask:
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
    .. arlunio-image::
       :include-code: before

       import arlunio as ar
       import numpy as np

       from arlunio.lib import Empty, Map, Rectangle

       @ar.definition
       def Wall(width, height, *, sides=None):
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
               mask = ar.any(mask, wall(width, height))

           return mask

       legend = {
           "": Empty(),
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
       image = ar.fill(map_(1080, 1080), color="blue")
    """

    nx, ny = len(layout), len(layout[0])
    size = (height // ny, width // nx)  # TODO: Handle divisions with rounding errors

    # Build a new dict with the values being the shapes drawn at the appropriate res
    # to ensure we only draw them once.
    items = {k: v(*size) for k, v in legend.items()}
    return np.block([[items[key] for key in row] for row in layout])


@ar.definition
def Pixelize(width, height, *, pixels=None, defn=None, n=None, m=None) -> ar.Mask:
    """
    .. arlunio-image::

       import arlunio as ar
       from arlunio.lib import Circle, Pixelize

       pix = Pixelize(defn=Circle(), n=32, m=32)
       image = ar.fill(pix(1920, 1080))

    Draw a pixelated version of a definition.

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

    .. arlunio-image::
       :include-code: before

       import arlunio as ar
       import numpy as np

       from arlunio.lib import Pixelize

       pixels = np.array([
           [False,  True,  True, False],
           [ True, False, False,  True],
           [ True, False, False,  True],
           [False,  True,  True, False]
       ])
       defn = Pixelize(pixels=pixels)
       image = ar.fill(defn(1080, 1080))

    Alternatively we can generate the pixels from an instance of another definition

    .. arlunio-image::
       :include-code: before

       import arlunio as ar
       import numpy as np

       from arlunio.lib import Circle, X, Y, Pixelize

       @ar.definition
       def Ghost(x: X, y: Y):
           head = Circle(yc=0.5, r=0.7)
           eyes = Circle(xc=0.2, yc=0.6, r=0.3)

           body = ar.all(
               y < 0.5,
               np.abs(x) < 0.49,
               0.1 * np.cos(5 * np.pi * x) - 0.3 < y
           )

           return ar.any(
               ar.all(
                   head(x=x, y=y),
                   ar.invert(eyes(x=np.abs(x), y=y))
               ),
               body
           )

       ghost = Pixelize(defn=Ghost(y0=-0.3), n=32, m=32)
       image = ar.fill(ghost(1080,1080), color="#f00")
    """

    if defn is None and pixels is None:
        raise ValueError("You must either provide a shape or a pixel pattern.")

    if defn is not None:

        if n is None or m is None:
            raise ValueError("You must also provide the `n` and `m` attributes")

        pixels = defn(n, m)

    n, m = len(pixels), len(pixels[0])
    size = (height // m, width // n)  # TODO: Handle divisions with rounding errors

    fill = np.full(size, True)
    empty = np.full(size, False)

    return np.block([[fill if col else empty for col in row] for row in pixels])
