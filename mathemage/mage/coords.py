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

    # The only purpose of this is to enable the nice decorator syntax
    # it simply passes the function to the above setter
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

    # The only purpose of this is to enable the nice decorator syntax
    # it simply passes the function to the above setter
    def mask(self, f):
        self.maskfunc = f

    @property
    def colorfunc(self):
        if self._colorfunc is None:

            def default_color(x, y):
                return np.array([0, 0, 0, 255], dtype=np.uint8)

            return default_color
        else:
            return self._colorfunc

    @colorfunc.setter
    def colorfunc(self, f):
        """
        This is where we do some kung-fu introspection to try and
        optimize the code a bit better.
        """
        vcode = f.__code__
        vargs = vcode.co_varnames

        # If the color is independant of any of the arguments
        # then there is no point in evaluating the function over
        # every point in the domain, so we may as well save the result
        # now and save time later
        if len(vargs) == 0:

            # We will evaluate it and look to see if the result
            # makes sense to us
            color = f()

            if not isinstance(color, (tuple,)):
                raise TypeError('Colors must be represented by a tuple')

            # If the color is an RGB lookalike, convert it to RGBA
            if len(color) == 3:
                color = tuple([*color, 255])

            if len(color) != 4:
                raise ValueError('Colors must be in RGB (r,g,b) '
                                 'or RGBA (r,g,b,a) format!')

            self._colorfunc = color

        else:
            self._colorfunc = np.vectorize(f, signature='(),()->(4)')

    # The only purpose of this is to enable the nice decorator syntax
    # it simply passes the function to the above setter
    def colormap(self, f):
        self.colorfunc = f


def mk_domain(xmin=0, xmax=1, ymin=0, ymax=1):

    def domain(width, height):
        xs = np.linspace(xmin, xmax, width)
        ys = np.linspace(ymin, ymax, height)

        return np.meshgrid(xs, ys)

    return domain


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

        return Drawable(domain=gridfunc, mask=f, name=f.__name__)

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

        extended.__name__ = f.__name__ + '_' + extended.__name__

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


def polar():
    """
    A function decorator which constructs a wrapper function that
    additionally calculates the conversion from cartesian to polar
    coordinates and passes them into the wrapped function along with
    the original cartesian coordinates.

    This means your funtion now must be defined: f(x, y, r, t)
    """

    def domain(f):
        """
        This is the constructed decorator made by _polar_ and is
        actually where we do the mapping onto the domain
        """

        def F(x, y):

            r = sqrt(x**2 + y**2)
            t = atan2(y, x)

            return f(x, y, r, t)

        F.__name__ = f.__name__ + '_polar'

        return F

    return domain
