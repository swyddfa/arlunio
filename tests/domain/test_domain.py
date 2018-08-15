import pytest
from unittest import TestCase

from stylo.domain import RealDomain
from stylo.domain.domain import PolarConversion


@pytest.mark.domain
class TestPolarConversion(TestCase):
    """Tests for the :code:`PolarConversion` class"""

    def setUp(self):

        class MyDomain(PolarConversion, RealDomain):
            def _get_ys(self):
                pass

            def _get_xs(self):
                pass

        self.domain = MyDomain()