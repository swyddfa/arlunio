import numpy as np

from stylo.domain import RealDomain
from stylo.domain.helpers import PolarConversion
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

    def _get_x(self):
        def mk_xs(width, height):
            xs = np.linspace(self.xmin, self.xmax, width)
            xs = np.array([xs for _ in range(height)])

            return xs

        return mk_xs

    def _get_y(self):
        def mk_ys(width, height):
            ys = np.linspace(self.ymax, self.ymin, height)
            ys = np.array([ys for _ in range(width)])
            ys = ys.transpose()

            return ys

        return mk_ys


def get_real_domain(width, height, scale=2):
    """Given the width and height for an image return a rectangular domain with
    appropriate bounds for the image's aspect ratio.

    So that shapes are not distorted when mapped onto non-square images the domain they
    are mapped onto needs to match the aspect ratio of the image otherwise the shape
    will be distorted in some way.

    This function will construct a RectangularDomain domain with :math:`(0, 0)` at the
    centre of the image, the overall size of the domain can be controlled with the
    :code:`scale` parameter

    :param width: The width of the image in pixels
    :param height: The height of the image in pixels
    :param scale: This constrols the size of the domain and corresponds to the length of
                  the interval :math:`[ymin, ymax]`

    :type width: int
    :type height: int
    :type scale: float

    :returns: An appropriately sized domain.
    :rtype: RectangularDomain
    """

    if height <= 0:
        raise ValueError("The height of the image must be a positive number.")

    if width <= 0:
        raise ValueError("The width of the image must be a positive number.")

    if scale <= 0:
        raise ValueError("The scale of the image must be strictly positive.")

    aspect_ratio = width / height

    ylength = scale / 2
    xlength = ylength * aspect_ratio

    ymin, ymax = -ylength, ylength
    xmin, xmax = -xlength, xlength

    return RectangularDomain(xmin, xmax, ymin, ymax)
