import numpy.testing as npt
import pytest
from hypothesis import given
from unittest import TestCase

from stylo.domain.square import UnitSquare
from stylo.domain.transforms.translation import Translation
from tests.helpers.domain import BaseDomainTest
from tests.helpers.strategies import dimension, real


@pytest.mark.domain
class TestTranslate(TestCase, BaseDomainTest):
    """Tests for the Translation class"""

    def setUp(self):

        # We just need any instance of the translation to test the interface
        # with, we'll get to the details ourselves in the test cases here.
        self.domain = Translation(UnitSquare(), 1, 1)

    @given(width=dimension, height=dimension, dx=real)
    def test_dx_affects_x_values(self, width, height, dx):
        """Ensure that the :code:`dx` shifts each value by the negative of the value
        given by the user so that the translation is intuitive. Also ensure that only
        the :code:`x` values are affected."""

        domain = UnitSquare()
        xs, ys = domain["xy"](width, height)

        translated = Translation(domain, dx=dx, dy=0)
        t_xs, t_ys = translated["xy"](width, height)

        # The y values should be unaffected.
        npt.assert_array_equal(ys, t_ys)

        difference = xs - t_xs
        npt.assert_array_equal(difference, -dx)

    @given(width=dimension, height=dimension, dy=real)
    def test_dy_affects_y_values(self, width, height, dy):
        """Ensure that the :code:`dy` shifts each value by the negative of the value
        given by the user so that the translation is intuitive. Also ensure that only
        the :code:`y` values are affected."""

        domain = UnitSquare()
        xs, ys = domain["xy"](width, height)

        translated = Translation(domain, dx=0, dy=dy)
        t_xs, t_ys = translated["xy"](width, height)

        # The x values should be unaffected
        npt.assert_array_equal(xs, t_xs)

        difference = ys - t_ys
        npt.assert_array_equal(difference, -dy)
