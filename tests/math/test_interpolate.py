import pytest
from hypothesis import given, assume

from stylo.math import lerp
from stylo.testing.strategies import real


@pytest.mark.math
class TestLerp:
    """Tests for the :code:`lerp` function."""

    @given(a=real, b=real)
    def test_take_a_at_zero(self, a, b):
        """Ensure that the resulting function takes the value :code:`a` at :code:`0`."""

        assume(a != b)

        s = lerp(a, b)
        assert s(0) == a

    @given(a=real, b=real)
    def test_take_b_at_one(self, a, b):
        """Ensure that the resulting function takes the value :code:`b` at :code:`1`."""

        assume(a != b)

        s = lerp(a, b)
        assert s(1) == b
