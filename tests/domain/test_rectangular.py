from unittest import TestCase

import pytest
from hypothesis import given, assume
from tests.helpers.strategies import real
from tests.helpers.domain import BaseDomainTest

from stylo.domain.rectangular import RectangularDomain


@pytest.mark.domain
class TestRectangularDomain(TestCase, BaseDomainTest):
    """Tests for the RectangularDomain class"""

    def setUp(self):
        self.domain = RectangularDomain(-1, 1, -1, 1)

    @given(xmin=real, xmax=real)
    def test_init_checks_x_min_max(self, xmin, xmax):
        """Ensure that the __init__ method checks to see that the value
        of :code:`xmin < xmax`."""

        assume(xmax <= xmin)

        with pytest.raises(ValueError) as err:
            RectangularDomain(xmin, xmax, 0, 1)

        self.assertIn("must be strictly less than", str(err.value))
        self.assertIn("xmin", str(err.value))
        self.assertIn("xmax", str(err.value))

    @given(ymin=real, ymax=real)
    def test_init_checks_y_min_max(self, ymin, ymax):
        """Ensure that the __init__ method checks to see that the value
        of :code:`ymin < ymax`."""

        assume(ymax <= ymin)

        with pytest.raises(ValueError) as err:
            RectangularDomain(0, 1, ymin, ymax)

        self.assertIn("must be strictly less than", str(err.value))
        self.assertIn("ymin", str(err.value))
        self.assertIn("ymax", str(err.value))

    @given(xmin=real)
    def test_xmin_property(self, xmin):
        """Ensure that the :code:`xmin` property works as expected.

        The :code:`xmin` property should:

        - Return the value of :code:`xmin`
        - Be used to set a new value of :code:`xmin`
        """

        domain = RectangularDomain(xmin, xmin + 1, 0, 1)
        self.assertEqual(xmin, domain.xmin)

        domain.xmin = xmin - 2
        self.assertEqual(xmin - 2, domain.xmin)

    def test_xmin_property_checks_value(self):
        """Ensure that the :code:`xmin` property checks the value it is
        given to make sure it makes sense.

        The new value should:

        - Be a numeric value
        - Be strictly less than the current value of :code:`xmax`
        """

        domain = RectangularDomain(0, 1, 0, 1)

        with pytest.raises(TypeError) as err:
            domain.xmin = "String"

        self.assertIn("must be a number", str(err.value))

        with pytest.raises(ValueError) as err:
            domain.xmin = 10

        self.assertIn("must be strictly less than", str(err.value))