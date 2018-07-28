from unittest import TestCase

import pytest
from tests.helpers.domain import BaseDomainTest

from stylo.domain.rectangular import RectangularDomain


@pytest.mark.domain
class TestRectangularDomain(TestCase, BaseDomainTest):
    """Tests for the RectangularDomain class"""

    def setUp(self):
        self.domain = RectangularDomain(-1, 1, -1, 1)
