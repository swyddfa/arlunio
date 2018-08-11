from unittest import TestCase

import pytest
import numpy as np
import numpy.testing as npt

from hypothesis import given
from hypothesis.strategies import integers, tuples

from stylo.color.rgb import RGB8

# Some useful strategies
dim = integers(min_value=2, max_value=256)
bit8 = integers(min_value=0, max_value=255)
rgb8 = tuples(bit8, bit8, bit8)


@pytest.mark.color
class TestRGB8(TestCase):
    @given(width=dim, height=dim)
    def test_init_width_height(self, width, height):
        """Test that the RGB8 ColorData implementation initialises correctly
        when just given a width and height."""

        color = RGB8(width, height)

        self.assertEquals(width, color._data.shape[1])
        self.assertEquals(height, color._data.shape[0])

        unique = np.unique(color._data)
        self.assertEquals(np.array(0), unique)

    @given(width=dim, height=dim, fill=rgb8)
    def test_init_with_fill(self, width, height, fill):
        """Test that the init function handles a fill color as expected."""

        color = RGB8(width, height, fill=fill)

        self.assertEquals(width, color._data.shape[1])
        self.assertEquals(height, color._data.shape[0])

        unique = np.unique(color._data, axis=0)
        unique = np.unique(unique, axis=1)
        unique.shape = (3,)

        npt.assert_equal(unique, fill)

    def test_bitdepth(self):
        """Check that it defines the bitdepth property correctly."""

        color = RGB8(12, 12)
        self.assertEquals(8, color.bitdepth)

    @given(width=dim, height=dim)
    def test_width_height_properties(self, width, height):
        """Test that the width and height properties report correctly."""

        color = RGB8(width, height)

        self.assertEquals(width, color.width)
        self.assertEquals(height, color.height)

    @given(width=dim, height=dim, col=bit8)
    def test_red_property(self, width, height, col):
        """Test that the red property returns the correct channel."""

        fill = (col, 0, 0)
        color = RGB8(width, height, fill=fill)

        reds = color.red
        self.assertEquals((height, width), reds.shape)

        unique = np.unique(reds)
        npt.assert_equal(np.array(col), unique)

    @given(width=dim, height=dim, col=bit8)
    def test_green_property(self, width, height, col):
        """Test that the green property returns the correct channel."""

        fill = (0, col, 0)
        color = RGB8(width, height, fill=fill)

        greens = color.green
        self.assertEquals((height, width), greens.shape)

        unique = np.unique(greens)
        npt.assert_equal(np.array(col), unique)

    @given(width=dim, height=dim, col=bit8)
    def test_blue_property(self, width, height, col):
        """Test that the blue property returns the correct channel."""

        fill = (0, 0, col)
        color = RGB8(width, height, fill=fill)

        blues = color.blue
        self.assertEquals((height, width), blues.shape)

        unique = np.unique(blues)
        npt.assert_equal(np.array(col), unique)

    @given(width=dim, height=dim, fill=rgb8)
    def test_alpha_property(self, width, height, fill):
        """Test that the alpha property is always opaque"""

        color = RGB8(width, height, fill=fill)
        alphas = color.alpha

        self.assertEquals((height, width), alphas.shape)

        unique = np.unique(alphas)
        npt.assert_equal(np.array(255), unique)
