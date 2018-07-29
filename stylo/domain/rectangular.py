import numpy as np

from .domain import Domain
from stylo.utils import bounded_property


class RectangularDomain(Domain):
    """A domain of the form [xmin,xmax] x [ymin,ymax]."""

    xmin = bounded_property("_xmin")
    xmax = bounded_property("_xmax")
    ymin = bounded_property("_ymin")
    ymax = bounded_property("_ymax")

    def __init__(self, xmin, xmax, ymin, ymax):

        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def __repr__(self):
        name = self.__class__.__name__
        return "{1}: [{0.xmin}, {0.xmax}] x [{0.ymin}, {0.ymax}]".format(self, name)

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
