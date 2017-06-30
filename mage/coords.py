import numpy as np
from math import sqrt, atan2, sin, cos


class Drawable:
    """
    A drawable consists of three things, a mask,
    a domain, and a colormap.

    The domain is a function, which given the height and
    width of the image, returns a numpy meshgrid of all the
    mathematical point in the domain each pixel represents

    The mask, is a function - which given a point in the domain
    of the drawable returns true or false indicating if that point
    is part of the drawable

    The colormap is a function - also given points in the domain
    which returns a numpy array of length 3/4 representing the
    RGB/RGBA color of that point respectively
    """

    def __init__(self, domain=None, mask=None, color=None, name=None):
        self._name = name
        self._domainfunc = domain
        self._maskfunc = np.vectorize(mask) if mask is not None else None
        self._colorfunc = np.vectorize(color, signature='(),()->(4)')\
                          if color is not None else None

    def __repr__(self):

        # The 'resolution' of the representation
        N = 8

        # We will construct a small approximation of the mask
        xdom, ydom = self.domainfunc(N, N)
        mask = self.maskfunc(xdom, ydom)

        # Little function to show us where the mask is true
        fmt = lambda t: 'XX' if t else '  '

        s = "Drawable: %s\n\n" % self.name

        # Create the 'graph' of the mask
        border = '+-' + ''.join('--' for _ in range(N)) + '-+\n'
        s += border

        for i in range(len(mask)):
            s += '| ' + ''.join(fmt(t) for t in mask[i]) + ' |\n'

        s += border + '\n'

        s += "Domain: [%.2f, %.2f] x [%.2f, %.2f]\n" % \
                (xdom[0][0], xdom[-1][-1], ydom[-1][-1], ydom[0][0])

        return s

    @property
    def name(self):
        if self._name is not None:
            return self._name
        else:
            return ''

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def domainfunc(self):
        if self._domainfunc is None:

            def default_domain(width, height):
                xs = np.linspace(-1, 1, width)
                ys = np.linspace(1, -1, height)
                return np.meshgrid(xs, ys)

            return default_domain
        else:
            return self._domainfunc

    @domainfunc.setter
    def domainfunc(self, value):
        self._domainfunc = value

    def domain(self, f):
        self.domainfunc = f

    @property
    def maskfunc(self):
        if self._maskfunc is None:

            def default_mask(x, y):
                return True

            return np.vectorize(default_mask)
        else:
            return self._maskfunc

    @maskfunc.setter
    def maskfunc(self, value):
        self._maskfunc = np.vectorize(value)

    def mask(self, f):
        self.maskfunc = f

    @property
    def colorfunc(self):
        if self._colorfunc is None:

            def default_color(x, y):
                return np.array([0, 0, 0, 255], dtype=np.uint8)

            return np.vectorize(default_color, signature='(),()->(4)')
        else:
            return self._colorfunc

    @colorfunc.setter
    def colorfunc(self, value):
        self._colorfunc = np.vectorize(value, signature='(),()->(4)')

    def colormap(self, f):
        self.colorfunc = f


def cartesian(X=[-1, 1], Y=[-1, 1]):
    """
    A function decorator which given the function and
    the domain it should be mapped onto, construct the
    necessary data structure so that the Image classes
    can apply it
    """

    xmin, xmax = X
    ymin, ymax = Y

    def domain(f):
        """
        This is the constructed decorator made by _cartesian_ and is
        actually where we do the mapping onto the domain
        """

        def gridfunc(width, height):

            xs = np.linspace(xmin, xmax, width)
            ys = np.linspace(ymax, ymin, height)

            return np.meshgrid(xs, ys)

        return {'grid': gridfunc, 'mask': np.vectorize(f)}

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
