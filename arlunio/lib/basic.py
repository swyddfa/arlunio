import arlunio as ar
import numpy as np

basic = ar.ShapeCollection(name="basic")


@basic.shape
def Circle(x, y, *, x0=0, y0=0, r=0.8, pt=None):
    """We define a circle using the following equality.

    .. math::

       \\sqrt{(x - x_0)^2 + (y - y_0)^2} = r

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


@basic.shape
def Ellipse(x, y, *, x0=0, y0=0, a=2, b=1, r=0.8, pt=None):
    """An ellipse can be defined using the following equality.

    .. math::

       \\left(\\frac{x - x_0}{a}\\right)^2 +
       \\left(\\frac{y - y_0}{b}\\right)^2 = r^2

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


@basic.shape
def SuperEllipse(x, y, *, x0=0, y0=0, a=1, b=1, n=3, r=0.8, m=None, pt=None):
    """We define a superellipse by the following equality.

    .. math::

       \\left|\\frac{(x - x_0)}{a}\\right|^n + \\left|\\frac{(y - y_0)}{b}\\right|^m = r

    where:

    - :math:`(x_0, y_0)`: Defines the center
    - :math:`r`: Controls the overall size
    - :math:`a`: Controls the width
    - :math:`b`: Controls the height
    - :math:`n`: Controls the profile of the curve far from :math:`x = 0`
    - :math:`m`: Controls the profile of the curve close to :math:`x = 0`

    Being a generalisation of an |Ellipse| the :code:`x0`, :code:`y0`, :code:`a`,
    :code:`b`, :code:`r` and :code:`pt` values behave as they would on a regular
    ellipse.

    The main difference between a `SuperEllipse`_ and a regular ellipse is the ability
    to choose the power each term on the |LHS| is raised to. This gives greater control
    over the profile of the curve that defines the shape. The power can be set
    independantly for each term through the properties :code:`n` and :code:`m`. If
    :code:`m` is :code:`None` then the shape will assume you want :math:`m = n` and set
    the value of :code:`m` accordingly.

    Considering the case where :math:`n = 2 = m`, then we recover the definition of an
    ellipse. Increasing this value, you will start seeing something that resembles a
    rectangle with rounded corners, theoretically becoming a rectangle at infinity.
    However due to limits of the implementation, the size of the shape is hard to
    control as you go much beyond :code:`10` or :code:`20`. If you want an actual
    rectangle, then perhaps the |Rectangle| shape is what you are after.

    In the range of :math:`1 \\leq n = m < 2` the "sides" of the ellipse progressively
    straighten, becoming a diamond shape at :math:`n = 1 = m`

    Finally when the values of both :math:`n,m` are less than one, the sides of the
    diamond start curving inwards towards the origin, theoretically producing something
    that looks like a :code:`+` symbol close to (but not equal to!) :code:`0`. Again
    however, due to limitations of the implementation, the shape becomes harder to
    control as you get much smaller than :code:`0.2`

    The cases where :math:`n \\neq m` the results are harder to describe! The result
    will be some combination of the results described above, but you are probably better
    off experimenting and seeing what comes out of it!

    .. _SuperEllipse: https://en.wikipedia.org/wiki/Superellipse

    """

    xc = x - x0
    yc = y - y0

    if m is None:
        m = n

    lhs = np.abs(xc / a) ** n + np.abs(yc / b) ** m

    if pt is not None:
        return np.logical_and(r - pt / 2 < lhs, lhs < r + pt / 2)

    return lhs < r


@basic.shape
def Square(x, y, *, x0=0, y0=0, size=0.8):
    """A square."""

    xc = x - x0
    yc = y - y0

    size = size / 2

    return np.logical_and(np.abs(xc) < size, np.abs(yc) < size)
