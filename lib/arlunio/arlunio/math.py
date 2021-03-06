from __future__ import annotations

from typing import Callable

# TODO: Remove this, all numpy specifics should be confined to the backend.
import numpy as np

import arlunio as ar
import arlunio.ast as ast


def sqrt(x):
    return ast.Node.sqrt(x)


def clamp(vs, min_=0, max_=1):
    """Force an array of values to stay within a range of values.

    Parameters
    ----------
    vs:
      The array of values to clamp
    min_:
      The minimum value the result should contain
    max_:
      The maximum value the result should contain

    Examples
    --------

    By default values will be limited to between :code:`0` and :code:`1`

    >>> from arlunio.math import clamp
    >>> import numpy as np
    >>> vs = np.linspace(-1, 2, 6)
    >>> clamp(vs)
    array([0. , 0. , 0.2, 0.8, 1. , 1. ])

    But this can be changed with extra arguments to the :code:`clamp` function

    >>> clamp(vs, min_=-1, max_=0.5)
    array([-1. , -0.4,  0.2,  0.5,  0.5,  0.5])
    """
    vs = np.array(vs)
    vs[vs > max_] = max_
    vs[vs < min_] = min_

    return vs


def dot(us, vs):
    """Return the dot product of two arrays of vectors."""
    return np.sum(us * vs, axis=-1)


def length(vs):
    return np.sqrt(np.sum(vs * vs, axis=-1))


def lerp(start: float = 0, stop: float = 1) -> Callable[[float], float]:
    """Return a function that will linerarly interpolate between a and b.

    Parameters
    ----------
    start:
      The value the interpolation should start from.
    stop:
      The value the interpolation should stop at.

    Examples
    --------

    By default this function will interpolate between :code:`0` and :code:`1`

    >>> from arlunio.math import lerp
    >>> f = lerp()
    >>> f(0)
    0
    >>> f(1)
    1

    However by passing arguments to the :code:`lerp` function we can change the bounds
    of the interpolation.

    >>> import numpy as np
    >>> ts = np.linspace(0, 1, 4)
    >>> f = lerp(start=3, stop=-1)
    >>> f(ts)
    array([ 3.        ,  1.66666667,  0.33333333, -1.        ])

    """

    def f(t: float) -> float:
        return (1 - t) * start + t * stop

    return f


def normalise(vs):
    """Normalise an array into the range :math:`[0, 1]`

    Parameters
    ----------
    vs:
       The array to normalise.
    """

    if len(vs.shape) == 1:
        return vs / length(vs)

    if len(vs.shape) == 2:
        return vs / length(vs)[:, np.newaxis]


@ar.definition
def X(*, x0=0, scale=1, stretch=False):
    """Cartesian :math:`x` coordinates.

    .. arlunio-image:: X Coordinates
       :align: right

       ::

          from arlunio.math import X
          from arlunio.image import colorramp

          x = X()
          image = colorramp(x(width=256, height=256))

    Attributes
    ----------
    x0:
        Shift all the coordinate values by :code:`x0`
    scale:
        Controls the magnitude of the extreme values.
    stretch:
        If :code:`True` and the image is wider than it is tall then the grid will be
        stretched so that :code:`x = scale` falls on the image border. Otherwise the
        image's aspect ratio will be taken into account and :code:`x = scale` will fall
        somewhere within the boundaries of the image.

    Examples
    --------

    By default values will be generated between :math:`\\pm 1`::

       >>> from arlunio.math import X
       >>> x = X()
       >>> x(width=4, height=4)
       array([[-1.        , -0.33333333,  0.33333333,  1.        ],
              [-1.        , -0.33333333,  0.33333333,  1.        ],
              [-1.        , -0.33333333,  0.33333333,  1.        ],
              [-1.        , -0.33333333,  0.33333333,  1.        ]])

    If however the image is wider than it is tall this range will be extended so that
    the resulting image is not stretched::

       >>> x(width=4, height=2)
       array([[-2.        , -0.66666667,  0.66666667,  2.        ],
              [-2.        , -0.66666667,  0.66666667,  2.        ]])

    This behaviour can be disabled with the :code:`stretch` attribute::

       >>> x.stretch = True
       >>> x(width=4, height=2)
       array([[-1.        , -0.33333333,  0.33333333,  1.        ],
              [-1.        , -0.33333333,  0.33333333,  1.        ]])

    Additionally the :code:`scale` attribute can be used to adjust the magnitude of the
    extreme values generated, while the :code:`x0` attribute can be used to shift all
    the values by a given amount::

       >>> x = X(x0=-2, scale=2)
       >>> x(width=4, height=4)
       array([[0.        , 1.33333333, 2.66666667, 4.        ],
              [0.        , 1.33333333, 2.66666667, 4.        ],
              [0.        , 1.33333333, 2.66666667, 4.        ],
              [0.        , 1.33333333, 2.66666667, 4.        ]])

    """
    return ast.Node.builtin(name="x", x0=x0, scale=scale, stretch=stretch)


