import arlunio as ar
import numpy as np

from .parameters import X, Y


@ar.definition
def Circle(x: X, y: Y, *, xc=0, yc=0, r=0.8, pt=None):
    """
    .. arlunio-image::

        import arlunio as ar
        from arlunio.lib import Circle

        circle = Circle()
        image = ar.fill(circle(1920, 1080))

    We define a circle using the following equality.

    .. math::

       (x - x_c)^2 + (y - y_c)^2 = r^2

    Attributes
    ----------
    xc:
        Corresponds with the :math:`x_c` variable in the equation above and defines the
        :math:`x`-coordinate of the circle's center.
    yc:
        Corresponds with the :math:`y_c` variable in the equation above and defines the
        :math:`y`-coordinate of the circle's center.
    r:
        Corresponds with the :math:`r` variable in the equation above and defines the
        radius of the circle.
    pt:
        If :code:`None`, then all points within the radius of the circle will be
        considered to be part of it. If this is set to some positive number then all
        points between radii :code:`(1 - pt) * r` and :code:`(1 + pt) * r` will be
        considered part of the circle.

    Examples
    --------
    Combining a few circles it's easy enough to draw a target

    .. arlunio-image::
       :include-code: before

       import arlunio as ar
       from arlunio.lib import Circle

       @ar.definition
       def Target(width, height):
           image = None
           parts = [
               (Circle(pt=0.02), "#000"),
               (Circle(r=0.75, pt=0.12), "#f00"),
               (Circle(r=0.6, pt=0.05), "#f00"),
               (Circle(r=0.4), "#f00"),
           ]

           for part, color in parts:
               image = ar.fill(part(width, height), color=color, image=image)

           return image

       target = Target()
       image = target(1920, 1080)

    Making use of the :code:`xc` and :code:`yc` attributes we can produce an
    approximation of the olympics logo

    .. arlunio-image::
       :include-code: before

       import arlunio as ar
       from arlunio.lib import Circle

       @ar.definition
       def OlympicRings(width, height, *, spacing=0.5, pt=0.025):

           dy = spacing / 4
           dx = spacing / 2
           args = {"scale": 0.5, "r": spacing, "pt": pt}

           image = None
           rings = [
               (Circle(yc=dy, xc=-(2.2 * dx), **args), "#0ff"),
               (Circle(yc=dy, **args), "#000"),
               (Circle(yc=dy, xc=(2.2 * dx), **args), "#f00"),
               (Circle(yc=-dy, xc=-(1.1 * dx), **args), "#ff0"),
               (Circle(yc=-dy, xc=(1.1 * dx), **args), "#0f0")
           ]

           for ring, color in rings:
               image = ar.fill(ring(width, height), color=color, image=image)
           return image

       rings = OlympicRings()
       image = rings(1920, 1080)
    """
    x = (x - xc) ** 2
    y = (y - yc) ** 2
    circle = np.sqrt(x + y)

    if pt is None:
        return circle < r ** 2

    inner = (1 - pt) * r ** 2
    outer = (1 + pt) * r ** 2

    return ar.all(inner < circle, circle < outer)


