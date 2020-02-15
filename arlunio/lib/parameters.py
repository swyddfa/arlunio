import arlunio as ar
import numpy as np


@ar.definition
def X(width, height, *, x0=0, scale=1, stretch=False):
    """Cartesian :math:`x` coordinates.

    :param x0: Shift the :math:`x` coordinates by :code:`x0`
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

    return x - x0


@ar.definition
def Y(width, height, *, y0=0, scale=1, stretch=False):
    """Cartesian :math:`y` coordinates.

    :param y0: Shift the :math:`y` coordinates by :code:`y0`
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

    return y - y0


@ar.definition
def R(x: X, y: Y):
    """Polar :math:`r` coordinates."""
    return np.sqrt(x * x + y * y)


@ar.definition
def T(x: X, y: Y, *, t0=0):
    """Polar, :math:`t` coordinates."""
    t = np.arctan2(y, x)
    return t - t0
