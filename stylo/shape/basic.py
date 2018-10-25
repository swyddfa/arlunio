"""This module defines the standard shapes you would expect to see from any graphics
package such as lines, simple curves, circles, squares, ellipses etc.
"""
import numpy as np

from stylo.shape.shape import Shape


def define_ellipse(a, b):
    """An ellipse can be implicitly defined by the equation.

    .. math::

       \\frac{x^2}{a^2} + \\frac{y^2}{b^2} = r^2

    where:

    - :math:`a` is known as the semi-major axis. Larger values stretch the ellipse along
      the :math:`x`-direction
    - :math:`b` is known as the semi-minor axis. Larger values stretch the ellipse along
      the :math:`y`-direction
    - :math:`r` is the radius and controls the overall size.

    This function will calculate the value of the left hand side of the above equation.

    :param a: The value of the semi-major axis
    :param b: The value of the semi-minor axis.

    :type a: float
    :type b: float

    :returns: The function in :code:`(x, y)` for the left hand side of the equation
    above.
    """
    a = a * a
    b = b * b

    def ellipse(x, y):
        return (x * x) / a + (y * y) / b

    return ellipse


def define_line(p1, p2):
    """Return a function than can be used to determine if a given point lies on the line
    joining the points :math:`p_1` and :math:`p_2`.

    This function assumes that your line is **not** vertical.

    The function returned will be the implicit form of a straight line

    .. math::

       f(x, y) = \\frac{(y_2 - y_1)}{(x_2 - x_1)}(x - x_1) + (y_1 - y)

    :param p1: The :math:`(x_1, y_1)` coordinate of :math:`p_1`
    :param p2: The :math:`(x_2, y_2)` coordinate of :math:`p2`

    :type p1: tuple
    :type p2: tuple
    """

    x1, y1 = p1
    x2, y2 = p2

    m = (y2 - y1) / (x2 - x1)

    def line(x, y):
        return m * (x - x1) + (y1 - y)

    return line


class Line(Shape):
    """We can define a line joining two points :math:`p_1, p_2` implicitly using the
    following equation.

    .. math::

       f(x, y) = \\frac{(y_2 - y_1)}{(x_2 - x_1)}(x - x_1) + (y_1 - y) = 0

    where:

    - :math:`x_2 \\neq x_1`
    - :math:`p_1 = (x_1, y_1)`
    - :math:`p_2 = (x_2, y_2)`

    However since a line has no area we would never see it so we need to introduce an
    error margin :math:`e > 0`. We will say a point is on the line if

    .. math::

       |f(x, y)| \\leq e
    """

    def __init__(
        self, p1=None, p2=None, pt=0.01, extend=False, above=False, below=False
    ):
        """Construct an instance of :code:`Line` depending on the the given parameters.

        By default only a line segment is drawn joining the two points :code:`p1, p2`.
        However if :code:`extend=True` then the line will be extended off to infinity.

        The thickness of the line can be controlled with the parameter :code:`pt`, which
        corresponds to :math:`e` in the equations above.

        :param p1: The first coordinate used to define the line.
                   (Default :code:`(0, 0)`)
        :param p2: The second coordinate used to define the line.
                   (Default :code:`(1, 1)`)
        :param pt: This defines the thickness of the line. (Default :code:`0.01`)
        :param extend: If :code:`True` the line will be extended off to infinity.
        :param above: If :code:`True` then the area above the line is shaded. Only takes
                      effect when :code:`extend=True`
        :param below: If code:`True` the the area below the line is shaded. Only takes
                      effect when :code:`extend=True`

        :type p1: tuple
        :type p2: tuple
        :type pt: float
        :type extend: bool
        :type above: bool
        :type below: bool
        """

        p1 = (0, 0) if p1 is None else p1
        p2 = (1, 1) if p2 is None else p2

        # It makes things easier if we can assume x1 < x2
        points = sorted([p1, p2], key=lambda p: p[0])

        self.p1 = points[0]
        self.p2 = points[1]

        self.pt = pt
        self.extend = extend
        self.above = above
        self.below = below

    def draw(self):

        pt = self.pt
        line_definition = define_line(self.p1, self.p2)

        if self.extend and self.above:

            def above_line(x, y):
                return line_definition(x, y) <= 0

            return above_line

        if self.extend and self.below:

            def below_line(x, y):
                return line_definition(x, y) >= 0

            return below_line

        if self.extend:

            def line(x, y):
                error = np.abs(line_definition(x, y))
                return error <= pt

            return line

        x1, _ = self.p1
        x2, _ = self.p2

        def line_segment(x, y):
            error = np.abs(line_definition(x, y)) <= pt

            after = x1 < x
            before = x < x2

            in_bounds = np.logical_and(after, before)
            return np.logical_and(in_bounds, error)

        return line_segment


