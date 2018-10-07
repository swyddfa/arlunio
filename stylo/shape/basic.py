import numpy as np

from stylo.shape.shape import Shape


class Ellipse(Shape):
    """An ellipse.

    Mathematically we can define an ellipse to be the set
    of points :math:`(x, y)` which satisfy:

    .. math::

        \\frac{(x - x_0)^2}{a^2} + \\frac{(y - y_0)^2}{b^2} \\leq r^2

    where:

    - :math:`(x_0, y_0)` is the center of the ellipse
    - :math:`a` is known as the semi major axis, larger values make the
      ellipse more elongated in the :math:`x`-direction
    - :math:`b` is known as the semi minor axis, larger values make the
      ellipse more elongated in the :math:`y`-direction
    - :math:`r` is the "radius" of the ellipse and controls the overall
      size of the ellipse
    """

    def __init__(self, x, y, a, b, r):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.r = r

    def __repr__(self):
        return "Ellipse(x={0.x}, y={0.y}, a={0.a}, b={0.b}, r={0.r})".format(self)

    def draw(self):

        r = self.r * self.r
        a = self.a
        b = self.b
        x0 = self.x
        y0 = self.y

        def ellipse(x, y):
            xc = x - x0
            yc = y - y0

            return (xc * xc) / a + (yc * yc) / b <= r

        return ellipse


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

    def __init__(self, x, y, r):
        super().__init__(x, y, 1, 1, r)

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