@ar.definition
def Ellipse(x: X, y: Y, *, xc=0, yc=0, a=2, b=1, r=0.8, pt=None):
    """
    .. arlunio-image::

       import arlunio as ar
       from arlunio.lib import Ellipse

       ellipse = Ellipse()
       image = ar.fill(ellipse(1920, 1080))

    An ellipse can be defined using the following equality.

    .. math::

       \\left(\\frac{x - x_c}{a}\\right)^2 +
       \\left(\\frac{y - y_c}{b}\\right)^2 = r^2

    Attributes
    ----------
    xc:
        Corresponds with the :math:`x_c` variable in the equation above and defines the
        :math:`x`-coordinate of the ellipse's center.
    yc:
        Corresponds with the :math:`y_c` variable in the equation above and defines the
        :math:`y`-coordinate of the ellipse's center.
    r:
        Corresponds with the :math:`r` variable in the equation above and controls the
        overall size of the ellipse.
    a:
        Corresponds with the :math:`a` variable in the equation above and controls the
        width of the ellipse.
    b:
        Corresponds with the :math:`b` variable in the equation above and controls the
        height of the ellipse.
    pt:
        If :code:`None` then all points within the radius of the ellipse will be
        considered to be part of it. If this is set to some positive number then all
        points between radii :code:`(1 - pt) * r` and :code:`(1 + pt) * r` will be
        considered part of the ellipse.

    Examples
    --------

    :code:`a` and :code:`b` together determine the overall shape of the ellipse.
    Increasing the value of :code:`a` will stretch the ellipse width wise, increasing
    :code:`b` has a similar effect for the height. It's worth noting that it's the
    ratio of these 2 values rather than their absolute values that has a greater effect
    on the shape of the ellipse. If :code:`a = b` then the equation simplifies to that
    of a circle

    .. arlunio-image::
       :include-code: before

       import arlunio as ar
       from arlunio.lib import Ellipse

       @ar.definition
       def EllipseDemo(width, height):
           image = None
           ellipses = [
               Ellipse(xc=-0.5, yc=-0.5, a=0.5, b=0.5, r=0.4),
               Ellipse(yc=-0.5, a=1, b=0.5, r=0.4),
               Ellipse(xc=0.5, yc=-0.5, a=2, b=0.5, r=0.4),
               Ellipse(a=1, b=1, r=0.4),
               Ellipse(xc=0.5, yc=0.5, a=2, b=2, r=0.4),
               Ellipse(xc=-0.5, a=0.5, b=1, r=0.4),
               Ellipse(xc=-0.5, yc=0.5, a=0.5, b=2, r=0.4)
           ]

           for ellipse in ellipses:
               image = ar.fill(ellipse(1920, 1080), image=image)
           return image

       demo = EllipseDemo()
       image = demo(1920, 1080)

    Playing around with the values and the coordinate inputs it's possible to draw
    something that looks like a diagram of an atom

    .. arlunio-image::
       :include-code: before

       import arlunio as ar
       from arlunio.lib import Ellipse, X, Y

       @ar.definition
       def Atom(x: X, y: Y):
           image = None

           ellipses = [
               (Ellipse(a=1.5, b=0.5, pt=0.005), x, y),
               (Ellipse(a=1.5, b=0.5, r=1, pt=0.005), x + y, y - x),
               (Ellipse(a=0.5, b=1.5, pt=0.005), x, y),
               (Ellipse(a=1.5, b=0.5, r=1, pt=0.005), x - y, x + y),
               (Ellipse(a=1, b=1, r=0.15), x, y)
           ]

           for ellipse, ex, ey in ellipses:
               image = ar.fill(ellipse(x=ex, y=ey), image=image)

           return image

       atom = Atom()
       image = atom(1920, 1080)
    """

    x = (x - xc) ** 2
    y = (y - yc) ** 2

    a = a ** 2
    b = b ** 2

    ellipse = np.sqrt(x / a + y / b)

    if pt is None:
        return ellipse < r * r

    inner = (1 - pt) * r ** 2
    outer = (1 + pt) * r ** 2

    return ar.all(inner < ellipse, ellipse < outer)