@ar.definition
def Y(*, y0=0, scale=1, stretch=False):
    """Cartesian :math:`y` coordinates

    .. arlunio-image:: Y Coordinates
       :align: right

       ::

          from arlunio.math import Y
          from arlunio.image import colorramp

          y = Y()
          image = colorramp(y(width=256, height=256))

    Attributes
    ----------
    y0:
        Shift all the coordinate values by :code:`y0`
    scale:
        Controls the size of the extreme values
    stretch:
        If :code:`True` and the image is taller than it is wide then the grid will be
        stretched so that :code:`y = scale` falls on the border. Otherwise the image's
        aspect ratio will be taken into account and :code:`y = scale` will fall
        somewhere within the boundaries of the image.

    Examples
    --------

    By default values will be generated between :math:`\\pm 1`::

       >>> from arlunio.math import Y
       >>> y = Y()
       >>> y(width=4, height=4)
       array([[ 1.        ,  1.        ,  1.        ,  1.        ],
              [ 0.33333333,  0.33333333,  0.33333333,  0.33333333],
              [-0.33333333, -0.33333333, -0.33333333, -0.33333333],
              [-1.        , -1.        , -1.        , -1.        ]])

    If however the image is taller than it is wide this range will be extended so that
    the resulting image is not stretched::

       >>> y(width=2, height=4)
       array([[ 2.        ,  2.        ],
              [ 0.66666667,  0.66666667],
              [-0.66666667, -0.66666667],
              [-2.        , -2.        ]])

    This behaviour can be disabled with the :code:`stretch` attribute::

       >>> y.stretch = True
       >>> y(width=2, height=4)
       array([[ 1.        ,  1.        ],
              [ 0.33333333,  0.33333333],
              [-0.33333333, -0.33333333],
              [-1.        , -1.        ]])

    Additionally the :code:`scale` attribute can be used to adjust the magnitude of the
    extreme values generated, while the :code:`y0` attribute can be used to shift all
    the values by a given amount::

       >>> y = Y(y0=-2, scale=2)
       >>> y(width=4, height=4)
       array([[4.        , 4.        , 4.        , 4.        ],
              [2.66666667, 2.66666667, 2.66666667, 2.66666667],
              [1.33333333, 1.33333333, 1.33333333, 1.33333333],
              [0.        , 0.        , 0.        , 0.        ]])

    """
    return ast.Node.builtin(name="y", y0=y0, scale=scale, stretch=stretch)


@ar.definition
def R(x: X, y: Y):
    """Polar :math:`r` coordinates.

    .. arlunio-image:: R Coordinates
       :align: right

       ::

          from arlunio.math import R
          from arlunio.image import colorramp

          r = R()
          image = colorramp(r(width=256, height=256))

    This definition corresponds with the distance a given point is from the origin and
    can be calculated from the point's equivalent Cartesian coordinate representation

    .. math::

       r = \\sqrt{x^2 + y^2}

    Examples
    --------
    ::

       >>> from arlunio.math import R
       >>> r = R()
       >>> r(width=5, height=5)
       array([[1.41421356, 1.11803399, 1.        , 1.11803399, 1.41421356],
              [1.11803399, 0.70710678, 0.5       , 0.70710678, 1.11803399],
              [1.        , 0.5       , 0.        , 0.5       , 1.        ],
              [1.11803399, 0.70710678, 0.5       , 0.70710678, 1.11803399],
              [1.41421356, 1.11803399, 1.        , 1.11803399, 1.41421356]])

    While this definition does not currently have any attributes of its own, since it's
    derived from the :class:`arlunio.math.X` and :class:`arlunio.math.Y` definitions it
    automatically inherits the attributes from these base definitions::

       >>> r = R(x0=-2, y0=-2, scale=2)
       >>> r(width=5, height=5)
       array([[4.        , 4.12310563, 4.47213595, 5.        , 5.65685425],
              [3.        , 3.16227766, 3.60555128, 4.24264069, 5.        ],
              [2.        , 2.23606798, 2.82842712, 3.60555128, 4.47213595],
              [1.        , 1.41421356, 2.23606798, 3.16227766, 4.12310563],
              [0.        , 1.        , 2.        , 3.        , 4.        ]])

    Notice how in the case where the base definitions share a attribute (:code:`scale`
    in this case) they both share the value that is set when creating an instance of the
    :code:`R` definition.

    """
    return np.sqrt(x * x + y * y)


