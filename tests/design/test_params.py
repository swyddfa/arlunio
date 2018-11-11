import pytest
from unittest import TestCase
from hypothesis import given

from stylo.design import StaticPosition, ParametricTrajectory
from stylo.testing.design import BasePositionTest, BaseTrajectoryTest
from stylo.testing.strategies import real


@pytest.mark.pgroup
class TestStaticPosition(TestCase, BasePositionTest):
    """Tests for the :code:`StaticPosition` parameter group."""

    def setUp(self):
        self.params = StaticPosition(x=0.4, y=-0.8)

    def test_default_init(self):
        """If no values are given then :code:`StaticPosition` should choose sensible
        defaults."""

        params = StaticPosition()

        def f(**kwargs):
            assert kwargs == {"x": 0, "y": 0}

        f(**params)

    @given(x=real, y=real)
    def test_init(self, x, y):
        """:code:`StaticPosition` should use the values supplied."""

        params = StaticPosition(x, y)

        def f(**kwargs):
            assert kwargs == {"x": x, "y": y}

        f(**params)


@pytest.mark.pgroup
class TestParametricTrajectory(TestCase, BaseTrajectoryTest):
    """Tests for the :code:`ParametricTrajectory` parameter group."""

    def setUp(self):
        def x(t):
            return 2 * t

        def y(t):
            return t * t - 4 * t + 3

        self.params = ParametricTrajectory(x, y)

    @given(t=real)
    def test_default_init(self, t):
        """If no functions are given then :code:`ParametricTrajectory` should choose
        sensible defaults."""

        params = ParametricTrajectory()

        def f(**kwargs):
            assert kwargs == {"x": t, "y": t}

        f(**params(t))

    @given(t=real)
    def test_init(self, t):
        """:code:`ParametricTrajectory` should use the functions supplied."""

        def x(s):
            return 2 * s

        def y(s):
            return s / 2

        params = ParametricTrajectory(x, y)

        def f(**kwargs):
            assert kwargs == {"x": 2 * t, "y": t / 2}

        f(**params(t))
