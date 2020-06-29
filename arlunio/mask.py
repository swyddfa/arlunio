import functools
import logging
from typing import Union

import numpy as np

import arlunio as ar


class Mask(np.ndarray):
    """A mask is just a boolean numpy array.

    They are typically used to represent 'selections' for various operations such as
    when coloring a region of an image.
    """

    def __new__(cls, arr):
        return np.asarray(arr).view(cls)

    def __mul__(self, other):

        try:
            return np.logical_and(self, other)
        except ValueError:

            mask = self.copy()
            size = np.prod(other.shape)

            if mask[mask].shape == size:
                mask[mask] = other.reshape(size)
                return mask

            raise

    def __neg__(self):
        return np.logical_not(self)

    def __sub__(self, other):
        return np.logical_and(self, np.logical_not(other))

    def __rsub__(self, other):
        return np.logical_and(other, np.logical_not(self))

    @classmethod
    def empty(cls, *shape):
        """Return an empty mask with the given shape.

        Example
        -------
        >>> from arlunio.mask import Mask
        >>> Mask.empty(3, 4)
        Mask([[False, False, False, False],
              [False, False, False, False],
              [False, False, False, False]])
        """

        if len(shape) == 1 and isinstance(shape[0], tuple):
            return cls(np.full(shape[0], False))

        return cls(np.full(shape, False))

    @classmethod
    def full(cls, *shape):
        """Return a full mask with the given shape.

        Example
        -------
        >>> from arlunio.mask import Mask
        >>> Mask.full(3, 4)
        Mask([[ True,  True,  True,  True],
              [ True,  True,  True,  True],
              [ True,  True,  True,  True]])
        """

        if len(shape) == 1 and isinstance(shape[0], tuple):
            return cls(np.full(shape[0], True))

        return cls(np.full(shape, True))


@ar.definition
def Empty(width: int, height: int) -> Mask:
    """An empty mask.

    Example
    -------
    >>> from arlunio.mask import Empty
    >>> empty = Empty()
    >>> empty(width=4, height=3)
    Mask([[False, False, False, False],
          [False, False, False, False],
          [False, False, False, False]])
    """
    return Mask.empty(height, width)


@ar.definition
def Full(width: int, height: int) -> Mask:
    """A full mask.

    Example
    -------
    >>> from arlunio.mask import Full
    >>> full = Full()
    >>> full(width=4, height=3)
    Mask([[ True,  True,  True,  True],
          [ True,  True,  True,  True],
          [ True,  True,  True,  True]])
    """
    return Mask.full(height, width)


@ar.definition(operation=ar.Defn.OP_ADD)
def MaskAdd(
    width: int, height: int, *, a: ar.Defn[Mask] = None, b: ar.Defn[Mask] = None
) -> Mask:
    """Add any two mask producing definitions together.

    The resulting defintion will return a mask that is :code:`True` if a given point
    is :code:`True` in either :code:`a` or :code:`b`.

    Attributes
    ----------
    a:
        The first mask
    b:
        The second mask
    """

    return a(width=width, height=height) + b(width=width, height=height)


@ar.definition(operation=ar.Defn.OP_SUB)
def MaskSub(
    width: int, height: int, *, a: ar.Defn[Mask] = None, b: ar.Defn[Mask] = None
) -> Mask:
    """Subtract one mask away from another mask.

    The resulting definition will return a mask that is :code:`True` only if a given
    point is in :code:`a` **and not** in :code:`b`.

    .. note::

       You will get very different results depending on which way around you set
       :code:`a` and :code:`b`!

    Attributes
    ----------
    a:
        The first "base" mask
    b:
        The second mask that defines the region to remove from :code:`a`
    """
    return a(width=width, height=height) - b(width=width, height=height)


@ar.definition(operation=ar.Defn.OP_MUL)
def MaskMul(
    width: int, height: int, *, a: ar.Defn[Mask] = None, b: ar.Defn[Mask] = None
) -> Mask:
    """Muliply any two mask producing definitions together.

    The resulting definition will return a mask that is :code:`True` only if a given
    point is in both :code:`a` and :code:`b`.

    Attributes
    ----------
    a:
        The first mask
    b:
        The second mask
    """
    return a(width=width, height=height) * b(width=width, height=height)


