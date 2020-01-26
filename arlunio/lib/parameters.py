import arlunio as ar
import numpy as np


def xs(width, height, scale=1):
    """Implementation of the `x` parameter."""
    ratio = width / height
    length = scale * ratio

    x = np.linspace(-length, length, width)
    x = np.array([x for _ in range(height)])

    return x


def ys(width, height, scale=1):
    """Implementation of the `y` parameter."""

    y = np.linspace(scale, -scale, height)
    y = np.array([y for _ in range(width)]).transpose()

    return y


def rs(width, height, scale=1):
    """Implementation for the `r` parameter"""

    x = xs(width, height, scale)
    y = ys(width, height, scale)

    return np.sqrt(x * x + y * y)


def ts(width, height, scale=1):
    """Implementation for the `t` parameter."""

    x = xs(width, height, scale)
    y = ys(width, height, scale)

    return np.arctan2(y, x)


@ar.parameter
def X(width, height, *, scale=1, stretch=False):
    """Cartesian :math:`x` coordinates.

    :param scale: Controls the size of the extreme values in the grid.
    :param stretch: If :code:`True` and the image is wider than it is tall then the grid
                    will be stretched so that :code:`x = scale` falls on the image
                    border.
    """
    ratio = width / height

    if not stretch and ratio > 1:
        scale = scale * ratio

    x = np.linspace(-scale, scale, width)
    x = np.array([x for _ in range(height)])

    return x


@ar.parameter
def Y(width, height, *, scale=1, stretch=False):
    """Cartesian :math:`y` coordinates.

    :param scale: Controls the size of the extreme values in the grid
    :param stretch: If :code:`True` and the image is taller than it is wide then the
                    grid will be stretched so that :code:`y = scale` falls on the image
                    border
    """
    ratio = height / width

    if not stretch and ratio > 1:
        scale = scale * ratio

    y = np.linspace(scale, -scale, height)
    y = np.array([y for _ in range(width)]).transpose()

    return y


@ar.parameter
def R(x: X, y: Y):
    """Polar :math:`r` coordinates."""
    return np.sqrt(x * x + y * y)


@ar.parameter
def T(x: X, y: Y, *, t0=0):
    """Polar, :math:`t` coordinates."""
    t = np.arctan2(y, x)
    return t - t0
