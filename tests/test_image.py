import unittest.mock as mock

import numpy as np
import PIL.Image as PImage
import py.test
from hypothesis import given
from hypothesis import settings

import arlunio.image as image
import arlunio.testing as T


@given(width=T.dimension, height=T.dimension)
def test_encode_decode(width, height):
    """Ensure that if we encode an image, then decode it we end up with the same
    thing."""

    expected = image.new((width, height), color="red")
    actual = image.decode(image.encode(expected))

    assert expected == actual


@py.test.mark.parametrize(
    "args, kwargs, pil_args, pil_kwargs",
    [
        (((120, 120),), {}, ("RGBA", (120, 120)), {}),
        ((120, 120), {}, ("RGBA", (120, 120)), {}),
        (((120, 120),), {"mode": "L"}, ("L", (120, 120)), {}),
        ((120, 120), {"mode": "L"}, ("L", (120, 120)), {}),
        (((120, 120),), {"color": "red"}, ("RGBA", (120, 120)), {"color": "red"}),
        ((120, 120), {"color": "red"}, ("RGBA", (120, 120)), {"color": "red"}),
    ],
)
def test_new_image(args, kwargs, pil_args, pil_kwargs):
    """Ensure that we wrap pillow's new image function correctly."""

    expected = PImage.new(*pil_args, **pil_kwargs)
    assert image.new(*args, **kwargs) == image.Image(expected)


@py.test.mark.parametrize(
    "args, kwargs, message", [((120,), {}, "must specify a width and a height")]
)
def test_new_image_validation(args, kwargs, message):
    """Ensure that the new image function performs some basic validation on its
    input."""

    with py.test.raises(ValueError) as err:
        image.new(*args, **kwargs)

    assert message in str(err.value)


class TestImage:
    """Tests for our image class"""

    @py.test.mark.parametrize("name", ["copy", "_repr_png_"])
    def test_pil_method_passthrough(self, name):
        """We're not here to test pillow, but we should make sure we're using
        it correctly"""

        m_func = mock.MagicMock()
        img = image.new((4, 4), color="red", mode="RGB")

        setattr(img.img, name, m_func)
        getattr(img, name)()

        m_func.assert_called_once()

    @py.test.mark.parametrize(
        "name,args,kwargs",
        [
            ("alpha_composite", (1, 2, 3), {"a": "a", "b": "b"}),
            ("save", (1, 2, 3), {"a": "a", "b": "b"}),
            ("paste", (1, 2, 3), {"a": "a", "b": "b"}),
        ],
    )
    def test_pil_method_args_passthrough(self, name, args, kwargs):
        """We're not here to test pillow, but we should check to make sure we are using
        it correctly."""

        m_func = mock.MagicMock()
        img = image.new((4, 4), color="red", mode="RGB")

        setattr(img.img, name, m_func)
        getattr(img, name)(*args, **kwargs)

        m_func.assert_called_with(*args, **kwargs)

    @given(width=T.dimension, height=T.dimension)
    def test_size_property(self, width, height):
        """Ensure that we expose the size property correctly."""

        p_img = PImage.new("RGB", (width, height))
        img = image.Image(p_img)

        assert img.size == p_img.size

    @given(width=T.dimension, height=T.dimension)
    def test_add(self, width, height):
        """Ensure that 2 images can be added together, where adding is the same as an
        alpha_composite."""

        a = image.new((width, height), color="black")
        b = image.new((width // 2, height), color="red")

        c = a + b
        assert c is not a, "Addition should return a new image object"

        d = a.copy()
        d.alpha_composite(b)

        assert c == d


class TestColorramp:
    """Tests for the image.colorramp function."""

    def test_with_defaults(self):
        """Ensure that the colorramp method chooses sensible defaults."""

        values = np.array([[0.0, 0.5], [0.75, 1.0]])
        img = image.colorramp(values)

        pix = np.array(
            [
                [[0, 0, 0, 255], [127, 127, 127, 255]],
                [[191, 191, 191, 255], [255, 255, 255, 255]],
            ],
            dtype=np.uint8,
        )

        assert (np.asarray(img) == pix).all()

    def test_colorramp(self):
        """Ensure that the colorramp parses the colors it is given."""

        values = np.array([[0.0, 0.5], [0.75, 1.0]])
        img = image.colorramp(values, start="#f00", stop="#0f0")

        pix = np.array(
            [
                [[255, 0, 0, 255], [127, 127, 0, 255]],
                [[63, 191, 0, 255], [0, 255, 0, 255]],
            ],
            dtype=np.uint8,
        )

        assert (np.asarray(img) == pix).all()


class TestFill:
    """Tests for the image.fill function."""

    @settings(max_examples=50)
    @given(mask=T.mask)
    def test_with_defaults(self, mask):
        """Ensure that the fill method chooses sensible defaults."""

        img = image.fill(mask)
        expected = np.full((*mask.shape, 4), (0, 0, 0, 0))

        if mask.any():
            expected[mask] = (0, 0, 0, 255)

        assert (np.asarray(img) == expected).all()

    @py.test.mark.parametrize(
        "fg,fgval,bg,bgval",
        [
            ("red", (255, 0, 0, 255), "black", (0, 0, 0, 255)),
            ("#ff0", (255, 255, 0, 255), "#00f", (0, 0, 255, 255)),
            ("#f0f0", (255, 0, 255, 0), "#0f0f", (0, 255, 0, 255)),
            ("#ff00ff", (255, 0, 255, 255), "#ffff00", (255, 255, 0, 255)),
            ("#00ff00ff", (0, 255, 0, 255), "#ffff0000", (255, 255, 0, 0)),
        ],
    )
    def test_with_colors(self, fg, fgval, bg, bgval):
        """Ensure that the fill method can handles various color specifications."""

        mask = np.array([[False, True], [True, False]])
        img = image.fill(mask, foreground=fg, background=bg)

        expected = np.full((*mask.shape, 4), bgval)

        if mask.any():
            expected[mask] = fgval

        assert (np.asarray(img) == expected).all()

    def test_fill_existing_rgb_image(self):
        """Ensure that the fill method can use an existing RGB image."""

        img = image.new((2, 2), color="white", mode="RGB")
        mask = np.array([[True, True], [False, False]])

        new_image = image.fill(mask, image=img)
        assert image != new_image, "Function should return a new image"

        expected = np.full((*mask.shape, 3), 255)
        expected[mask] = (0, 0, 0)

        assert (np.asarray(new_image) == expected).all()

    def test_fill_existing_rgba_image(self):
        """Ensure that the fill method can use an existing RGBA image."""

        img = image.new((2, 2), color="white")
        mask = np.array([[True, True], [False, False]])

        new_image = image.fill(mask, image=img)
        assert image != new_image, "Function should return a new image"

        expected = np.full((*mask.shape, 4), 255)
        expected[mask] = (0, 0, 0, 255)

        assert (np.asarray(new_image) == expected).all()
