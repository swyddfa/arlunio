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
