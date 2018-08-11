import pytest
import numpy as np
from hypothesis import given

from tests.helpers.strategies import dimension


class BaseDomainTest:
    """A base class to be used when testing domains.

    When creating your test case to test your :class:`Domain` implementation
    if you set declare it as follows

    .. code-block:: python

       from unittest import TestCase
       from tests.helpers.domain import BaseDomainTest

       class TestMyDomain(TestCase, BaseDomainTest):
           ...

    Also if you define an implementation of the :code:`setUp` method to
    set the :code:`domain` attribute on your class to be an instance of your
    domain implementation. For example

    .. code-block:: python

       class TestMyDomain(TestCase, BaseDomainTest):

           def setUp(self):
               self.domain = MyDomain()

    Then your class will be automatically tested to see if it conforms to the
    expected behavior of :code:`Domain` objects. This will allow you to focus
    on testing the aspects of the domain that are unique to your implementation.
    """

    @given(width=dimension, height=dimension)
    def test_x_property(self, width, height):
        """Ensure that the :code:`x` property works as expected.

        The :code:`x` property should:

        - Return a function in width and height.
        - When called this function should return a numpy array with the shape
          :code:`(height, width)`
        """

        xs = self.domain.x
        self.assertTrue(callable(xs), "The x property should return a function.")

        XS = xs(width, height)
        self.assertTrue(
            isinstance(XS, (np.ndarray,)), "The function should return a numpy array"
        )

        self.assertEqual(
            (height, width),
            XS.shape,
            "The resulting array should have shape (height, width)",
        )

    def test_x_property_read_only(self):
        """Ensure that the :code:`x` property is read only."""

        with pytest.raises(AttributeError) as err:
            self.domain.x = 2

        self.assertIn("can't set attribute", str(err.value))

    @given(width=dimension, height=dimension)
    def test_y_property(self, width, height):
        """Ensure that the :code:`y` property works as expected.

        The :code:`y` property should:

        - Return a function in width and height.
        - When this function is called it should return a numpy array
          with the shape :code:`(height, width)`
        """

        ys = self.domain.y
        self.assertTrue(callable(ys), "The y property should return a function.")

        YS = ys(width, height)
        self.assertTrue(
            isinstance(YS, (np.ndarray,)), "The function should return a numpy array"
        )

        self.assertEqual(
            (height, width),
            YS.shape,
            "The resulting array should have shape (height, width)",
        )

    def test_y_property_read_only(self):
        """Ensure that the :code:`y` property is read only."""

        with pytest.raises(AttributeError) as err:
            self.domain.y = 2

        self.assertIn("can't set attribute", str(err.value))

    @given(width=dimension, height=dimension)
    def test_r_property(self, width, height):
        """Ensure that the :code:`r` property works as expected.

        The :code:`r` property should:

        - Return a function in width and height.
        - When this function is called it should return a numpy array
          with the shape :code:`(height, width)`
        """

        rs = self.domain.r
        self.assertTrue(callable(rs), "The r property should return a function.")

        RS = rs(width, height)
        self.assertTrue(
            isinstance(RS, (np.ndarray,)), "The function should return a numpy array"
        )

        self.assertEqual(
            (height, width),
            RS.shape,
            "The resulting array should have shape (height, width)",
        )

    def test_r_property_read_only(self):
        """Ensure that the :code:`r` property is read only."""

        with pytest.raises(AttributeError) as err:
            self.domain.r = 2

        self.assertIn("can't set attribute", str(err.value))

    @given(width=dimension, height=dimension)
    def test_t_property(self, width, height):
        """Ensure that the :code:`t` property works as expected.

        The :code:`t` property should:

        - Return a function in width and height
        - When this function is called it should return a numpy array
          with the shape :code:`(height, width)`
        """

        ts = self.domain.t
        self.assertTrue(callable(ts), "The t property should return a function")

        TS = ts(width, height)
        self.assertTrue(
            isinstance(TS, (np.ndarray,)), "The function should return a numpy array"
        )

        self.assertEqual(
            (height, width),
            TS.shape,
            "The resulting array should have shape (height, width)",
        )

    def test_t_property_read_only(self):
        """Ensure that the :code:`t` property is read only."""

        with pytest.raises(AttributeError) as err:
            self.domain.t = 2

        self.assertIn("can't set attribute", str(err.value))
