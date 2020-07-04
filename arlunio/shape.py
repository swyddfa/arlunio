import numpy as np

import arlunio as ar
import arlunio.mask as mask
import arlunio.math as math


@ar.definition
def Circle(x: math.X, y: math.Y, *, xc=0, yc=0, r=0.8, pt=None) -> mask.Mask:
    """
    .. arlunio-image:: Basic Circle
       :align: right

       ::

          from arlunio.shape import Circle
          from arlunio.image import fill

          circle = Circle()
          image = fill(circle(width=256, height=256))

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

    .. arlunio-image:: Target
       :include-code:
       :gallery: examples

       Combining a few circles we're able to draw a target::

          import arlunio as ar
          import arlunio.image as image
          import arlunio.shape as shape

          @ar.definition
          def Target(width: int, height: int) -> image.Image:
              img = image.new((width, height), color="white")
              parts = [
                  (shape.Circle(pt=0.02), "#000"),
                  (shape.Circle(r=0.75, pt=0.12), "#f00"),
                  (shape.Circle(r=0.6, pt=0.05), "#f00"),
                  (shape.Circle(r=0.4), "#f00"),
              ]

              for part, color in parts:
                  img = image.fill(
                      part(width=width, height=height), foreground=color, image=img
                  )

              return img

          target = Target()
          img = target(width=1920, height=1080)

    Making use of the :code:`xc` and :code:`yc` attributes we can produce an
    approximation of the olympics logo

    .. arlunio-image:: Olympic Rings
       :include-code:
       :gallery: examples

       ::

          import arlunio as ar
          import arlunio.image as image
          import arlunio.shape as shape


          @ar.definition
          def OlympicRings(width: int, height: int, *, spacing=0.5, pt=0.025):

              dy = spacing / 4
              dx = spacing / 2
              args = {"scale": 0.5, "r": spacing, "pt": pt}

              img = image.new((width, height), color="white")
              rings = [
                  (shape.Circle(yc=dy, xc=-(2.2 * dx), **args), "#0ff"),
                  (shape.Circle(yc=dy, **args), "#000"),
                  (shape.Circle(yc=dy, xc=(2.2 * dx), **args), "#f00"),
                  (shape.Circle(yc=-dy, xc=-(1.1 * dx), **args), "#ff0"),
                  (shape.Circle(yc=-dy, xc=(1.1 * dx), **args), "#0f0")
              ]

              for ring, color in rings:
                  img = image.fill(
                      ring(width=width, height=height), foreground=color, image=img
                  )

              return img

          rings = OlympicRings()
          img = rings(width=1920, height=1080)
    """

    x = (x - xc) ** 2
    y = (y - yc) ** 2
    circle = np.sqrt(x + y)

    if pt is None:
        return mask.Mask(circle < r ** 2)

    inner = (1 - pt) * r ** 2
    outer = (1 + pt) * r ** 2

    return mask.all_(inner < circle, circle < outer)