class Ellipse(Shape):
    """One way of defining an ellipse centered at :math:`(x_0, y_0)` is through the
    implicit equation.

    .. math::

       \\frac{(x - x_0)^2}{a^2} + \\frac{(y - y_0)^2}{b^2} - r^2 = 0

    where:

    - :math:`a` is known as the semi-major axis. Larger values stretch the ellipse along
      the :math:`x`-direction
    - :math:`b` is known as the semi-minor axis. Larger values stretch the ellipse along
      the :math:`y`-direction
    - :math:`r` is the radius and controls the overall size.

    By playing around with this definition we can draw just the outline of the ellipse
    with a given thickness or a filled in version of the ellipse.

    """

    def __init__(
        self,
        x=0,
        y=0,
        a=2,
        b=1,
        r=0.5,
        pt=0.01,
        fill=False,
        start_angle=None,
        end_angle=None,
    ):
        """Construct an instance of :code:`Ellipse` based on given parameters.

        By default this will define an ellipse that only draws it's outline. If you want
        a filled in ellipse then see the :code:`fill` parameter.

        If values for :code:`start_angle` and :code:`end_angle` are provided the portion
        of the ellipse drawn will be restricted to the portion between those two angles.
        If only one of the the values are set then only an upper/lower bound will be
        imposed.

        .. note::

           All angles are in :term:`radians`.

        :param x: The :math:`x`-coordinate of the center of the ellipse. (Default:
                  :code:`0`)
        :param y: The :math:`y`-coordinate of the center of the ellipse. (Default:
                  :code:`0`)
        :param a: The length of the semi-major axis (Default: :code:`2`)
        :param b: The length of the semi-minor axis. (Default: :code:`1`)
        :param r: The radius of the ellipse. (Default: :code:`0.5`)
        :param pt: This controls the thickness of the line used to draw the ellipse.
                   (Default: :code:`0.01`). Has no effect if :code:`fill` is used.
        :param fill: If true the ellipse is drawn as a shaded region instead of a curve.
                     (Default: :code:`False`)
        :param start_angle: If set only draw the ellipse for values of
                            :math:`\\theta \\geq t` (Default: :code:`None`)
        :param end_angle: If set only draw the ellipse for values of
                          :math:`\\theta \\leq t` (Default: :code:`None`)

        :type x: float
        :type y: float
        :type a: float
        :type b: float
        :type r: float
        :type pt: float
        :type fill: bool
        :type start_angle: float
        :type end_angle: float

        :raises ValueError: If the provided arguments are inconsistent in some way.
        """

        # These define the properties of the ellipse itself.
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.r = r

        # These define how the ellipse is actually drawn.
        self.pt = pt
        self.fill = fill

        if start_angle and end_angle and end_angle <= start_angle:
            raise ValueError("start_angle must be strictly less than end_angle")

        self.start_angle = start_angle
        self.end_angle = end_angle

    def __repr__(self):
        return "Ellipse(x={0.x}, y={0.y}, a={0.a}, b={0.b}, r={0.r})".format(self)

    def _get_filled_ellipse(self):
        """Return a function that will draw a filled in ellipse."""

        x0 = self.x
        y0 = self.y
        r = self.r * self.r
        ellipse = define_ellipse(self.a, self.b)

        def ellipse_fill(x, y):
            return ellipse(x - x0, y - y0) <= r

        return ellipse_fill

    def _get_ellipse(self):
        """Return a function that will draw an ellipse as a curve."""

        x0 = self.x
        y0 = self.y
        pt = self.pt
        r = self.r * self.r
        ellipse = define_ellipse(self.a, self.b)

        def ellipse_curve(x, y):
            error = ellipse(x - x0, y - y0) - r
            return np.abs(error) <= pt

        return ellipse_curve

    def draw(self):

        if self.fill:
            return self._get_filled_ellipse()

        return self._get_ellipse()


