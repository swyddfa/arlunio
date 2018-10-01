import pytest
import numpy as np
from unittest import TestCase
from hypothesis import given

from stylo.domain import UnitSquare
from stylo.shape import Circle, Shape
from stylo.shape.shape import InvertedShape, ANDedShape, ORedShape, XORedShape
from stylo.testing.strategies import dimension
from stylo.testing.shape import BaseShapeTest


class MyShape(Shape):
    """A shape that depends on something other than x and y. This should be replaced
    with a shape from the library when such a shape is available.
    """

    def draw(self):
        return lambda r, t: r < t


@pytest.mark.shape
class TestInvertedShape(TestCase, BaseShapeTest):
    """Tests for the :code:`InvertedShape` class."""

    def setUp(self):
        self.baseshape = Circle(0, 0, 0.8)
        self.shape = InvertedShape(self.baseshape)

        self.domain = UnitSquare()

    def test_exposes_parameters(self):
        """Ensure that the :code:`InvertedShape` class exposes the parameters defined
        by the underlying shape.
        """
        assert self.shape.parameters == self.baseshape.parameters

    @given(width=dimension, height=dimension)
    def test_shape_is_inverted(self, width, height):
        """Ensure that an :code:`InvertedShape` is inverted by checking that a shape
        anded with its inversion should be False everywhere.
        """

        mask = self.baseshape(self.domain, width, height)
        inverted_mask = self.shape(self.domain, width, height)

        assert np.logical_not(np.logical_and(mask, inverted_mask)).all()

    @given(width=dimension, height=dimension)
    def test_double_inversion(self, width, height):
        """Ensure that an inverted :code:`InvertedShape` is the same as the shape
        itself.
        """

        double_inversion = InvertedShape(self.shape)

        mask = self.baseshape(self.domain, width, height)
        inverted_mask = double_inversion(self.domain, width, height)

        assert (mask == inverted_mask).all()

    def test_draw_method(self):
        """Rightly or wrongly, :code:`InvertedShape` currently doesn't make use of the
        draw method. So we'll override and disable this test from the base class."""
        pass


@pytest.mark.shape
class TestANDedShape(TestCase, BaseShapeTest):
    """Tests for the :code:`ANDedShape` class."""

    def setUp(self):
        self.a = Circle(0, 0, 0.8)
        self.not_a = InvertedShape(self.a)
        self.b = MyShape()

        self.shape = ANDedShape(self.a, self.not_a)
        self.domain = UnitSquare()

    def test_exposes_parameters(self):
        """Ensure that the parameters needed to define both a and b are exposed."""

        composite = ANDedShape(self.a, self.b)

        for p in self.a.parameters:
            assert p in composite.parameters, "Expected parameter: {}".format(p)

        for p in self.b.parameters:
            assert p in composite.parameters, "Expected parameter: {}".format(p)

    @given(width=dimension, height=dimension)
    def test_shapes_are_anded(self, width, height):
        """Ensure that the shapes are anded together. This is done by checking that the
        circle and its inversion results in False everywhere."""

        mask = self.shape(self.domain, width, height)

        assert np.logical_not(mask).all()

    def test_draw_method(self):
        """Rightly or wrongly, :code:`ANDedShape` currently doesn't make use of the
        draw method. So we'll override and disable this test from the base class."""
        pass


@pytest.mark.shape
class TestORedShape(TestCase, BaseShapeTest):
    """Tests for the :code:`ORedShape` class."""

    def setUp(self):
        self.a = Circle(0, 0, 0.8)
        self.not_a = InvertedShape(self.a)
        self.b = MyShape()

        self.shape = ORedShape(self.a, self.not_a)
        self.domain = UnitSquare()

    def test_exposes_parameters(self):
        """Ensure that the parameters needed to define both a and b are exposed."""

        composite = ORedShape(self.a, self.b)

        for p in self.a.parameters:
            assert p in composite.parameters, "Expected parameter: {}".format(p)

        for p in self.b.parameters:
            assert p in composite.parameters, "Expected parameter: {}".format(p)

    @given(width=dimension, height=dimension)
    def test_shapes_are_ored(self, width, height):
        """Ensure that the shapes are ored together. This is done by checking that the
        circle and its inversion results in True everywhere."""

        mask = self.shape(self.domain, width, height)

        assert mask.all()

    def test_draw_method(self):
        """Rightly or wrongly, :code:`ORedShape` currently doesn't make use of the
        draw method. So we'll override and disable this test from the base class."""
        pass


@pytest.mark.shape
class TestXORedShape(TestCase, BaseShapeTest):
    """Tests for the :code:`XORedShape` class."""

    def setUp(self):
        self.a = Circle(0, 0, 0.8)
        self.not_a = InvertedShape(self.a)
        self.b = MyShape()

        self.shape = XORedShape(self.a, self.not_a)
        self.domain = UnitSquare()

    def test_exposes_parameters(self):
        """Ensure that the parameters needed to define both a and b are exposed."""

        composite = XORedShape(self.a, self.b)

        for p in self.a.parameters:
            assert p in composite.parameters, "Expected parameter: {}".format(p)

        for p in self.b.parameters:
            assert p in composite.parameters, "Expected parameter: {}".format(p)

    @given(width=dimension, height=dimension)
    def test_shapes_are_xored(self, width, height):
        """Ensure that the shapes are xored together. This is done by checking that the
        circle and its inversion results in True everywhere."""

        mask = self.shape(self.domain, width, height)

        assert mask.all()

    @given(width=dimension, height=dimension)
    def test_shapes_are_xored_part2(self, width, height):
        """Ensure that the shapes are xored together. This is done by checking that the
        circle and itself results in False everywhere."""

        composite = XORedShape(self.a, self.a)
        mask = composite(self.domain, width, height)

        assert np.logical_not(mask).all()

    def test_draw_method(self):
        """Rightly xor wrongly, :code:`XORedShape` currently doesn't make use of the
        draw method. So we'll override and disable this test from the base class."""
        pass
