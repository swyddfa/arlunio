import numpy as np
import re


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

    @property
    def coords(self):
        return ''.join(self._coords.keys())


    @property
    def _X(self):

        def mk_xs(width, height):
            xs = np.linspace(self._xmin, self._xmax, width)
            return np.array([xs for _ in range(height)])

        return mk_xs

    @property
    def _Y(self):

        def mk_ys(width, height):
            ys = np.linspace(self._ymax, self._ymin, height)
            Y = np.array([ys for _ in range(width)])
            return Y.transpose()

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