@ar.definition
def Ellipse(x: math.X, y: math.Y, *, xc=0, yc=0, a=2, b=1, r=0.8, pt=None) -> mask.Mask:
    """
    .. arlunio-image:: Simple Ellipse
       :align: right

       ::

          from arlunio.shape import Ellipse
          from arlunio.image import fill

          ellipse = Ellipse(r=0.6)
          image = fill(ellipse(width=256, height=256))

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

    .. arlunio-image:: Ellipse Demo
       :include-code:

       ::

          import arlunio as ar
          import arlunio.image as image
          import arlunio.shape as shape

          @ar.definition
          def EllipseDemo(width: int, height: int):
              img = image.new(width, height, color="white")
              ellipses = [
                  shape.Ellipse(xc=-0.5, yc=-0.5, a=0.5, b=0.5, r=0.4),
                  shape.Ellipse(yc=-0.5, a=1, b=0.5, r=0.4),
                  shape.Ellipse(xc=0.5, yc=-0.5, a=2, b=0.5, r=0.4),
                  shape.Ellipse(a=1, b=1, r=0.4),
                  shape.Ellipse(xc=0.5, yc=0.5, a=2, b=2, r=0.4),
                  shape.Ellipse(xc=-0.5, a=0.5, b=1, r=0.4),
                  shape.Ellipse(xc=-0.5, yc=0.5, a=0.5, b=2, r=0.4)
              ]

              for ellipse in ellipses:
                  img = image.fill(ellipse(width=1920, height=1080), image=img)
              return img

          demo = EllipseDemo()
          img = demo(width=1920, height=1080)

    .. arlunio-image:: Atom
       :include-code:
       :gallery: examples

       Playing around with the values and the coordinate inputs it's possible to
       draw something that looks like a diagram of an atom::

          import arlunio as ar
          import arlunio.image as image
          import arlunio.math as math
          import arlunio.shape as shape


          @ar.definition
          def Atom(x: math.X, y: math.Y):
              img = None

              ellipses = [
                  (shape.Ellipse(a=1.5, b=0.5, pt=0.005), x, y),
                  (shape.Ellipse(a=1.5, b=0.5, r=1, pt=0.005), x + y, y - x),
                  (shape.Ellipse(a=0.5, b=1.5, pt=0.005), x, y),
                  (shape.Ellipse(a=1.5, b=0.5, r=1, pt=0.005), x - y, x + y),
                  (shape.Ellipse(a=1, b=1, r=0.15), x, y)
              ]

              bg = "white"

              for ellipse, ex, ey in ellipses:
                  img = image.fill(ellipse(x=ex, y=ey), image=img, background=bg)
                  bg = None

              return img

          atom = Atom()
          img = atom(width=1920, height=1080)
    """

    x = (x - xc) ** 2
    y = (y - yc) ** 2

    a = a ** 2
    b = b ** 2

    ellipse = np.sqrt(x / a + y / b)

    if pt is None:
        return mask.Mask(ellipse < r * r)

    inner = (1 - pt) * r ** 2
    outer = (1 + pt) * r ** 2

    return mask.all_(inner < ellipse, ellipse < outer)


@ar.definition
def SuperEllipse(
    x: math.X, y: math.Y, *, xc=0, yc=0, a=1, b=1, n=3, r=0.8, m=None, pt=None
) -> mask.Mask:
    """
    .. arlunio-image:: SuperEllipse
       :align: right

       ::

          from arlunio.shape import SuperEllipse
          from arlunio.image import fill

          ellipse = SuperEllipse()
          image = fill(ellipse(width=256, height=256))

    We define a `SuperEllipse`_ by the following equality.

    .. math::

       \\left|\\frac{(x - x_c)}{a}\\right|^n + \\left|\\frac{(y - y_c)}{b}\\right|^m = r

    Attributes
    ----------
    xc:
        Corresponds with the :math:`x_c` variable in the equation above and defines the
        :math:`x`-coordinate of the center of the super ellipse.
    yc:
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

    Being a generalisation of the regular :class:`arlunio.shape.Ellipse` definition most
    of the attributes will have a similar effect on the outcome so be sure to check it
    out for additional examples. For the :code:`SuperEllipse` definition the most
    interesting attributes are :code:`n` and :code:`m` greatly affect the shape of the
    super ellipse.

    .. arlunio-image:: SuperEllipse Demo
       :include-code:
       :gallery: examples

       ::

          import arlunio as ar
          import arlunio.image as image
          import arlunio.shape as shape


          @ar.definition
          def SuperEllipseDemo(width: int, height: int):
              img = image.new(width, height, color="white")
              ellipses = [
                  (shape.SuperEllipse(n=0.5, pt=0.01),'#f00'),
                  (shape.SuperEllipse(n=1, pt=0.01),'#0f0'),
                  (shape.SuperEllipse(n=1.5, pt=0.01), '#00f'),
                  (shape.SuperEllipse(n=2, pt=0.01), '#ff0'),
                  (shape.SuperEllipse(n=3, pt=0.01), '#0ff')
              ]

              for ellipse, color in ellipses:
                  img = image.fill(
                      ellipse(width=1920, height=1080), foreground=color, image=img
                  )

              return img

          demo = SuperEllipseDemo()
          img = demo(width=1920, height=1080)

    By default if you don't specify a value for :code:`m` it will inherit the value
    assigned to :code:`n`. However if you set :code:`m` to a different value then you
    can get even more interesting results!

    .. arlunio-image:: Eye of Sauron
       :include-code:
       :gallery: examples

       "Eye of Sauron"::

          import arlunio as ar
          import arlunio.image as image
          import arlunio.shape as shape


          @ar.definition
          def Sauron(width: int, height: int):
              img = image.new(width, height, color="white")
              ellipses = [
                  (shape.SuperEllipse(a=2, n=3, m=0.2, r=0.98),'#f00'),
                  (shape.SuperEllipse(n=2),'#f50'),
                  (shape.SuperEllipse(n=0.1, m=2), '#000'),
              ]

              for ellipse, color in ellipses:
                  img = image.fill(
                      ellipse(width=1920, height=1080), foreground=color, image=img
                  )

              return img

          eye = Sauron()
          img = eye(width=1920, height=1080)

    .. _SuperEllipse: https://en.wikipedia.org/wiki/Superellipse

    """

    x = x - xc
    y = y - yc

    if m is None:
        m = n

    ellipse = np.abs(x / a) ** n + np.abs(y / b) ** m

    if pt is None:
        return mask.Mask(ellipse < r)

    inner = (1 - pt) * r
    outer = (1 + pt) * r

    return mask.all_(inner < ellipse, ellipse < outer)


