from unittest import TestCase

import pytest
from tests.helpers.domain import BaseDomainTest

from stylo.domain.square import UnitSquare
from stylo.domain.transforms import Translation


@pytest.mark.domain
class TestSquareDomain(TestCase, BaseDomainTest):
    """Tests for the RectangularDomain class"""

    def setUp(self):

        # We just need any instance of the translation to test the interface
        # with, we'll get to the details ourselves in the test cases here.
        self.domain = Translation(UnitSquare(), 1, 1)
