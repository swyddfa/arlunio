import numpy as np
from hypothesis import given

from stylo.domain import UnitSquare, RealDomain
from stylo.testing.strategies import dimension
from stylo.utils import get_parameters


class BaseShapeTest:
    """A base class for testing :code:`Shape` implementations.

    When writing your test case for a new :code:`Shape` implementation you need to
    declare it as follows.

    .. code-block:: python

       from unittest import TestCase
       from stylo.testing.shape import BaseShapeTest

       class TestMyShape(TestCase, BaseShapeTest):
           ...

    .. note::

       The order in which you write the classes is *very* important.

    You also need to define the :code:`setUp` method to set the :code:`shape` attribute
    equal to an instance of your shape implementation.

    .. code-block:: python

       def setUp(self):
           self.shape = MyShape()

    Then in addition to any tests you write, your :code:`Shape` implementation will be
    automatically tested to see if it passes the checks defined below.
    """

    @given(width=dimension, height=dimension)
    def test_render_with_domain(self, width, height):
        """Ensure that a shape can be called with a domain and integers representing the
        width and height in pixels of an image. The result must:

        - Be numpy array
        - With shape :code:`(height, width)`
        - With elements of type bool.
        """
        domain = UnitSquare()
        mask = self.shape(domain, width, height)

        self.assertTrue(isinstance(mask, (np.ndarray,)), "Expected numpy array.")
        self.assertEqual((height, width), mask.shape)
        self.assertTrue(mask.dtype == np.bool, "Expected boolean array")

    @given(width=dimension, height=dimension)
    def test_render_with_args(self, width, height):
        """Ensure that a shape can be called with keyword arguments. Each of the
        arguments should be numpy arrays of the same shape with names corresponding to
        each of the coordinate names the shape is defined with. The result must:

        - Be a numpy array
        - With shape :code:`(height, width)`
        - With elements of type bool.
        """
        domain = UnitSquare()
        parameters = self.shape.parameters

        values = domain[parameters](width, height)
        params = {k: v for k, v in zip(parameters, values)}

        mask = self.shape(**params)

        self.assertTrue(isinstance(mask, (np.ndarray,)), "Expected numpy array.")
        self.assertEqual((height, width), mask.shape)
        self.assertTrue(mask.dtype == np.bool, "Expected boolean array.")

    def test_parameters_property(self):
        """Ensure that the :code:`parameters` property returns the coordinates that the
        shape is defined with. The parameters must

        - Be iterable
        - Be unique
        - Be declared on the :code:`RealDomain` interface.
        """

        coordinates = self.shape.parameters
        unique = set(coordinates)

        self.assertEqual(len(unique), len(coordinates))

        for c in coordinates:
            if c not in RealDomain._parameters:
                message = "{} is not a valid coordinate variable."
                raise ValueError(message.format(c))

    def test_draw_method(self):
        """Ensure that the :code:`draw` method returns a valid shape function. A shape
        function must

        - Be callable
        - Only take coordinate arguments defined in :code:`RealDomain`
        - These arguments must match those defined in the :code:`parameters` property.
        """

        method = self.shape.draw()

        self.assertTrue(callable(method), "Expected callable.")
        parameters = get_parameters(method)

        self.assertEqual(parameters, self.shape.parameters)

    def test_has_transforms(self):
        """Ensure that a shape has a :code:`_transforms` attribute that is equal to the
        empty list."""

        assert self.shape._transforms == []

    def test_add_transform(self):
        """Ensure that when transforms are added to the list that they are added to the
        front of the list."""

        shape = self.shape
        shape._add_transform(1)
        shape._add_transform(2)

        assert [2, 1] == shape._transforms

    def test_apply_transform_none(self):
        """Ensure that when a shape carries no transforms that the domain is returned
        untouched."""

        domain = UnitSquare()
        assert self.shape._apply_transform(domain) == domain

    def test_apply_transform(self):
        """Ensure that when a shape carries transforms that they are applied."""

        self.shape._add_transform(lambda n: 2 * n)
        self.shape._add_transform(lambda n: n + 1)

        assert 22 == self.shape._apply_transform(10)