@ar.definition
def Square(x: math.X, y: math.Y, *, xc=0, yc=0, size=0.8, pt=None) -> mask.Mask:
    """
    .. arlunio-image:: Simple Square
       :align: right

       A square::

          from arlunio.shape import Square
          from arlunio.image import fill

          square = Square()
          image = fill(square(width=256, height=256))

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

    .. arlunio-image:: Square Demo
       :include-code:
       :gallery: examples

       ::

          import arlunio as ar
          import arlunio.image as image
          import arlunio.math as math
          import arlunio.shape as shape

          @ar.definition
          def SquareDemo(x: math.X, y: math.Y):
              img = None
              squares = [
                  (shape.Square(pt=0.01), x, y),
                  (shape.Square(pt=0.01), x + y, x - y),
                  (shape.Square(size=0.39, pt=0.01), x, y),
                  (shape.Square(size=0.39, pt=0.01), x + y, x - y),
                  (shape.Square(size=0.2), x, y),
              ]

              bg = "white"

              for square, sx, sy in squares:
                  img = image.fill(square(x=sx, y=sy), image=img, background=bg)
                  bg = None

              return img

          square = SquareDemo()
          img = square(width=1920, height=1080)
    """

    xs = np.abs(x - xc)
    ys = np.abs(y - yc)

    if pt is None:
        return mask.all_(xs < size, ys < size)

    s = (1 - pt) * size
    S = (1 + pt) * size

    inner = mask.all_(xs < s, ys < s)
    outer = mask.all_(xs < S, ys < S)

    return outer - inner


@ar.definition
def Rectangle(
    x: math.X, y: math.Y, *, xc=0, yc=0, size=0.6, ratio=1.618, pt=None
) -> mask.Mask:
    """
    .. arlunio-image:: Simple Rectangle
       :align: right

       A rectangle::

          from arlunio.shape import Rectangle
          from arlunio.image import fill

          rectangle = Rectangle()
          image = fill(rectangle(width=256, height=256))

    Attributes
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

    .. arlunio-image:: Rectangle Demo
       :include-code:

       ::

          import arlunio as ar

          from arlunio.shape import Rectangle
          from arlunio.image import fill

          @ar.definition
          def RectangleDemo(width: int, height: int):
              image = None
              rects = [
                  Rectangle(xc=-1, size=0.4, ratio=0.5),
                  Rectangle(xc=0.25, yc=0.5, size=0.2, ratio=1),
                  Rectangle(xc=0.5, yc=-0.5, size=0.4, ratio=2)
              ]

              for r in rects:
                  image = fill(r(width=width, height=height), image=image)

              return image

          demo = RectangleDemo()
          image = demo(width=1920, height=1080)
    """

    xs = np.abs(x - xc)
    ys = np.abs(y - yc)

    height = np.sqrt(size / ratio)
    width = height * ratio

    if pt is None:
        return mask.all_(xs < width, ys < height)

    w, W = (1 - pt) * width, (1 + pt) * width
    h, H = (1 - pt) * height, (1 + pt) * height

    inner = mask.all_(xs < w, ys < h)
    outer = mask.all_(xs < W, ys < H)

    return outer - inner


@ar.definition
def Triangle(p: math.Barycentric) -> mask.Mask:
    """A triangle.

    .. arlunio-image:: Triangle Demo
       :align: right

       ::

          import arlunio.shape as shape
          import arlunio.image as img

          tri = shape.Triangle()
          image = img.fill(tri(width=256, height=256))

    """

    l1 = p[:, :, 0]
    l2 = p[:, :, 1]
    l3 = p[:, :, 2]

    return mask.all_(0 < l1, l1 < 1, 0 < l2, l2 < 1, 0 < l3, l3 < 1)
