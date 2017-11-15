from pytest import raises
from hypothesis import given
from hypothesis.strategies import integers, tuples


import numpy as np
import numpy.random as npr
from stylo.image import Image


dimension = integers(min_value=2, max_value=5000)
smalldim = integers(min_value=2, max_value=256)
colvalue = integers(min_value=0, max_value=255)
rgb = tuples(colvalue, colvalue, colvalue)
rgba = tuples(colvalue, colvalue, colvalue, colvalue)


class TestInit(object):

    @given(width=smalldim, height=smalldim)
    def test_with_width_height(self, width, height):

        img = Image(width, height)

        assert img.pixels.shape == (height, width, 4)
        assert img.pixels.dtype == np.uint8

        unique = np.unique(img.pixels)
        assert unique.shape == (1,)
        assert (unique == [(255, 255, 255, 255)]).all()


    @given(width=smalldim, height=smalldim, background=rgba)
    def test_with_width_height_rgba_background(self, width, height, background):

        img = Image(width, height, background=background)

        assert img.pixels.shape == (height, width, 4)
        assert img.pixels.dtype == np.uint8

        unique = np.unique(img.pixels, axis=0)
        unique = np.unique(unique, axis=1).flatten()
        assert unique.shape == (4,)
        assert (unique == [background]).all()

    @given(width=smalldim, height=smalldim, color=rgb)
    def test_with_width_height_rgb_background(self, width, height, color):

        img = Image(width, height, background=color)

        assert img.pixels.shape == (height, width, 4)
        assert img.pixels.dtype == np.uint8

        unique = np.unique(img.pixels, axis=0)
        unique = np.unique(unique, axis=1).flatten()
        assert unique.shape == (4,)

        background = (*color, 255)
        assert (unique == [background]).all()


    @given(width=smalldim, height=smalldim)
    def test_with_pixels(self, width, height):

        px = npr.randint(0, 255, (height, width, 4), dtype=np.uint8)
        img = Image(pixels=px)

        assert img.pixels.shape == (height, width, 4)
        assert (img.pixels == px).all()

        img = Image.fromarray(px)

        assert img.pixels.shape == (height, width, 4)
        assert (img.pixels == px).all()


    def test_with_bad_values(self):

        with raises(ValueError) as err:
            img = Image()

        assert 'specify a width and height' in str(err.value)

        with raises(ValueError) as err:
            img = Image(width=12)

        assert 'specify a width and height' in str(err.value)

        with raises(ValueError) as err:
            img = Image(height=12)

        assert 'specify a width and height' in str(err.value)


    @given(width=smalldim, height=smalldim)
    def test_with_bad_pixels(self, width, height):

        px = npr.randint(0, 255, (height, width), dtype=np.uint8)

        with raises(ValueError) as err:
            img = Image(pixels=px)

        assert 'must have shape:' in str(err.value)

        px = npr.randint(0, 255, (height, width, 5), dtype=np.uint8)

        with raises(ValueError) as err:
            img = Image(pixels=px)

        assert 'must have shape:' in str(err.value)


