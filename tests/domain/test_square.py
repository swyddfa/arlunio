import pytest
from hypothesis import given, assume
from unittest import TestCase

from stylo.domain.square import SquareDomain, UnitSquare
from stylo.testing.domain import BaseRealDomainTest
from stylo.testing.strategies import real


@pytest.mark.domain
class TestSquareDomain(TestCase, BaseRealDomainTest):
    """Tests for the :code:`SquareDomain` class"""

    def setUp(self):
        self.domain = SquareDomain(-1, 1)

    @given(value=real)
    def test_xmin_property_sets_ymin(self, value):
        """Ensure that the :code:`xmin` property also sets the :code:`ymin`
        property to maintain the square aspect ratio."""
        assume(value < 1)

        domain = SquareDomain(-1, 1)
        domain.xmin = value

        self.assertEqual(value, domain.xmin)
        self.assertEqual(value, domain.ymin)

    @given(value=real)
    def test_ymin_property_sets_xmin(self, value):
        """Ensure that the :code:`ymin` property also sets the :code:`xmin`
        property to maintain the square aspect ratio."""

        assume(value < 1)

        domain = SquareDomain(-1, 1)
        domain.ymin = value

        self.assertEqual(value, domain.xmin)
        self.assertEqual(value, domain.ymin)

    @given(value=real)
    def test_xmax_property_sets_ymax(self, value):
        """Ensure that the :code:`xmax` property also sets the :code:`ymax`
        property to maintain the square aspect ratio."""

        assume(value > 1)

        domain = SquareDomain(-1, 1)
        domain.xmax = value

        self.assertEqual(value, domain.xmax)
        self.assertEqual(value, domain.ymax)

    @given(value=real)
    def test_ymax_property_sets_xmax(self, value):
        """Ensure that the :code:`ymax` property also sets the :code:`xmax`
        property to maintain the square aspect ratio."""

        assume(value > 1)

        domain = SquareDomain(-1, 1)
        domain.ymax = value

        self.assertEqual(value, domain.xmax)
        self.assertEqual(value, domain.ymax)


@pytest.mark.domain
class TestUnitSquareDomain(TestCase, BaseRealDomainTest):
    """Tests for the :code:`UnitSquare` class"""

    def setUp(self):
        self.domain = UnitSquare()

    def test_init(self):
        """Ensure that the domain is initialised with the proper values to
        define the unit square"""

        domain = UnitSquare()

        self.assertEqual(0, domain.xmin)
        self.assertEqual(0, domain.ymin)

        self.assertEqual(1, domain.xmax)
        self.assertEqual(1, domain.ymax)

    def test_xmax_property_not_settable(self):
        """Ensure that the :code:`xmax` property cannot be set on the UnitSquare
        domain."""

        domain = UnitSquare()

        with pytest.raises(AttributeError) as err:
            domain.xmax = 2

        self.assertIn("can't set attribute", str(err.value))

    def test_xmin_property_not_settable(self):
        """Ensure that the :code:`xmin` property cannot be set on the UnitSquare
        domain."""

        domain = UnitSquare()

        with pytest.raises(AttributeError) as err:
            domain.xmin = -1

        self.assertIn("can't set attribute", str(err.value))

    def test_ymin_property_not_settable(self):
        """Ensure that the :code:`ymin` property cannot be set on the UnitSquare
        domain."""

        domain = UnitSquare()

        with pytest.raises(AttributeError) as err:
            domain.ymin = -1

        self.assertIn("can't set attribute", str(err.value))

    def test_ymax_property_not_settable(self):
        """Ensure that the :code:`ymax` property cannot be set on the UnitSquare
        domain."""

        domain = UnitSquare()

        with pytest.raises(AttributeError) as err:
            domain.ymax = 2

        self.assertIn("can't set attribute", str(err.value))
