from unittest import TestCase

import pytest

from hypothesis import given
from hypothesis.strategies import integers

from stylo.color.mono import Mono

# Some useful strategies
dim = integers(min_value=2, max_value=256)


@pytest.mark.color
class TestMono(TestCase):

    @given(width=dim, height=dim)
    def test_init_width_height(self, width, height):
        """Test that the RGBA8 ColorData implementation initialises correctly
        when just given a width and height."""

        color = Mono(width, height)

        self.assertEquals(width, color._data.shape[1])
        self.assertEquals(height, color._data.shape[0])

        assert not color._data.all()

    @given(width=dim, height=dim)
    def test_init_with_fill(self, width, height):
        """Test that the init function handles a fill color as expected."""

        color = Mono(width, height, fill=True)

        self.assertEquals(width, color._data.shape[1])
        self.assertEquals(height, color._data.shape[0])

        assert color._data.all()

    def test_bitdepth(self):
        """Check that it defines the bitdepth property correctly."""

        color = Mono(12, 12)
        self.assertEquals(1, color.bitdepth)

    @given(width=dim, height=dim)
    def test_width_height_properties(self, width, height):
        """Test that the width and height properties report correctly."""

        color = Mono(width, height)

        self.assertEquals(width, color.width)
        self.assertEquals(height, color.height)

    @given(width=dim, height=dim)
    def test_red_property(self, width, height):
        """Test that the red property returns the correct channel."""

        color = Mono(width, height, fill=True)

        reds = color.red
        self.assertEquals((height, width), reds.shape)
        assert reds.all()

    @given(width=dim, height=dim)
    def test_green_property(self, width, height):
        """Test that the green property returns the correct channel."""

        color = Mono(width, height, fill=True)

        greens = color.green
        self.assertEquals((height, width), greens.shape)
        assert greens.all()

    @given(width=dim, height=dim)
    def test_blue_property(self, width, height):
        """Test that the blue property returns the correct channel."""

        color = Mono(width, height, fill=True)

        blues = color.blue
        self.assertEquals((height, width), blues.shape)
        assert blues.all()

    @given(width=dim, height=dim)
    def test_alpha_property(self, width, height):
        """Test that the alpha property is always opaque"""

        color = Mono(width, height, fill=True)
        alphas = color.alpha

        self.assertEquals((height, width), alphas.shape)
        assert alphas.all()
