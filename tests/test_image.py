import unittest.mock as mock

import numpy as np
import py.test
from hypothesis import given
from hypothesis import settings

import arlunio.image as image
import arlunio.testing as T


@given(width=T.dimension, height=T.dimension)
def test_encode_decode(width, height):
    """Ensure that if we encode an image, then decode it we end up with the same
    thing."""

    expected = image.new("RGBA", (width, height), color="red")
    actual = image.decode(image.encode(expected))

    assert expected == actual


class TestImage:
    """Tests for our image class"""

    @py.test.mark.parametrize("name", ["copy", "_repr_png_"])
    def test_pil_method_passthrough(self, name):
        """We're not here to test pillow, but we should make sure we're using
        it correctly"""

        m_func = mock.MagicMock()
        img = image.new("RGB", (4, 4), color="red")

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
        img = image.new("RGB", (4, 4), color="red")

        setattr(img.img, name, m_func)
        getattr(img, name)(*args, **kwargs)

        m_func.assert_called_with(*args, **kwargs)

    @given(width=T.dimension, height=T.dimension)
    def test_add(self, width, height):
        """Ensure that 2 images can be added together, where adding is the same as an
        alpha_composite."""

        a = image.new("RGBA", (width, height), color="black")
        b = image.new("RGBA", (width // 2, height), color="red")

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

        img = image.new("RGB", (2, 2), color="white")
        mask = np.array([[True, True], [False, False]])

        new_image = image.fill(mask, image=img)
        assert image != new_image, "Function should return a new image"

        expected = np.full((*mask.shape, 3), 255)
        expected[mask] = (0, 0, 0)

        assert (np.asarray(new_image) == expected).all()

    def test_fill_existing_rgba_image(self):
        """Ensure that the fill method can use an existing RGBA image."""

        img = image.new("RGBA", (2, 2), color="white")
        mask = np.array([[True, True], [False, False]])

        new_image = image.fill(mask, image=img)
        assert image != new_image, "Function should return a new image"

        expected = np.full((*mask.shape, 4), 255)
        expected[mask] = (0, 0, 0, 255)

        assert (np.asarray(new_image) == expected).all()
