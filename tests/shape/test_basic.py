import pytest
from unittest import TestCase

from stylo.shape import Ellipse, Circle, Rectangle, Square
from stylo.testing.shape import BaseShapeTest


@pytest.mark.shape
class TestEllipse(TestCase, BaseShapeTest):
    """Tests for the :code:`Ellipse` shape."""

    def setUp(self):
        self.shape = Ellipse(0, 0, 1 / 2, 1 / 3, 0.6)


@pytest.mark.shape
class TestCircle(TestCase, BaseShapeTest):
    """Tests for the :code:`Circle` shape."""

    def setUp(self):
        self.shape = Circle(0, 0, 0.5)


@pytest.mark.shape
class TestRectangle(TestCase, BaseShapeTest):
    """Tests for the :code:`Rectangle` shape."""

    def setUp(self):
        self.shape = Rectangle(0, 0, 0.6, 0.3)


@pytest.mark.shape
class TestSquare(TestCase, BaseShapeTest):
    """Tests for the :code:`Square` shape."""

    def setUp(self):
        self.shape = Square(0, 0, 0.75)
