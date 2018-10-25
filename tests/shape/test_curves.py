import pytest
import numpy as np
from unittest import TestCase

from stylo.domain import SquareDomain
from stylo.shape.curves import ImplicitXY
from stylo.testing.shape import BaseShapeTest


@pytest.mark.shape
class TestImplicitXY(TestCase, BaseShapeTest):
    """Tests for the :code:`ImplicitXY` shape."""

    def setUp(self):
        self.shape = ImplicitXY(lambda x, y: x - y)

    def test_init_defaults(self):
        """Ensure that the shape is initialised with sane defaults."""

        curve = ImplicitXY(lambda x, y: x * y)

        assert curve.pt == 0.01
        assert not curve.above
        assert not curve.below

    def test_draw_pt(self):
        """Ensure that we can draw a function as a curve."""

        domain = SquareDomain(-1, 1)
        curve = ImplicitXY(lambda x, y: x - y, pt=0.05)

        # fmt: off
        expected = np.array(
            [
                [False, False, False, False, False, False, False,  True],
                [False, False, False, False, False, False,  True, False],
                [False, False, False, False, False,  True, False, False],
                [False, False, False, False,  True, False, False, False],
                [False, False, False,  True, False, False, False, False],
                [False, False,  True, False, False, False, False, False],
                [False,  True, False, False, False, False, False, False],
                [ True, False, False, False, False, False, False, False],
            ]
        )
        # fmt: on

        assert (expected == curve(domain, 8, 8)).all()

    def test_draw_above(self):
        """Ensure that we can draw the area above the curve as a shaded region."""

        domain = SquareDomain(-1, 1)
        curve = ImplicitXY(lambda x, y: x - y, above=True)

        # fmt: off
        expected = np.array(
            [
                [True,  True,  True,  True,  True,  True,  True,  True],
                [True,  True,  True,  True,  True,  True,  True, False],
                [True,  True,  True,  True,  True,  True, False, False],
                [True,  True,  True,  True,  True, False, False, False],
                [True,  True,  True,  True, False, False, False, False],
                [True,  True,  True, False, False, False, False, False],
                [True,  True, False, False, False, False, False, False],
                [True, False, False, False, False, False, False, False],
            ]
        )
        # fmt: on

        assert (expected == curve(domain, 8, 8)).all()

    def test_draw_below(self):
        """Ensure that we can draw the are below the curve as a shaded region."""

        domain = SquareDomain(-1, 1)
        curve = ImplicitXY(lambda x, y: x - y, below=True)

        # fmt: off
        expected = np.array(
            [
                [False, False, False, False, False, False, False,  True],
                [False, False, False, False, False, False, False,  True],
                [False, False, False, False, False, False,  True,  True],
                [False, False, False, False, False,  True,  True,  True],
                [False, False, False, False,  True,  True,  True,  True],
                [False, False, False,  True,  True,  True,  True,  True],
                [False, False,  True,  True,  True,  True,  True,  True],
                [ True,  True,  True,  True,  True,  True,  True,  True],
            ]
        )
        # fmt: on

        assert (expected == curve(domain, 8, 8)).all()