@ar.definition
def SuperEllipse(x: X, y: Y, *, xc=0, yc=0, a=1, b=1, n=3, r=0.8, m=None, pt=None):
    """
    .. arlunio-image::

       import arlunio as ar
       from arlunio.lib import SuperEllipse

       ellipse = SuperEllipse()
       image = ar.fill(ellipse(1920,1080))

    We define a `SuperEllipse`_ by the following equality.

    .. math::

       \\left|\\frac{(x - x_c)}{a}\\right|^n + \\left|\\frac{(y - y_c)}{b}\\right|^m = r

    Attributes
    ----------
    x_c:
        Corresponds with the :math:`x_c` variable in the equation above and defines the
        :math:`x`-coordinate of the center of the super ellipse.
    y_c:
        Corresponds with the :math:`y_c` variable in the equation above and defines the
        :math:`y` -coordinate of the center of the super ellipse.
    r:
        Corresponds with the :math:`r` variable in the equation above and controls the
        size of the super ellipse.
    a:
        Corresponds with the :math:`a` variable in the equation above and controls the
        width of the super ellipse.
    b:
        Corresponds with the :math:`b` variable in the equation above and controls the
        height of the super ellipse.
    n:
        Corresponds with the :math:`n` variable in the equation above and controls the
        profile of the curve far from :math:`x = 0`
    m:
        Corresponds with the :math:`m` variable in the equation above and controls the
        profile of the curve close to :math:`x = 0`. If :code:`m = None` (default) then
        it will be set to the value of :code:`n`.
    pt:
        If :code:`None` then all points within the radius of the super ellipse will be
        considered to be part of it. If this is set to some positive number then all
        points between radii :code:`(1 - pt) * r` and :code:`(1 + pt) * r` will be
        considered part of the super ellipse.

    Examples
    --------

    Being a generalisation of the regular |Ellipse| definition most of the attributes
    will have a similar effect on the outcome so be sure to check it out for additional
    examples. For the :code:`SuperEllipse` definition the most interesting attributes
    are :code:`n` and :code:`m` greatly affect the shape of the super ellipse.

    .. arlunio-image::
       :include-code: before

       import arlunio as ar
       from arlunio.lib import SuperEllipse

       @ar.definition
       def SuperEllipseDemo(width, height):
           image = None
           ellipses = [
               (SuperEllipse(n=0.5, pt=0.01),'#f00'),
               (SuperEllipse(n=1, pt=0.01),'#0f0'),
               (SuperEllipse(n=1.5, pt=0.01), '#00f'),
               (SuperEllipse(n=2, pt=0.01), '#ff0'),
               (SuperEllipse(n=3, pt=0.01), '#0ff')
           ]

           for ellipse, color in ellipses:
               image = ar.fill(ellipse(1920, 1080), color=color, image=image)

           return image

       demo = SuperEllipseDemo()
       image = demo(1920, 1080)

    By default if you don't specify a value for :code:`m` it will inherit the value
    assigned to :code:`n`. However if you set :code:`m` to a different value then you
    can get even more interesting results!

    .. arlunio-image::
       :include-code: before

       import arlunio as ar
       from arlunio.lib import SuperEllipse

       @ar.definition
       def Sauron(width, height):
           image = None
           ellipses = [
               (SuperEllipse(a=2, n=3, m=0.2, r=0.98),'#f00'),
               (SuperEllipse(n=2),'#f50'),
               (SuperEllipse(n=0.1, m=2), '#000'),
           ]

           for ellipse, color in ellipses:
               image = ar.fill(ellipse(1920, 1080), color=color, image=image)

           return image

       eye = Sauron()
       image = eye(1920, 1080)

    .. _SuperEllipse: https://en.wikipedia.org/wiki/Superellipse

    """

    x = x - xc
    y = y - yc

    if m is None:
        m = n

    ellipse = np.abs(x / a) ** n + np.abs(y / b) ** m

    if pt is None:
        return ellipse < r

    inner = (1 - pt) * r
    outer = (1 + pt) * r

    return ar.all(inner < ellipse, ellipse < outer)


@ar.definition
def Empty(width, height):
    """An empty shape definition.

    Example
    -------

    .. arlunio-image::
       :include-code: before

       import arlunio as ar
       from arlunio.lib import Empty

       e = Empty()
       image = ar.fill(e(1920, 1080))
    """
    return np.full((height, width), False)


@ar.definition
def Full(width, height):
    """An full shape definition.

    Example
    -------

    .. arlunio-image::
       :include-code: before

       import arlunio as ar
       from arlunio.lib import Full

       f = Full()
       image = ar.fill(f(1920, 1080))
    """
    return np.full((height, width), True)


