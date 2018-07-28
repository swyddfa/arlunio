from unittest import TestCase

import pytest
from tests.helpers.domain import BaseDomainTest

from stylo.domain.square import SquareDomain, UnitSquare


@pytest.mark.domain
class TestSquareDomain(TestCase, BaseDomainTest):
    """Tests for the RectangularDomain class"""

    def setUp(self):
        self.domain = SquareDomain(-1, 1)


@pytest.mark.domain
class TestUnitSquareDomain(TestCase, BaseDomainTest):
    """Tests for the RectangularDomain class"""

    def setUp(self):
        self.domain = UnitSquare()