def any_(*args: Union[bool, np.ndarray, Mask]) -> Mask:
    """Given a number of conditions, return :code:`True` if any of the conditions
    are true.

    This function is implemented as a thin wrapper around numpy's
    :data:`numpy:numpy.logical_or` function so that it can take an arbitrary number of
    inputs. This also means that this function will accept arrays of differing sizes,
    assuming that they can be broadcasted to a common shape.

    Parameters
    ----------
    args:
      A number of boolean conditions, a condition can either be a single boolean value
      or a numpy array of boolean values.

    Examples
    --------

    >>> import arlunio.mask as mask
    >>> mask.any_(True, False, False)
    Mask(True)
    >>> mask.any_(False, False, False, False)
    Mask(False)

    If the arguments are boolean numpy arrays, then the any condition is applied
    element-wise

    >>> import numpy as np
    >>> x1 = np.array([True, False, True])
    >>> x2 = np.array([False, False, True])
    >>> x3 = np.array([False, True, False])
    >>> mask.any_(x1, x2, x3)
    Mask([ True,  True,  True])

    The arguments can be any mixture of booleans, arrays and masks.

    >>> mask.any_(
    ...     False,
    ...     mask.Mask([True, False]),
    ...     np.array([[False, True], [True, False]])
    ... )
    Mask([[ True,  True],
          [ True, False]])


    See Also
    --------

    :doc:`numpy:user/basics.broadcasting`
       Numpy documentation on broadcasting.

    :doc:`numpy:user/theory.broadcasting`
       Further background on broadcasting.

    :data:`numpy:numpy.logical_or`
       Reference documentation on the :code:`numpy.logical_or` function
    """
    return Mask(functools.reduce(np.logical_or, args))


def all_(*args: Union[bool, np.ndarray, Mask]) -> Mask:
    """Given a number of conditions, return :code:`True` only if **all**
    of the given conditions are true.

    This function is implemented as a thin wrapper around numpy's
    :data:`numpy:numpy.logical_and` function so that it can take an arbitrary number of
    inputs. This also means that this function will accept arrays of differing sizes,
    assuming that they can be broadcasted to a common shape.

    Parameters
    ----------
    args:
      A number of boolean conditions, a conditon can either be a single boolean value,
      or a numpy array of boolean values.

    Examples
    --------

    >>> import arlunio.mask as mask
    >>> mask.all_(True, True, True)
    Mask(True)
    >>> mask.all_(True, False, True, True)
    Mask(False)

    If the arguments are boolean numpy arrays, then the any condition is applied
    element-wise

    >>> import numpy as np
    >>> x1 = np.array([True, False, True])
    >>> x2 = np.array([False, False, True])
    >>> x3 = np.array([False, True, True])
    >>> mask.all_(x1, x2, x3)
    Mask([False, False,  True])

    Arugments can be any mixture of booleans, masks and numpy arrays.

    >>> mask.all_(
    ...     True,
    ...     mask.Mask([True, False]),
    ...     np.array([[False, True], [True, False]])
    ... )
    Mask([[False, False],
          [ True, False]])


    See Also
    --------

    :doc:`numpy:user/basics.broadcasting`
       Numpy documentation on broadcasting.

    :doc:`numpy:user/theory.broadcasting`
       Further background on broadcasting.

    :data:`numpy:numpy.logical_and`
       Reference documentation on the :code:`logical_and` function.
    """
    return Mask(functools.reduce(np.logical_and, args))


