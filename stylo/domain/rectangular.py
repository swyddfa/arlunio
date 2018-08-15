import numpy as np

from .domain import RealDomain, PolarConversion
from stylo.utils import bounded_property


class RectangularDomain(PolarConversion, RealDomain):
    """A domain of the form :math:`[a, b] \\times [c, d] \\subset \\mathbb{R}^2`"""

    xmin = bounded_property("xmin", bounded_above_by="xmax")
    xmax = bounded_property("xmax", bounded_below_by="xmin")
    ymin = bounded_property("ymin", bounded_above_by="ymax")
    ymax = bounded_property("ymax", bounded_below_by="ymin")

    def __init__(self, xmin, xmax, ymin, ymax):

        if xmin >= xmax:
            raise ValueError(
                "The value of xmin must be strictly less than the " "value of xmax"
            )

        if ymin >= ymax:
            raise ValueError(
                "The value of ymin must be strictly less than the " "value of ymax"
            )

        self._xmin = xmin
        self._ymin = ymin
        self._xmax = xmax
        self._ymax = ymax

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
