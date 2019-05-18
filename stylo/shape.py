import enum
import logging
import pkg_resources

import numpy as np

from .image import Image


logger = logging.getLogger(__name__)


def xs(width, height, scale):
    """Implementation of the `x` parameter."""
    ratio = width / height
    length = (scale / 2) * ratio

    x = np.linspace(-length, length, width)
    x = np.array([x for _ in range(height)])

    return x


def ys(width, height, scale):
    """Implementation of the `y` parameter."""
    length = scale / 2

    y = np.linspace(length, -length, height)
    y = np.array([y for _ in range(width)]).transpose()

    return y


def rs(width, height, scale):
    """Implementation for the `r` parameter"""

    x = xs(width, height, scale)
    y = ys(width, height, scale)

    return np.sqrt(x * x + y * y)


def ts(width, height, scale):
    """Implementation for the `t` parameter."""

    x = xs(width, height, scale)
    y = ys(width, height, scale)

    return np.arctan2(y, x)


class Shape:
    """A shape, produces an image."""

    def __init__(self, domain=None, mask=None, color=None):
        self.domain = domain
        self.mask = mask
        self.color = color

    def __call__(self, width, height):

        domain = self.domain(width, height)
        mask = self.mask(**domain)
        pixels = self.color(mask)

        return Image(pixels)