@ar.definition
def Repeat(width: int, height: int, *, n=4, m=None, defn=None) -> Mask:
    """Given a mask producing definition, replicate the resulting mask in a grid.

    .. arlunio-image:: Simple Grid

       ::

          import arlunio.image as image
          import arlunio.mask as mask
          import arlunio.shape as shape

          pattern = mask.Repeat(defn=shape.Circle())
          img = image.fill(pattern(width=256, height=256))

    When evaluated this will create a mask with the given :code:`width` and
    :code:`height`. It will then subdivide it into an :math:`n \\times m` grid where
    each cell contains a copy of the mask as produced by the definition specified with
    the :code:`defn` attribute.

    It's important to note that the given definition must only take :code:`width` and
    :code:`height` as inputs.


    .. note::

       Due to a limitation in the current implementation, you will get the best results
       if your :math:`n \\times m` grid divides cleanly into the resolution of the final
       mask. Otherwise you will find that the generated grid won't completly fill it.

    Attributes
    ----------
    n:
        The number of times to repeat the given definition horizontally
    m:
        The number of times to repeat the given definition vertically. If :code:`None`
        this defaults to the value of :code:`n`
    defn:
        The instance of the definition to replicate.

    Examples
    --------

    .. arlunio-image:: Circular Pattern
       :gallery: examples
       :include-code:
       :width: 50%

       A pattern generated from circles::

          import arlunio as ar
          import numpy as np

          import arlunio.image as image
          import arlunio.math as math
          import arlunio.mask as mask
          import arlunio.shape as shape

          @ar.definition
          def Template(x: math.X, y: math.Y) -> mask.Mask:
              c = shape.Circle(xc=0.4, yc=0.4, pt=0.02)
              return c(x=np.abs(x), y=np.abs(y))

          pattern = mask.Repeat(defn=Template(scale=1.))
          img = image.fill(
              pattern(width=1080, height=1080), background="#000", foreground="#ff0"
          )

    .. arlunio-image:: Checkerboard
       :gallery: examples
       :include-code:
       :width: 50%

       A checkerboard::

          import arlunio.image as image
          import arlunio.mask as mask
          import arlunio.pattern as pattern

          grid = mask.Repeat(defn=pattern.Checker())
          img = image.fill(grid(width=1080, height=1080), background="white")

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
def Map(width: int, height: int, *, layout=None, legend=None, fill=None) -> Mask:
    """Build a mask composed out of smaller, simpler masks.

    When evaluated this will produce a mask with the given :code:`width` and
    :code:`height` and divide it into a grid. The dimensions of this grid are determined
    by shape of the :code:`layout` array.

    The :code:`layout` attribute should be set to a 2D array the elements of which can
    be anything. While the :code:`legend` attribute is set to a dictionary whose keys
    correspond to values in the :code:`layout` array. These keys should then map to mask
    producing definitions. It's important to note that these definitions can only take
    :code:`width` and :code:`height` as inputs.

    The cells in the grid will then be set to the mask produced by the definition
    corresponding to the value in the :code:`layout`. If however the :code:`legend` does
    not contain a matching key then the :code:`fill` definition will be used instead.

    .. note::

       Due to a limitation in the current implementation, you will get best results
       if the dimensions of the :code:`layout` grid divide cleanly into the dimensions
       of the final mask.

    Attributes
    ----------
    fill:
        The definition to use in any cell where a corresponding definition cannot be
        found in the legend. If :code:`None` this will default to
        :class:`arlunio.mask.Empty`
    layout:
        A 2D numpy array of values representing keys from the :code:`legend` detailing
        which mask should be used in which cell.
    legend:
        A dictionary with keys corresponding to values in the :code:`layout` that map to
        mask producing definitions that should be used.

    Example
    -------
    .. arlunio-image:: Simple Map
       :include-code:
       :width: 50%
       :gallery: examples

       ::

          import arlunio.image as image
          import arlunio.mask as mask
          import arlunio.shape as shape

          import numpy as np

          top = shape.Rectangle(size=0.2, yc=1, ratio=50)
          left = shape.Rectangle(size=0.2, xc=-1, ratio=1/50)
          right = shape.Rectangle(size=0.2, xc=1, ratio=1/50)
          bottom = shape.Rectangle(size=0.2, yc=-1, ratio=50)

          legend = {
              "tt": top,
              "bb": bottom,
              "ll": left,
              "rr": right,
              "tl": top + left,
              "tr": top + right,
              "bl": bottom + left,
              "br": bottom + right
          }

          layout = np.array([
              ["tt", "tt", "tt", "tt", "tr"],
              [  "", "tl", "tt", "tr", "rr"],
              [  "", "ll", "bl", "br", "rr"],
              [  "", "bl", "bb", "bb", "br"],
              [  "",   "",   "",   "",   ""]
          ])

          map_ = mask.Map(legend=legend, layout=layout)
          img = image.fill(
              map_(width=1080, height=1080), foreground="blue", background="white"
          )
    """
    fill = fill if fill is not None else Empty()

    # TODO: Handle divisions with rounding errors
    nx, ny = len(layout), len(layout[0])
    size = {"height": height // ny, "width": width // nx}

    # Build a new dict with the values being the shapes drawn at the appropriate res
    # to ensure we only draw them once.
    items = {k: v(**size) for k, v in legend.items()}
    default = fill(**size)

    return np.block([[items.get(key, default) for key in row] for row in layout])


@ar.definition
def Pixelize(width: int, height: int, *, mask=None, defn=None, scale=16) -> Mask:
    """Produce a pixelated version of the given mask.

    .. arlunio-image:: Pixelise
       :align: center

       ::

          import arlunio.image as image
          import arlunio.mask as mask
          import arlunio.shape as shape

          pix = mask.Pixelize(defn=shape.Circle())
          img = image.fill(pix(width=256, height=256))

    This definition can either be given an existing :code:`mask` or a mask producing
    definition which can be given with the :code:`defn` attribute. Note that this
    definition can only take :code:`width` and :code:`height` as inputs.

    .. note::

       There is a limitation in the current implementation where the resulting mask may
       be smaller than expected due to rounding errors. For best results

       - Ensure that the shape of the mask given with the :code:`mask` attribute cleanly
         divides your desired :code:`width` and :code:`height`.

       - When using the :code:`defn` attribute ensure that the :code:`scale` attribute
         cleanly divides your desired :code:`width` and :code:`height`.


    Attributes
    ----------
    mask:
        The mask to pixelise. If given then :code:`defn` must be :code:`None`.
    defn:
        The mask producing definition to use. If given then :code:`mask` must be
        :code:`None`
    scale:
        When providing the :code:`defn` attribute this controls the resolution the
        definition is rendered at. Has no effect when providing a :code:`mask`

    Examples
    --------

    This definition can be used to render a mask at a higher resolution

     .. arlunio-image:: Creeper
       :gallery: examples
       :include-code:
       :width: 50%

       ::

          import numpy as np

          import arlunio.image as image
          import arlunio.mask as mask

          face = np.array([
              [False, False, False, False, False, False, False, False],
              [False, False, False, False, False, False, False, False],
              [False,  True,  True, False, False,  True,  True, False],
              [False,  True,  True, False, False,  True,  True, False],
              [False, False, False,  True,  True, False, False, False],
              [False, False,  True,  True,  True,  True, False, False],
              [False, False,  True,  True,  True,  True, False, False],
              [False, False,  True, False, False,  True, False, False],
          ])

          defn = mask.Pixelize(mask=face)
          img = image.fill(defn(width=512, height=512), background="white")

    We can also generate the mask directly from another definition.

    .. arlunio-image:: Ghost
       :include-code:
       :width: 50%
       :gallery: examples

       ::

          import arlunio as ar
          import arlunio.image as image
          import arlunio.mask as mask
          import arlunio.math as math
          import arlunio.shape as shape

          import numpy as np

          @ar.definition
          def Ghost(x: math.X, y: math.Y) -> mask.Mask:
              head = shape.Circle(yc=0.5, r=0.7)
              eyes = shape.Circle(xc=0.2, yc=0.6, r=0.3)

              body = mask.all_(
                  y < 0.5,
                  np.abs(x) < 0.49,
                  0.1 * np.cos(5 * np.pi * x) - 0.3 < y
              )

              return (head(x=x, y=y) - eyes(x=np.abs(x), y=y)) + body

          ghost = mask.Pixelize(defn=Ghost(y0=-0.3), scale=32)
          img = image.fill(
              ghost(width=1080, height=1080), foreground="#f00", background="white"
          )

    """
    logger = logging.getLogger(__name__)

    if defn is None and mask is None:
        raise ValueError("You must provide a mask or a mask producing definition.")

    if mask is not None:
        w, h = len(mask), len(mask[0])

    if defn is not None:
        # Based on the given resolution, calculate the size of each enlarged element.
        ratio = width / height

        w, h = int(scale * ratio), scale
        mask = defn(width=w, height=h)

    n, m = int(width // w), int(height // h)

    logger.debug("Mask size: (%s, %s)", w, h)
    logger.debug("Pixel size: (%s, %s)", n, m)

    fill = Mask.full(m, n)
    empty = Mask.empty(m, n)

    return Mask(np.block([[fill if col else empty for col in row] for row in mask]))
