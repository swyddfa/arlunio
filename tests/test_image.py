import pytest
from hypothesis import given
from hypothesis.strategies import integers, tuples


import numpy as np
import numpy.random as npr
from mage.image import Image


dimension = integers(min_value=2, max_value=5000)
smalldim = integers(min_value=2, max_value=256)
colvalue = integers(min_value=0, max_value=255)
color = tuples(colvalue, colvalue, colvalue, colvalue)


@given(width=smalldim, height=smalldim)
def test_width_height_init(width, height):

    img = Image(width, height)

    assert img.pixels.shape == (height, width, 4)
    assert img.pixels.dtype == np.uint8

    unique = np.unique(img.pixels)
    assert unique.shape == (1,)
    assert (unique == [(255, 255, 255, 255)]).all()


@given(width=smalldim, height=smalldim, background=color)
def test_width_height_background_init(width, height, background):

    img = Image(width, height, background)

    assert img.pixels.shape == (height, width, 4)
    assert img.pixels.dtype == np.uint8

    unique = np.unique(img.pixels, axis=0)
    unique = np.unique(unique, axis=1).flatten()
    assert unique.shape == (4,)
    assert (unique == [background]).all()


@given(width=smalldim, height=smalldim)
def test_pixel_init(width, height):

    px = npr.randint(0, 255, (height, width, 4), dtype=np.uint8)
    img = Image(pixels=px)

    assert img.pixels.shape == (height, width, 4)
    assert (img.pixels == px).all()

    img = Image.fromarray(px)

    assert img.pixels.shape == (height, width, 4)
    assert (img.pixels == px).all()


def test_init_exceptions():

    with pytest.raises(ValueError) as err:
        img = Image()

    assert 'specify a width and height' in str(err.value)

    with pytest.raises(ValueError) as err:
        img = Image(width=12)

    assert 'specify a width and height' in str(err.value)

    with pytest.raises(ValueError) as err:
        img = Image(height=12)

    assert 'specify a width and height' in str(err.value)


@given(width=smalldim, height=smalldim)
def test_pixel_init_exceptions(width, height):

    px = npr.randint(0, 255, (height, width), dtype=np.uint8)

    with pytest.raises(ValueError) as err:
        img = Image(pixels=px)

    assert 'must have shape:' in str(err.value)

    px = npr.randint(0, 255, (height, width, 5), dtype=np.uint8)

    with pytest.raises(ValueError) as err:
        img = Image(pixels=px)

    assert 'must have shape:' in str(err.value)


@given(width=smalldim, height=smalldim)
def test_repr(width, height):

    img = Image(width, height)
    assert repr(img) == '%ix%i Image' % (width, height)


def test_getitem():

    img = Image(512, 512)
    assert isinstance(img[1:10], (Image,))
