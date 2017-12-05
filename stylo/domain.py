import numpy as np
import re


class Domain:
    """
    How we represent a mathematical domain.
    """

    def __init__(self, x_min=-1, x_max=1, y_min=-1, y_max=1):

        self._xmin = x_min
        self._xmax = x_max
        self._ymin = y_min
        self._ymax = y_max

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
            raise ValueError('Please specify the coordinate variables you '
                             'want along with the width and height of the '
                             'image')

        # Here we build a dict containing "instructions" on how to get the
        # values for the desired coordinate values
        coords = {
            'x': lambda w, h: self.X(w, h),
            'y': lambda w, h: self.Y(w, h),
            'r': lambda w, h: self.R(w, h),
            't': lambda w, h: self.T(w, h),
        }

        # Next, we need to validate the coordinate string
        coordstr = ''.join(coordstr.lower())
        fmt = re.compile('\A[xyrt]+\Z')

        if not fmt.match(coordstr):
            raise ValueError('Coordinate string can only contain one '
                             'of the following: x, y, r, t')

        # Next just make sure the dimensions are ok
        width_ok = isinstance(width, (int,)) and width > 0
        height_ok = isinstance(height, (int,)) and height > 0

        if not (width_ok and height_ok):
            raise ValueError('Width and Height must be specified by positive integers!')

        # Finally! We can return the coordinates asked for
        return tuple(coords[c](width, height) for c in coordstr)


    @property
    def X(self):

        def mk_xs(width, height):
            xs = np.linspace(self._xmin, self._xmax, width)
            return np.array([xs for _ in range(height)])

        return mk_xs

    @property
    def Y(self):

        def mk_ys(width, height):
            ys = np.linspace(self._ymax, self._ymin, height)
            Y = np.array([ys for _ in range(width)])
            return Y.transpose()

        return mk_ys

    @property
    def R(self):

        X = self.X
        Y = self.Y

        def mk_rs(width, height):

            XS = X(width, height)
            YS = Y(width, height)

            return np.sqrt(XS * XS + YS * YS)

        return mk_rs

    @property
    def T(self):

        X = self.X
        Y = self.Y

        def mk_ts(width, height):

            XS = X(width, height)
            YS = Y(width, height)

            return np.arctan2(YS, XS)

        return mk_ts
