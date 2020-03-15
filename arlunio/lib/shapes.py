"""Built in definitions of basic shapes."""
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

    where:

    - :math:`(x_c, y_c)`: Defines the centre
    - :math:`r`: Controls the radius

    Parameters
    ----------
    xc:
        Corresponds with the :math:`x_c` variable in the equation above
    yc:
        Corresponds with the :math:`y_c` variable in the equation above
    r:
        Corresponds with the :math:`r` variable in the equation above
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

    Making use of the :code:`xc` and :code:`yc` parameters we can produce an
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

    where:

    - :math:`(x_c, y_c)`: Defines the centre
    - :math:`r`: Controls the overall size
    - :math:`a`: Controls the width
    - :math:`b`: Controls the height

    Parameters
    ----------
    xc:
        Corresponds with the :math:`x_c` variable in the equation above
    yc:
        Corresponds with the :math:`y_c` variable in the equation above
    r:
        Corresponds with the :math:`r` variable in the equation above
    a:
        Corresponds with the :math:`a` variable in the equation above
    b:
        Corresponds with the :math:`b` variable in the equation above
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
    """We define a superellipse by the following equality.

    .. math::

       \\left|\\frac{(x - x_c)}{a}\\right|^n + \\left|\\frac{(y - y_c)}{b}\\right|^m = r

    where:

    - :math:`(x_c, y_c)`: Defines the center
    - :math:`r`: Controls the overall size
    - :math:`a`: Controls the width
    - :math:`b`: Controls the height
    - :math:`n`: Controls the profile of the curve far from :math:`x = 0`
    - :math:`m`: Controls the profile of the curve close to :math:`x = 0`

    Being a generalisation of an |Ellipse| the :code:`xc`, :code:`yc`, :code:`a`,
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

    x = x - xc
    y = y - yc

    if m is None:
        m = n

    ellipse = np.abs(x / a) ** n + np.abs(y / b) ** m

    if pt is None:
        return ellipse < r

    p = r * pt
    inner = r - p
    outer = r + p

    return ar.all(inner < ellipse, ellipse < outer)


@ar.definition
def Square(x: X, y: Y, *, xc=0, yc=0, size=0.8, pt=None):
    """A square."""

    xs = np.abs(x)
    ys = np.abs(y)

    if pt is None:
        return ar.all(xs < size, ys < size)

    inner = ar.all(xs < size - pt, ys < size - pt)
    outer = ar.all(xs < size + pt, ys < size + pt)

    return ar.all(outer, ar.invert(inner))


@ar.definition
def Rectangle(x: X, y: Y, *, xc=0, yc=0, size=0.6, ratio=1.618, pt=None):
    """A Rectangle."""

    xs = np.abs(x)
    ys = np.abs(y)
    width = size * ratio
    height = size

    if pt is None:
        return ar.all(xs < width, ys < height)

    inner = ar.all(xs < width - pt, ys < height - pt)
    outer = ar.all(xs < width + pt, ys < height + pt)

    return ar.all(outer, ar.invert(inner))
