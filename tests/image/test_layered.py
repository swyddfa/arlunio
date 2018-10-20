import pytest
from unittest import TestCase

from stylo.shape import Circle
from stylo.color import FillColor
from stylo.image import LayeredImage
from stylo.testing.image import BaseImageTest


@pytest.mark.image
class TestLayeredImage(TestCase, BaseImageTest):
    """Tests for the :code:`LayeredImage` object."""

    def setUp(self):
        circle, black = Circle(0, 0, 0.9), FillColor()

        image = LayeredImage()
        image.add_layer(circle, black)

        self.image = image
