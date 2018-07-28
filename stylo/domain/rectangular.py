import numpy as np
from .domain import Domain


class RectangularDomain(Domain):
    """A domain of the form [xmin,xmax] x [ymin,ymax]."""

    def __init__(self, x_min, x_max, y_min, y_max):

        if x_min >= x_max:
            raise ValueError()

        if y_min >= y_max:
            raise ValueError()

        self._xmin = x_min
        self._ymin = y_min
        self._xmax = x_max
        self._ymax = y_max

    def __repr__(self):
        name = self.__class__.__name__
        return "{1}: [{0.xmin}, {0.xmax}] x [{0.ymin}, {0.ymax}]".format(self, name)

    @property
    def xmin(self):
        return self._xmin

    @property
    def ymin(self):
        return self._ymin

    @property
    def xmax(self):
        return self._xmax

    @property
    def ymax(self):
        return self._ymax

    def _get_xs(self):

        def mk_xs(width, height):
            xs = np.linspace(self.xmin, self.xmax, width)
            xs = np.array([xs for _ in range(height)])

            return xs

        return mk_xs

    def _get_ys(self):

        def mk_ys(width, height):
            ys = np.linspace(self.ymax, self.ymin, height)
            ys = np.array([ys for _ in range(width)])
            ys = ys.transpose()

            return ys

        return mk_ys

    def _get_rs(self):

        xs = self._get_xs()
        ys = self._get_ys()

        def mk_rs(width, height):

            XS = xs(width, height)
            YS = ys(width, height)

            return np.sqrt(XS * XS + YS * YS)

        return mk_rs

    def _get_ts(self):

        xs = self._get_xs()
        ys = self._get_ys()

        def mk_rs(width, height):

            XS = xs(width, height)
            YS = ys(width, height)

            return np.arctan2(YS, XS)

        return mk_rs

