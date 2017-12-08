import numpy as np
from math import sqrt, atan2, sin, cos


def mk_domain(xmin=0, xmax=1, ymin=0, ymax=1):

    def domain(width, height):
        xs = np.linspace(xmin, xmax, width)
        ys = np.linspace(ymax, ymin, height)

        return np.meshgrid(xs, ys)

    return domain


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

        transformed.__name__ = f.__name__ + '_translated'

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

            F.__name__ = f.__name__ + '_reflected'

            return F
        return wrapper

    if X:
        def wrapper(f):

            def F(x, y):

                return f(x, abs(y))

            F.__name__ = f.__name__ + '_reflected'
            return F
        return wrapper

    if Y:
        def wrapper(f):

            def F(x, y):

                return f(abs(x), y)

            F.__name__ = f.__name__ + '_reflected'
            return F
        return wrapper

    def wrapper(f):

        def F(x, y):

            return f(x, y)

        F.__name__ = f.__name__ + '_reflected'
        return F
    return wrapper
