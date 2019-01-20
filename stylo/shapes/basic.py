"""This module defines the standard shapes you would expect to see from any graphics
package such as lines, simple curves, circles, squares, ellipses etc.
"""
import numpy as np

from stylo.shapes import shape
from stylo.math import anded


class Shape:
    pass


@shape()
def Ellipse(x, y, *, x0=0, y0=0, a=2, b=1, r=1):

    xc = (x - x0) ** 2
    yc = (y - y0) ** 2
    a = a * b
    b = b * b
    r = r * r

    return (xc / a) + (yc / b) < r


@shape()
def Circle(x, y, *, x0=0, y0=0, r=1):

    xc = x - x0
    yc = y - y0

    return (xc * xc) + (yc * yc) < r * r


@shape()
def Rectangle(x, y, *, x0=0, y0=0, width=1, height=0.5):

    w = width / 2
    h = height / 2

    left = x0 - w
    right = x0 + w
    top = y0 + h
    bottom = y0 - h

    return anded(left < x, x < right, bottom < y, y < top)


@shape()
def Square(x, y, *, x0=0, y0=0, size=1):

    s = size / 2

    left = x0 - s
    right = x0 + s
    top = y0 + s
    bottom = y0 - s

    return anded(left < x, x < right, bottom < y, y < top)


@shape()
def Line(x):
    pass


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
