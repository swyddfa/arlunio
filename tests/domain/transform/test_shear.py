import pytest
import numpy.testing as npt
from hypothesis import given
from unittest import TestCase

from stylo.domain import UnitSquare
from stylo.domain.transform.shear import HorizontalShear, VerticalShear
from stylo.testing.domain import BaseRealDomainTest
from stylo.testing.strategies import real, dimension


@pytest.mark.domain
class TestHorizontalShear(TestCase, BaseRealDomainTest):
    """Tests for the horizontal shear class."""

    def setUp(self):
        self.domain = HorizontalShear(UnitSquare(), 0.5)

    @given(width=dimension, height=dimension, k=real)
    def test_k_affects_x_values(self, width, height, k):
        """Ensure that :code:`k` shears the x values by the factor -ky so that the
        user's intuition is maintained. Also ensure that the y values are unaffected."""

        domain = UnitSquare()
        xs, ys = domain["xy"](width, height)

        sheared = HorizontalShear(domain, k)
        t_xs, t_ys = sheared["xy"](width, height)

        # Y values should be unchanged
        npt.assert_array_equal(ys, t_ys)

        # X values should only differ by -ky
        difference = t_xs - xs
        npt.assert_almost_equal(difference, -k * ys)


@pytest.mark.domain
class TestVerticalShear(TestCase, BaseRealDomainTest):
    """Tests for the vertical shear class."""

    def setUp(self):
        self.domain = VerticalShear(UnitSquare(), 0.5)

    @given(width=dimension, height=dimension, k=real)
    def test_k_affects_y_values(self, width, height, k):
        """Ensure that :code:`k` shears the y values by a factor of -kx so that the
        user's intuition is maintained. Also ensure that the x values are unaffected."""

        domain = UnitSquare()
        xs, ys = domain["xy"](width, height)

        sheared = VerticalShear(domain, k)
        t_xs, t_ys = sheared["xy"](width, height)

        # X values should be unchanged
        npt.assert_array_equal(xs, t_xs)

        # Y values should only differ by -kx
        difference = t_ys - ys
        npt.assert_almost_equal(difference, -k * xs)
