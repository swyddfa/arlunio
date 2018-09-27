from unittest import TestCase

from stylo.color import FillColor
from stylo.testing.color import BaseColorMapTest


class TestFillColor(TestCase, BaseColorMapTest):
    """Tests for the :code:`FillColor` colormap."""

    def setUp(self):
        self.colormap = FillColor()

    def test_init_no_args(self):
        """Ensure that if no arguments are given, then the color defaults to black."""

        fill = FillColor()
        self.assertEqual((0, 0, 0), fill.color)
