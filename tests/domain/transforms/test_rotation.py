from math import pi

import pytest
import numpy.testing as npt
from hypothesis import given
from unittest import TestCase

from stylo.domain import UnitSquare
from stylo.domain.transforms.rotation import Rotation
from stylo.testing import BaseDomainTest
from stylo.testing import dimension, angle


@pytest.mark.domain
class TestRotate(TestCase, BaseDomainTest):
    """Tests for the translation class."""

    def setUp(self):

        self.domain = Rotation(UnitSquare(), pi / 2)

    @given(width=dimension, height=dimension, angle=angle)
    def test_angle_affects_t_values(self, width, height, angle):
        """Ensure that the :code:`angle` shifts each value by the negative of the value
        given by the user so that the rotation is intuitive. Also ensure that only the
        :code:`t` values are affected."""

        domain = UnitSquare()
        rs, ts = domain["rt"](width, height)

        rotated = Rotation(domain, angle)
        r_rs, r_ts = rotated["rt"](width, height)

        # The r values should be unaffected
        npt.assert_array_equal(rs, r_rs)

        difference = ts - r_ts
        npt.assert_almost_equal(difference, -angle)