class Circle(Ellipse):
    """
    Mathematically a circle can be defined as the set of all
    points :math:`(x, y)` that satisfy

    .. math::

    (x - x_0)^2 + (y - y_0)^2 = r^2

    This function returns another function which when given
    a point :code:`(x, y)` will return :code:`True` if that
    point is in the circle
    """

    def __init__(self, x=0, y=0, r=0.5, *args, **kwargs):
        super().__init__(x, y, 1, 1, r, *args, **kwargs)

    def __repr__(self):
        return "Circle(x={0.x},y={0.y},r={0.r})".format(self)


class Rectangle(Shape):
    """
    It's quite simple to define a rectangle, simply pick a
    point :math:`(x_0,y_0)` that you want to be the center
    and then two numbers which will represent the width and
    height of the rectangle.
    """

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        arg_string = "x={0.x},y={0.y},width={0.width},height={0.height}".format(self)
        return "Rectangle({})".format(arg_string)

    def draw(self):

        left = self.x - (self.width / 2)
        right = self.x + (self.width / 2)
        top = self.y + (self.height / 2)
        bottom = self.y - (self.height / 2)

        def rectangle(x, y):
            xs = np.logical_and(left < x, x < right)
            ys = np.logical_and(bottom < y, y < top)

            return np.logical_and(xs, ys)

        return rectangle


class Square(Rectangle):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)

    def __repr__(self):
        return "Square(x={0.x},y={0.y},size={0.width})".format(self)


class Triangle(Shape):
    """
    A Triangle can be defined by picking three non-collinear points
    :math:`(a, b, c)` in the form of a tuple each.
    Points inside the triangle are determined using the
    barycentric coordinate system method, which is further explained
    `in this answer <https://math.stackexchange.com/a/1884485/294670>`_
    and the first method
    `here <http://totologic.blogspot.com/2014/01/accurate-point-in-triangle-test.html>`_.
    """  # noqa E501

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __repr__(self):
        return "Triangle(a={0.a}, b={0.b}, c={0.c})".format(self)

    def get_q(self):
        """
        Returns the denominator for calculating both the barycentric
        coordinates, which absolute value is the double of the area
        of the triangle.
        """
        a = self.a
        b = self.b
        c = self.c
        q = -b[1] * c[0] + a[1] * (-b[0] + c[0]) + a[0] * (b[1] - c[1]) + b[0] * c[1]

        return q

    def get_s(self, x, y):
        """
        Returns one of the barycentric coordinates of the triangle using both
        :math:`a` and :math:`c` points.
        """
        a = self.a
        c = self.c
        sign = -1 if self.get_q() < 0 else 1
        s = (a[1] * c[0] - a[0] * c[1] + (c[1] - a[1]) * x + (a[0] - c[0]) * y) * sign
        return s

    def get_t(self, x, y):
        """
        Returns one of the barycentric coordinates of the triangle using both
        :math:`a` and :math:`b` points.
        """
        a = self.a
        b = self.b
        sign = -1 if self.get_q() < 0 else 1
        t = (a[0] * b[1] - a[1] * b[0] + (a[1] - b[1]) * x + (b[0] - a[0]) * y) * sign
        return t

    def draw(self):
        def triangle(x, y):
            sign = -1 if self.get_q() < 0 else 1
            first_condition = self.get_s(x, y) > 0
            second_condition = self.get_t(x, y) > 0
            third_condition = self.get_s(x, y) + self.get_t(x, y) < self.get_q() * sign

            return np.logical_and(
                first_condition, np.logical_and(second_condition, third_condition)
            )

        return triangle
