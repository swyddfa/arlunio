import numpy as np
from math import sqrt, atan2, sin, cos


def cartesian(X=[-1, 1], Y=[-1, 1]):
    """
    A function decorator which constructs a wrapper function that
    maps a given function onto a domain with given dimensions and
    cartesian coordinates
    """

    xmin, xmax = X
    ymin, ymax = Y

    def domain(f):
        """
        This is the constructed decorator made by _cartesian_ and is
        actually where we do the mapping onto the domain
        """

        def F(i, j):

            x = (1 - i)*xmin + i*xmax

            # Annoyingly convention for images is to have the orign in the
            # upper left of the image, but for maths convention for the origin
            # to be in the lower left of the image. Simply interpolating the
            # max, min y values the 'wrong' way should allow us to keep
            # thinking mathematically while the code behind the scenes works as
            # expected
            y = (1 - j)*ymax + j*ymin
            return f(x, y)

        return F

    return domain


def extend_periodically(X=[-1, 1], Y=[-1, 1]):
    """
    A function decorator which wraps a function defined on X x Y
    and extends it to an arbitrary domain by looping it back on itself
    """

    xmin, xmax = X
    xlength = xmax - xmin
    ymin, ymax = Y
    ylength = ymax - ymin

    def wrapper(f):

        def extended(x, y):

            # I have no idea why I can't find a more efficient way
            # to do this *shrug*
            while x < xmin:
                x += xlength
            while x > xmax:
                x -= xlength
            while y < ymin:
                y += ylength
            while y > ymax:
                y -= ylength

            return f(x, y)

        return extended

    return wrapper


def translate(X=[0, 0], r=0):
    """
    A function decorator which allows for easy translation of a
    domain onto the final image.
    """
    def wrapper(f):

        # We need to shift values in the opposite direction
        # to achieve the intiuitive behavior
        M = np.array([[cos(-r), -sin(-r), -X[0]],
                      [sin(-r),  cos(-r), -X[1]],
                      [0, 0, 1]])

        def transformed(x, y):

            (x, y, _) = np.dot(M, np.array([x, y, 1]))
            return f(x, y)

        return transformed

    return wrapper


def reflect(Y=False, X=False):
    """
    A decorator to reflect about the x-axis, the y-axis
    or both!

    Arguments
    ---------

    X : bool, optional
        If true function is reflected across the x axis
        Default: False
    Y : bool, optional
        If true, function is reflected across the y axis
        Default: False
    """

    if X and Y:
        def wrapper(f):

            def F(x, y):

                return f(abs(x), abs(y))
            return F
        return wrapper

    if X:
        def wrapper(f):

            def F(x, y):

                return f(x, abs(y))
            return F
        return wrapper

    if Y:
        def wrapper(f):

            def F(x, y):

                return f(abs(x), y)
            return F
        return wrapper

    def wrapper(f):

        def F(x, y):

            return f(x, y)
        return F
    return wrapper


def polar(X=[-1, 1], Y=[-1, 1]):
    """
    A function decorator which constructs a wrapper function that
    maps a given function onto a domain with given dimensions and
    polar coordinates
    """

    xmin, xmax = X
    ymin, ymax = Y

    def domain(f):
        """
        This is the constructed decorator made by _polar_ and is
        actually where we do the mapping onto the domain
        """

        def F(j, i):

            x = (1 - i)*xmin + i*xmax

            # Annoyingly convention for images is to have the orign in the
            # upper left of the image, but for maths convention for the origin
            # to be in the lower left of the image. Simply interpolating the
            # max, min y values the 'wrong' way should allow us to keep
            # thinking mathematically while the code behind the scenes works as
            # expected
            y = (1 - j)*ymax + j*ymin

            # Convert to polar coordinates
            r = sqrt(x**2 + y**2)
            t = atan2(y, x)

            return f(r, t)

        return F

    return domain