@ar.definition
def T(x: X, y: Y, *, t0=0):
    """Polar :math:`\\theta` coordinates.

    .. arlunio-image:: T Coordinates
       :align: right

       ::

          from arlunio.math import T
          from arlunio.image import colorramp

          t = T()
          image = colorramp(t(width=256, height=256))

    This definition corresponds with the angle a given point is around from the positive
    :math:`x`-axis. This can be calculated from the point's equivalent Cartesian
    coordinate representation. All angles are given in :term:`radians`

    .. math::

       t = atan2\\left(\\frac{y}{x}\\right)

    Attributes
    ----------
    t0:
        Shift all the coordinate values by :code:`t0`

    Examples
    --------

    By default all point on the :math:`x`-axis will have a value of :code:`t = 0`::

       >>> from arlunio.math import T
       >>> t = T()
       >>> t(width=5, height=5)
       array([[ 2.35619449,  2.03444394,  1.57079633,  1.10714872,  0.78539816],
              [ 2.67794504,  2.35619449,  1.57079633,  0.78539816,  0.46364761],
              [ 3.14159265,  3.14159265,  0.        ,  0.        ,  0.        ],
              [-2.67794504, -2.35619449, -1.57079633, -0.78539816, -0.46364761],
              [-2.35619449, -2.03444394, -1.57079633, -1.10714872, -0.78539816]])

    This can be changed however with the :code:`t0` attribute::

       >>> from math import pi
       >>> t.t0 = pi
       >>> t(width=5, height=5)
       array([[-0.78539816, -1.10714872, -1.57079633, -2.03444394, -2.35619449],
              [-0.46364761, -0.78539816, -1.57079633, -2.35619449, -2.67794504],
              [ 0.        ,  0.        , -3.14159265, -3.14159265, -3.14159265],
              [-5.8195377 , -5.49778714, -4.71238898, -3.92699082, -3.60524026],
              [-5.49778714, -5.17603659, -4.71238898, -4.24874137, -3.92699082]])

    Also, being a definition derived from :class:`arlunio.math.X` and
    :class:`arlunio.math.Y` the attributes for these definitions are also available to
    control the output::

       >>> t = T(x0=-2, y0=-2, scale=2)
       >>> t(width=5, height=5)
       array([[1.57079633, 1.32581766, 1.10714872, 0.92729522, 0.78539816],
              [1.57079633, 1.24904577, 0.98279372, 0.78539816, 0.64350111],
              [1.57079633, 1.10714872, 0.78539816, 0.5880026 , 0.46364761],
              [1.57079633, 0.78539816, 0.46364761, 0.32175055, 0.24497866],
              [0.        , 0.        , 0.        , 0.        , 0.        ]])

    """
    t = np.arctan2(y, x)
    return t - t0


@ar.definition
def Cartesian(x: X, y: Y):
    """Cartesian coordinates."""
    return np.dstack([x, y])


@ar.definition
def Polar(r: R, t: T):
    """Polar coordinates."""
    return np.dstack([r, t])


@ar.definition
def Barycentric(x: X, y: Y, *, a=(0.5, -0.5), b=(0, 0.5), c=(-0.5, -0.5)):
    """Barycentric coordinates.

    .. arlunio-image:: Barycentric Demo
       :align: right

       ::

          import arlunio.math as math
          import arlunio.image as img
          import numpy as np

          coords = math.Barycentric()(width=256, height=256)

          l1 = np.abs(coords[:, :, 0])
          l2 = np.abs(coords[:, :, 1])
          l3 = np.abs(coords[:, :, 2])

          r = img.colorramp(l1, start='red', stop='black')
          g = img.colorramp(l2, start='green', stop='black')
          b = img.colorramp(l3, start='blue', stop='black')

          rs = np.asarray(r)
          gs = np.asarray(g)
          bs = np.asarray(b)

          image = img.fromarray(rs + gs + bs)

    Returns the Barycentric coordinate grid as defined by the given triangle.

    Attributes
    ----------
    a:
      The cartesian :math:`(x, y)` coordinates of the point :math:`a`
    b:
      The cartesian :math:`(x, y)` coordinates of the point :math:`b`
    c:
      The cartesian :math:`(x, y)` coordinates of the point :math:`c`
    """

    h, w = x.shape

    # Construct the transform matrix T
    t1 = a[0] - c[0]
    t2 = b[0] - c[0]
    t3 = a[1] - c[1]
    t4 = b[1] - c[1]

    # Compute the inverse determinant
    d = 1 / ((t1 * t4) - (t2 * t3))
    p = np.dstack([x, y]).reshape(w * h, 2) - c

    p1 = p[:, 0]
    p2 = p[:, 1]

    # Compute the coordinates
    l1 = d * ((p1 * t4) - (p2 * t2))
    l2 = d * ((p2 * t1) - (p1 * t3))
    l3 = 1 - l1 - l2

    return np.dstack([l1, l2, l3])[0].reshape(h, w, 3)