class TestProperties(object):

    @given(width=smalldim, height=smalldim)
    def test_repr(self, width, height):

        img = Image(width, height)
        assert repr(img) == '%ix%i Image' % (width, height)

    @given(width=smalldim, height=smalldim, color=rgb)
    def test_color_property(self, width, height, color):

        img = Image(width, height, background=color)

        colors = img.color
        assert colors.shape == (height, width, 3)

        unique = np.unique(colors, axis=0)
        unique = np.unique(unique, axis=1).flatten()
        assert unique.shape == (3,)

        assert (unique == [color]).all()

    @given(width=smalldim, height=smalldim, color=rgb)
    def test_set_color_property(self, width, height, color):

        img = Image(width, height)

        unique = np.unique(img.color, axis=0)
        unique = np.unique(unique, axis=1).flatten()
        assert (unique == [255, 255, 255]).all()

        img.color = color

        unique = np.unique(img.color, axis=0)
        unique = np.unique(unique, axis=1).flatten()
        assert (unique == color).all()

    def test_color_property_with_bad_values(self):

        img = Image(4, 4)

        unique = np.unique(img.color, axis=0)
        unique = np.unique(unique, axis=1).flatten()
        assert (unique == [255, 255, 255]).all()

        with raises(ValueError) as err:
            img.color = [2, 3]

        assert 'For more details' in str(err.value)

        unique = np.unique(img.color, axis=0)
        unique = np.unique(unique, axis=1).flatten()
        assert (unique == [255, 255, 255]).all()


    @given(width=smalldim, height=smalldim, color=rgb)
    def test_red_property(self, width, height, color):

        img = Image(width, height, background=color)

        reds = img.red
        assert reds.shape == (height, width,)

        unique = np.unique(reds, axis=0)
        unique = np.unique(unique, axis=1).flatten()
        assert unique.shape == (1,)

        assert (unique == color[0]).all()

    @given(width=smalldim, height=smalldim, color=colvalue)
    def test_set_red_property(self, width, height, color):

        img = Image(width, height)

        unique = np.unique(img.red, axis=0)
        unique = np.unique(unique, axis=1).flatten()
        assert (unique == [255]).all()

        img.red = color

        unique = np.unique(img.red, axis=0)
        unique = np.unique(unique, axis=1).flatten()
        assert (unique == color).all()

    @given(width=smalldim, height=smalldim, color=rgb)
    def test_green_property(self, width, height, color):

        img = Image(width, height, background=color)

        greens = img.green
        assert greens.shape == (height, width,)

        unique = np.unique(greens, axis=0)
        unique = np.unique(unique, axis=1).flatten()
        assert unique.shape == (1,)

        assert (unique == color[1]).all()

    @given(width=smalldim, height=smalldim, color=colvalue)
    def test_set_green_property(self, width, height, color):

        img = Image(width, height)

        unique = np.unique(img.green, axis=0)
        unique = np.unique(unique, axis=1).flatten()
        assert (unique == [255]).all()

        img.green = color

        unique = np.unique(img.green, axis=0)
        unique = np.unique(unique, axis=1).flatten()
        assert (unique == color).all()

    @given(width=smalldim, height=smalldim, color=rgb)
    def test_blue_property(self, width, height, color):

        img = Image(width, height, background=color)

        blues = img.blue
        assert blues.shape == (height, width,)

        unique = np.unique(blues, axis=0)
        unique = np.unique(unique, axis=1).flatten()
        assert unique.shape == (1,)

        assert (unique == color[2]).all()

    @given(width=smalldim, height=smalldim, color=colvalue)
    def test_set_blue_property(self, width, height, color):

        img = Image(width, height)

        unique = np.unique(img.blue, axis=0)
        unique = np.unique(unique, axis=1).flatten()
        assert (unique == [255]).all()

        img.blue = color

        unique = np.unique(img.blue, axis=0)
        unique = np.unique(unique, axis=1).flatten()
        assert (unique == color).all()

    @given(width=smalldim, height=smalldim, color=rgba)
    def test_alpha_property(self, width, height, color):

        img = Image(width, height, background=color)

        alphas = img.alpha
        assert alphas.shape == (height, width,)

        unique = np.unique(alphas, axis=0)
        unique = np.unique(unique, axis=1).flatten()
        assert unique.shape == (1,)

        assert (unique == color[3]).all()

    @given(width=smalldim, height=smalldim, color=colvalue)
    def test_set_alpha_property(self, width, height, color):

        img = Image(width, height)

        unique = np.unique(img.alpha, axis=0)
        unique = np.unique(unique, axis=1).flatten()
        assert (unique == [255]).all()

        img.alpha = color

        unique = np.unique(img.alpha, axis=0)
        unique = np.unique(unique, axis=1).flatten()
        assert (unique == color).all()


@given(index=integers(min_value=4, max_value=512))
def test_getitem_pixels(index):

    img = Image(512, 512)

    # Test that slicing by x works as expected
    sliced_x = img[:index]

    assert isinstance(sliced_x, (Image,))
    assert sliced_x.width == index
    assert sliced_x.height == 512

    # Test that slicing by y works as expected
    sliced_y = img[:, :index]

    assert isinstance(sliced_y, (Image,))
    assert sliced_y.width == 512
    assert sliced_y.height == index

    # Test that slicing by both works as expected
    sliced_both = img[:index, :index]

    assert isinstance(sliced_both, (Image,))
    assert sliced_both.width == index
    assert sliced_both.height == index

    # As a further test ensure that the smaller images
    # point back to subsets of the original pixel
    # data
    sliced_both[:, :] = (255, 0, 0, 255)

    assert (img.pixels[:index, :index] == sliced_both.pixels).all()
    assert (img.pixels[index:, index:] == (255, 255, 255, 255)).all()