@ar.definition
def Square(x: X, y: Y, *, xc=0, yc=0, size=0.8, pt=None):
    """
    .. arlunio-image::

       import arlunio as ar
       from arlunio.lib import Square

       square = Square()
       image = ar.fill(square(1920, 1080))

    A square.

    Attributes
    ----------
    xc:
        Defines the :math:`x`-coordinate of the square's center
    yc:
        Defines the :math:`y`-coordinate of the square's center
    size:
        Defines the size of the square, sides will have a length of :code:`2 * size`
    pt:
        If :code:`None` then all points within the square's border will be considered to
        be part of it. If set to some positive number then all points within
        :code:`(1 - pt) * size` to :code:`(1 + pt) * size` of the border will be
        considered to be part of the square.

    Example
    -------

    .. arlunio-image::
       :include-code: before

       import arlunio as ar
       from arlunio.lib import Square, X, Y

       @ar.definition
       def SquareDemo(x: X, y: Y):
           image = None
           squares = [
               (Square(pt=0.01), x, y),
               (Square(pt=0.01), x + y, x - y),
               (Square(size=0.39, pt=0.01), x, y),
               (Square(size=0.39, pt=0.01), x + y, x - y),
               (Square(size=0.2), x, y),
           ]

           for square, sx, sy in squares:
               image = ar.fill(square(x=sx, y=sy), image=image)

           return image

       square = SquareDemo()
       image = square(1920, 1080)
    """

    xs = np.abs(x - xc)
    ys = np.abs(y - yc)

    if pt is None:
        return ar.all(xs < size, ys < size)

    s = (1 - pt) * size
    S = (1 + pt) * size

    inner = ar.all(xs < s, ys < s)
    outer = ar.all(xs < S, ys < S)

    return ar.all(outer, ar.invert(inner))


@ar.definition
def Rectangle(x: X, y: Y, *, xc=0, yc=0, size=0.6, ratio=1.618, pt=None):
    """
    .. arlunio-image::

       import arlunio as ar
       from arlunio.lib import Rectangle

       rectangle = Rectangle()
       image = ar.fill(rectangle(1920, 1080))

    A Rectangle.

    Parameters
    ----------
    xc:
        Defines the :math:`x`-coordinate of the center of the rectangle
    yc:
        Defines the :math:`y`-coordinate of the center of the rectangle
    size:
        Defines the area of the rectangle
    ratio:
        Defines the ratio of the width to the height of the rectangle
    pt:
        If :code:`None` then all points within the rectangle's border will be considered
        to be part of it. If set to some positive number then all points within
        :code:`(1 - pt) * size` to :code:`(1 + pt) * size` of the border will be
        considered to be part of the rectangle.

    Examples
    --------

    .. arlunio-image::
       :include-code: before

       import arlunio as ar
       from arlunio.lib import Rectangle

       @ar.definition
       def RectangleDemo(width, height):
           image = None
           rects = [
               Rectangle(xc=-1, size=0.4, ratio=0.5),
               Rectangle(xc=0.25, yc=0.5, size=0.2, ratio=1),
               Rectangle(xc=0.5, yc=-0.5, size=0.4, ratio=2)
           ]

           for r in rects:
               image = ar.fill(r(width, height), image=image)

           return image

       demo = RectangleDemo()
       image = demo(1920, 1080)
    """

    xs = np.abs(x - xc)
    ys = np.abs(y - yc)

    height = np.sqrt(size / ratio)
    width = height * ratio

    if pt is None:
        return ar.all(xs < width, ys < height)

    w, W = (1 - pt) * width, (1 + pt) * width
    h, H = (1 - pt) * height, (1 + pt) * height

    inner = ar.all(xs < w, ys < h)
    outer = ar.all(xs < W, ys < H)

    return ar.all(outer, ar.invert(inner))
