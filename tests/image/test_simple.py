import pytest
from unittest import TestCase

from stylo.shape import Circle
from stylo.color import FillColor
from stylo.image import SimpleImage
from stylo.testing.image import BaseImageTest


@pytest.mark.image
class TestSimpleImage(TestCase, BaseImageTest):
    """Tests for the :code:`SimpleImage` object."""

    def setUp(self):
        self.image = SimpleImage(Circle(0, 0, 0.9), FillColor())
