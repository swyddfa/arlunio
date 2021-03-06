import numpy as np
import numpy.testing as npt
import py.test
from hypothesis import assume
from hypothesis import given

import arlunio.testing as T
from arlunio.math import X
from arlunio.math import Y


@given(width=T.dimension, height=T.dimension)
def test_X_matches_dimension(width, height):
    """Ensure that the output shape matches the width and height of the image"""

    x = X()
    assert x(width=width, height=height).shape == (height, width)


@given(width=T.dimension, height=T.dimension)
def test_X_uniform_vertically(width, height):
    """Ensure that the output only varies in the x-direction"""

    x = X()
    xs = x(width=width, height=height)

    assert np.unique(xs, axis=0).shape == (1, width)


@given(width=T.dimension, height=T.dimension, scale=T.pve_num)
def test_X_adapts_to_image_ratio_by_default(width, height, scale):
    """Ensure that the output adapts to the aspect ratio of the image."""

    assume(width / height > 1)

    x = X(scale=scale)
    xs = x(width=width, height=height)

    assert width / height == py.test.approx(np.max(xs) / scale)


@given(width=T.dimension, height=T.dimension, scale=T.pve_num)
def test_X_fits_to_image_size_when_told(width, height, scale):
    """Ensure that the output fits to the size of the image when :code:`fit` property
    is set."""

    x = X(scale=scale, stretch=True)
    xs = x(width=width, height=height)

    assert np.max(xs) == scale


@given(width=T.dimension, height=T.dimension, offset=T.real_num)
def test_X_shifts_origin_accordingly(width, height, offset):
    """Ensure that the output has shifted the output according to the :code:`x0`
    property."""

    x1 = X()
    x2 = X(x0=offset)

    x1s = x1(width=width, height=height)
    x2s = x2(width=width, height=height)

    npt.assert_almost_equal(x1s - x2s, offset)


@given(width=T.dimension, height=T.dimension)
def test_Y_matches_dimension(width, height):
    """Ensure that the output shape matches the width and height of the image."""

    y = Y()
    ys = y(width=width, height=height)

    assert ys.shape == (height, width)


@given(width=T.dimension, height=T.dimension)
def test_Y_uniform_horizontally(width, height):
    """Ensure that the output only varies in the y direction"""

    y = Y()
    ys = y(width=width, height=height)

    assert np.unique(ys, axis=1).shape == (height, 1)


@given(width=T.dimension, height=T.dimension, scale=T.pve_num)
def test_Y_adapts_to_image_ratio_by_default(width, height, scale):
    """Ensure that the output adapts to the aspect ratio of the image"""

    assume(height / width > 1)

    y = Y(scale=scale)
    ys = y(width=width, height=height)

    assert height / width == py.test.approx(np.max(ys) / scale)


@given(width=T.dimension, height=T.dimension, scale=T.pve_num)
def test_Y_fits_to_image_size_when_told(width, height, scale):
    """Ensure that the output fits to the size of the image when :code:`fit` property
    is set."""

    y = Y(scale=scale, stretch=True)
    ys = y(width=width, height=height)

    assert np.max(ys) == scale


@given(width=T.dimension, height=T.dimension, offset=T.real_num)
def test_Y_shifts_origin_accordingly(width, height, offset):
    """Ensure that the output has shifted the output according to the :code:`y0`
    property."""

    y1 = Y()
    y2 = Y(y0=offset)

    y1s = y1(width=width, height=height)
    y2s = y2(width=width, height=height)

    npt.assert_almost_equal(y1s - y2s, offset)
