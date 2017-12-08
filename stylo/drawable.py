import numpy as np
import re

from math import sin, cos

from collections import namedtuple

def mk_repeater(x_min, x_max):
    """
    Factory function produce a repeater function. Given the
    bounds of the domain, the resulting function will shift values
    until it lies within the resulting domain

    Parameters
    ----------
    x_min : float
        The minimum value of the domain
    x_max : float
        The maximum value of the domain

    Returns
    -------
    A function that accepts a numpy array and shifts each of the
    elements until they lie within the specified domain
    """

    x_length = x_max - x_min

    def repeat(x):

        while x > x_max:
            x -= x_length

        while x < x_min:
            x += x_length

        return x

    return np.vectorize(repeat)


class Domain:
    """
    How we represent a 2D mathematical domain.
    """

    def __init__(self, x_min=-1, x_max=1, y_min=-1, y_max=1):

        if x_min >= x_max:
            message = 'Invalid range for X domain: '
            message += '[{}, {}]\n'.format(x_min, x_max)
            message += 'x_min must be less than x_max'

            raise ValueError(message)

        if y_min >= y_max:
            message = 'Invalid range for Y domain: '
            message += '[{}, {}]\n'.format(y_min, y_max)
            message += 'y_min must be less than y_max'

            raise ValueError(message)

        self._xmin = x_min
        self._xmax = x_max
        self._ymin = y_min
        self._ymax = y_max

        # A list to put all the modification functions in to be applied
        # later
        self._mods = []

        # Here we build a dict containing "instructions" on how to get the
        # values for the desired coordinate values
        self._coords = {
            'x': lambda w, h: self._X(w, h),
            'y': lambda w, h: self._Y(w, h),
            'r': lambda w, h: self._R(w, h),
            't': lambda w, h: self._T(w, h),
        }

    def __str__(self):
        return "[{}, {}] x [{}, {}]".format(self._xmin, self._xmax,
                                            self._ymin, self._ymax)

    def __repr__(self):
        return "Domain(x_min={},x_max={},y_min={},y_max{})".format(self._xmin,
               self._xmax, self._ymin, self._ymax)

    def __getitem__(self, key):

        # We need to make sure we get the three things we expect from
        # the user
        try:
            coordstr, width, height = key
        except ValueError:
            message = ('Expected: \'coordstr\', i, j where\n'
                       'coordstr: a string representing the variables '
                       'you wanted e.g. \'xy\'\n'
                       'i: the width of the picture in pixels\n'
                       'j: the height of the picture in pixels')

            raise ValueError(message)

        # Next, we need to validate the coordinate string
        coordstr = ''.join(coordstr)
        fmt = re.compile('\A[' + self.coords + ']+\Z')

        if not fmt.match(coordstr):
            message = 'Coordinate string can only contain one '
            message += 'of the following: '
            message += ', '.join(self.coords)

            raise ValueError(message)

        # Next just make sure the dimensions are ok
        width_ok = isinstance(width, (int,)) and width > 0
        height_ok = isinstance(height, (int,)) and height > 0

        if not (width_ok and height_ok):
            raise ValueError('Width and Height must be specified by positive integers!')

        # Finally! We can return the coordinates asked for
        return tuple(self._coords[c](width, height) for c in coordstr)

    def __call__(self, f):
        return Drawable(domain=self, mask=f, color=None, name=f.__name__)

    def _gen_coords(self, width, height):
        # Generate the 'vanilla' grid of coordinates

        xs = np.linspace(self._xmin, self._xmax, width)
        xs = np.array([xs for _ in range(height)])

        ys = np.linspace(self._ymax, self._ymin, height)
        ys = np.array([ys for _ in range(width)])
        ys = ys.transpose()

        return (xs, ys)

    def _get_coords(self, width, height):
        # Get the grid of coordinates, modifications and all

        X, Y = self._gen_coords(width, height)

        for mod in self._mods:
            X, Y = mod(X, Y)

        return (X, Y)

    def transform(self, dx=[0, 0], r=0):

        def transformation(X, Y):
            # The following is the equivalent of doing the
            # transformation matrix multiplication 'by hand'
            Xp = X * np.cos(-r) - Y * np.sin(-r) - dx[0]
            Yp = X * np.sin(-r) + Y * np.cos(-r) - dx[1]

            return (Xp, Yp)

        self._mods.insert(0, transformation)


    def repeat(self, x_min, x_max, y_min, y_max):

        x_repeat = mk_repeater(self._xmin, self._xmax)
        y_repeat = mk_repeater(self._ymin, self._ymax)

        self._xmin = x_min
        self._xmax = x_max
        self._ymin = y_min
        self._ymax = y_max

        self._mods.insert(0, lambda x, y: (x_repeat(x), y_repeat(y)))

    @property
    def coords(self):
        return ''.join(self._coords.keys())


    @property
    def _X(self):

        def mk_xs(width, height):
            X, _ = self._get_coords(width, height)
            return X

        return mk_xs

    @property
    def _Y(self):

        def mk_ys(width, height):
            _, Y = self._get_coords(width, height)
            return Y

        return mk_ys

    @property
    def _R(self):

        X = self._X
        Y = self._Y

        def mk_rs(width, height):

            XS = X(width, height)
            YS = Y(width, height)

            return np.sqrt(XS * XS + YS * YS)

        return mk_rs

    @property
    def _T(self):

        X = self._X
        Y = self._Y

        def mk_ts(width, height):

            XS = X(width, height)
            YS = Y(width, height)

            return np.arctan2(YS, XS)

        return mk_ts


Drawable = namedtuple('Drawable', ['domain', 'mask', 'color', 'name'])
