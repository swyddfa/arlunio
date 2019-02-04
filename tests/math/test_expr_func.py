"""This module contains another kind of integration test for stylo's expression system.

This one is to verify that the user is able to use the exported mathematical functions
in a transparent way. i.e. **The user should never have to know that they are using
:code:`StyExpr` objects!**
"""
import pytest
from hypothesis import given

from stylo.math.expr import sqrt, sin, cos
from stylo.testing.strategies import real, vec3, positive, pos3
from stylo.testing.math import ensure_equivalent


@pytest.mark.math
@given(x=positive)
@ensure_equivalent
def test_sqrt(x):
    """Ensure that the user is able to use the :code:`sqrt` function with
    :code:`StyExpr` objects or regular Python numbers."""
    return sqrt(x)


@pytest.mark.math
@given(x=pos3)
@ensure_equivalent
def test_sqrt_numpy(x):
    """Same as :code:`test_sqrt` but with numpy arrays."""
    return sqrt(x)


@pytest.mark.math
@given(x=real)
@ensure_equivalent
def test_sin(x):
    """Ensure that the user is able to use the :code:`sin` function with
    :code:`StyExpr` objects or regular Python numbers."""
    return sin(x)


@pytest.mark.math
@given(x=vec3)
@ensure_equivalent
def test_sin_numpy(x):
    """Ensure that the user is able to use the :code:`cos` function with
    :code:`StyExpr` objects or regular Python numbers."""
    return sin(x)


@pytest.mark.math
@given(x=real)
@ensure_equivalent
def test_cos(x):
    """Ensure that the user is able to use the :code:`cos` function with
    :code:`StyExpr` objects or regular Python numbers."""
    return cos(x)


@pytest.mark.math
@given(x=vec3)
@ensure_equivalent
def test_cos_numpy(x):
    """Ensure that the user is able to use the :code:`cos` function with
    :code:`StyExpr` objects or regular Python numbers."""
    return cos(x)
