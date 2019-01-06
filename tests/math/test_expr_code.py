"""This module contains a type of 'integration test' for stylo's expression system.

These tests are meant to verify that a user can write code in an identical manner to
how they usually would and produce the same result. **The user should never have to
know that they are in fact manipulating :code:`StyExpr` objects!**
"""
import pytest
import numpy as np
from hypothesis import given

from stylo.testing.strategies import real, vec3, positive, pos3, small_dimension
from stylo.math.expr import StyConst


def ensure_equivalent(f):
    """A decorator that given a function, will execute it twice to ensure the
    output is consistent.

    The first run will be with regular Python objects to give us a reference
    result. The second will be with values wrapped in stylo's expression system
    with the result checked against the reference to ensure it functions as expected.

    TODO: Come up with a better name for this decorator!
    """

    def wrapped_func(**kwargs):
        wrapped_kwargs = {k: StyConst(v) for k, v in kwargs.items()}

        for arg, warg in zip(kwargs.values(), wrapped_kwargs.values()):
            arg_check = arg == warg.eval()

            if isinstance(arg_check, (np.ndarray,)):
                arg_check = arg_check.all()

            assert arg_check

        expected = f(**kwargs)
        actual = f(**wrapped_kwargs)

        check = expected == actual.eval()

        if isinstance(check, (np.ndarray,)):
            check = check.all()

        assert check

    return wrapped_func


@pytest.mark.math
@given(a=real, b=real)
@ensure_equivalent
def test_add(a, b):
    """Ensure that users can add :code:`StyExpr` objects together, or add regular
    Python numbers to them."""

    c = a + 2
    d = 1 + b

    return c + d


@pytest.mark.math
@given(a=vec3, b=vec3)
@ensure_equivalent
def test_add_numpy(a, b):
    """Same as :code:`test_add` but ensure that it also works with numpy arrays."""

    c = a + 2
    d = 1 + b

    return c + d


@pytest.mark.math
@given(a=real, b=real)
@ensure_equivalent
def test_subtract(a, b):
    """Ensure that users can subtract :code:`StyExpr` objects, or subtract regular
    Python numbers from them."""

    c = a - 2
    d = 1 - b

    return c - d


@pytest.mark.math
@given(a=vec3, b=vec3)
@ensure_equivalent
def test_subtract_numpy(a, b):
    """Same as :code:`test_subtract` but ensure that it also works with numpy arrays."""

    c = a - 2
    d = 1 - b

    return c - d


@pytest.mark.math
@given(a=real, b=real)
@ensure_equivalent
def test_multiply(a, b):
    """Ensure that users can multiply :code:`StyExpr` objects, or multiply regular
    Python objects with them."""

    c = a * 2
    d = 3 * b

    return c * d


@pytest.mark.math
@given(a=vec3, b=vec3)
@ensure_equivalent
def test_multiply_numpy(a, b):
    """Same as :code:`test_multiply` but ensure it also works with numpy arrays."""

    c = a * 2
    d = 3 * b

    return c * d


@pytest.mark.math
@given(a=real, b=positive)
@ensure_equivalent
def test_divide(a, b):
    """Ensure that users can divide :code:`StyExpr` objects, or divide them by
    regular Python objects with them."""

    c = a / 2
    d = 5 / b

    return c / d


@pytest.mark.math
@given(a=vec3, b=pos3)
@ensure_equivalent
def test_divide_numpy(a, b):
    """Same as :code:`test_divide` but ensure it also works with numpy arrays."""

    c = a / 2
    d = 5 / b

    return c / d


@pytest.mark.math
@given(a=real, b=small_dimension)
@ensure_equivalent
def test_power(a, b):
    """Ensure that users can use :code:`StyExpr` objects with powers, or use powers with
    regular Python objects."""

    c = a ** 2
    d = 2 ** b

    return c
