import arlunio as ar
import numpy as np


@ar.shape
def Circle(x, y, *, x0=0, y0=0, r=0.8, pt=None):
    """We define a circle using the following inequality.

    .. math::

       \\sqrt{(x - x_0)^2 + (y - y_0)^2} < r^2

    where:

    - :math:`(x_0, y_0)`: Defines the centre
    - :math:`r`: Controls the radius

    In python these variables can be set using the :code:`x0`, :code:`y0`
    and :code:`r` keyword arguments to the shape's constructor.

    By default when drawn the shape will draw a filled in circle, however the
    :code:`pt` keyword argument can be used to override this. If not :code:`None`
    the value of this argument will be used to control the thickness of the line
    used to draw the circle.
    """

    xc = x - x0
    yc = y - y0
    circle = np.sqrt(xc * xc + yc * yc)

    if pt is None:
        return circle < r * r

    r, R = (r - pt) ** 2, (r + pt) ** 2

    return np.logical_and(r < circle, circle < R)


@ar.shape
def Ellipse(x, y, *, x0=0, y0=0, a=2, b=1, r=0.8, pt=None):
    """An ellipse can be defined using the following inequality.

    .. math::

       \\frac{(x - x_0)^2}{a^2} + \\frac{(y - y_0)^2}{b^2} < r^2

    where:

    - :math:`(x_0, y_0)`: Defines the centre
    - :math:`r`: Controls the overall size
    - :math:`a`: Controls the width
    - :math:`b`: Controls the height

    In python these variables can be set using the :code:`x0`, :code:`y0`,
    :code:`r`, :code:`a` and :code:`b` keyword arguments to the shape's
    constructor.

    Increasing the value of :code:`a` will have the effect of stretching out the
    ellpise width-wise. Similarly increasing the value of :code:`b` will do the
    same but for the height. Whenever :code:`a == b` the result will be a circle.

    By default when drawn the shape will draw the ellipse filled in, this behavior
    can be changed using the :code:`pt` keyword argument. If not :code:`None` the
    value of this argument will be used as the thickness of the line used to draw
    the ellipse.
    """

    xc = (x - x0) ** 2
    yc = (y - y0) ** 2

    A = a ** 2
    B = b ** 2

    ellipse = np.sqrt(xc / A + yc / B)

    if pt is None:
        return ellipse < r * r

    r, R = (r - pt / 2) ** 2, (r + pt / 2) ** 2

    return np.logical_and(r < ellipse, ellipse < R)


@ar.shape
def Square(x, y, *, x0=0, y0=0, size=0.8):
    """A square."""

    xc = x - x0
    yc = y - y0

    size = size / 2

    return np.logical_and(np.abs(xc) < size, np.abs(yc) < size)
