"""This module contains a type of 'integration test' for stylo's expression system.

These tests are meant to verify that a user can write code in an identical manner to
how they usually would and produce the same result. **The user should never have to
know that they are in fact manipulating :code:`StyExpr` objects!**
"""
import pytest
import numpy as np
from hypothesis import given
from hypothesis.strategies import integers, booleans
from hypothesis.extra.numpy import arrays

from stylo.testing.strategies import real, vec3, positive, pos3, small_dimension
from stylo.math.expr import StyConst


bools = booleans()
bool3 = arrays(np.bool_, (3,))
power = integers(min_value=1, max_value=10)


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


#######################################################################################
#
#  StyPlus
#
#######################################################################################


@pytest.mark.math
@given(a=real)
@ensure_equivalent
def test_add_left(a):
    """Ensure that users can add a :code:`StyExpr` object on the left with a regular
    Python number."""
    return a + 2


@pytest.mark.math
@given(a=real)
@ensure_equivalent
def test_add_right(a):
    """Ensure that users can add a :code:`StyExpr` object on the right with a regular
    Python number."""
    return 2 + a


@pytest.mark.math
@given(a=real, b=real)
@ensure_equivalent
def test_add_both(a, b):
    """Ensure that users can add two :code:`StyExpr` objects together."""
    return a + b


@pytest.mark.math
@given(a=vec3)
@ensure_equivalent
def test_add_numpy_left(a):
    """Same as :code:`test_add_left` but with numpy arrays."""
    return a + 2


@pytest.mark.math
@given(a=vec3)
@ensure_equivalent
def test_add_numpy_right(a):
    """Same as :code:`test_add_right` but with numpy arrays."""
    return 2 + a


@pytest.mark.math
@given(a=vec3, b=vec3)
@ensure_equivalent
def test_add_numpy_both(a, b):
    """Same as :code:`test_add_both` but with numpy arrays."""
    return a + b


#######################################################################################
#
#  StyMinus
#
#######################################################################################


@pytest.mark.math
@given(a=real)
@ensure_equivalent
def test_subtract_left(a):
    """Ensure that users can subtract :code:`StyExpr` objects on the left with regular
    Python numbers."""
    return a - 2


@pytest.mark.math
@given(a=real)
@ensure_equivalent
def test_subtract_right(a):
    """Ensure that users can subtract :code:`StyExpr` objects on the right with regular
    Python numbers."""
    return 2 - a


@pytest.mark.math
@given(a=real, b=real)
@ensure_equivalent
def test_subtract_both(a, b):
    """Ensure that users can subtract :code:`StyExpr` objects from each other."""
    return a - b


@pytest.mark.math
@given(a=vec3)
@ensure_equivalent
def test_subtract_numpy_left(a):
    """Same as :code:`test_subtract_left` but with numpy arrays."""
    return a - 2


@pytest.mark.math
@given(a=vec3)
@ensure_equivalent
def test_subtract_numpy_right(a):
    """Same as :code:`test_subtract_right` but with numpy arrays."""
    return 2 - a


@pytest.mark.math
@given(a=vec3, b=vec3)
@ensure_equivalent
def test_subtract_numpy_both(a, b):
    """Same as :code:`test_subtract_both` but with numpy arrays."""
    return a - b


#######################################################################################
#
#  StyMultiply
#
#######################################################################################


@pytest.mark.math
@given(a=real)
@ensure_equivalent
def test_mulitply_left(a):
    """Ensure that users can multiply :code:`StyExpr` objects on the left with regular
    Python numbers."""
    return a * 2


@pytest.mark.math
@given(a=real)
@ensure_equivalent
def test_multiply_right(a):
    """Ensure that users can multiply :code:`StyExpr` objects on the right with regular
    Python numbers."""
    return 2 * a


@pytest.mark.math
@given(a=real, b=real)
@ensure_equivalent
def test_multiply_both(a, b):
    """Ensure that users can multiply :code:`StyExpr` objects together."""
    return a * b


@pytest.mark.math
@given(a=vec3)
@ensure_equivalent
def test_mulitply_numpy_left(a):
    """Same as :code:`test_multiply_left` but with numpy arrays."""
    return a * 2


@pytest.mark.math
@given(a=vec3)
@ensure_equivalent
def test_multiply_numpy_right(a):
    """Same as :code:`test_multiply_right` but with numpy arrays."""
    return 2 * a


@pytest.mark.math
@given(a=vec3, b=vec3)
@ensure_equivalent
def test_multiply_numpy_both(a, b):
    """Same as :code:`test_multiply_both` but with numpy arrays."""
    return a * b


#######################################################################################
#
#  StyDivide
#
#######################################################################################


@pytest.mark.math
@given(a=real)
@ensure_equivalent
def test_divide_left(a):
    """Ensure that users can divide :code:`StyExpr` objects on the left with regular
    Python numbers."""
    return a / 2


@pytest.mark.math
@given(a=positive)
@ensure_equivalent
def test_divide_right(a):
    """Ensure that users can divide :code:`StyExpr` objects on the right with regular
    Python numbers."""
    return 2 / a


@pytest.mark.math
@given(a=real, b=positive)
@ensure_equivalent
def test_divide_both(a, b):
    """Ensure that users can divide :code:`StyExpr` objects together."""
    return a / b


@pytest.mark.math
@given(a=vec3)
@ensure_equivalent
def test_divide_numpy_left(a):
    """Same as :code:`test_divide_left` but with numpy arrays."""
    return a / 2


@pytest.mark.math
@given(a=pos3)
@ensure_equivalent
def test_divide_numpy_right(a):
    """Same as :code:`test_divide_right` but with numpy arrays."""
    return 2 / a


@pytest.mark.math
@given(a=real, b=positive)
@ensure_equivalent
def test_divide_numpy_both(a, b):
    """Same as :code:`test_divide_both` but with numpy arrays."""
    return a / b


#######################################################################################
#
#  StyFloorDivide
#
#######################################################################################


@pytest.mark.math
@given(a=real)
@ensure_equivalent
def test_floor_divide_left(a):
    """Ensure that users can floor divide :code:`StyExpr` objects on the left with
    regular Python numbers."""
    return a // 2


@pytest.mark.math
@given(a=positive)
@ensure_equivalent
def test_floor_divide_right(a):
    """Ensure that users can floor divide :code:`StyExpr` objects on the right with
    regular Python numbers."""
    return 2 // a


@pytest.mark.math
@given(a=real, b=positive)
@ensure_equivalent
def test_floor_divide_both(a, b):
    """Ensure that users can floor divide :code:`StyExpr` objects together."""
    return a // b


@pytest.mark.math
@given(a=vec3)
@ensure_equivalent
def test_floor_divide_numpy_left(a):
    """Same as :code:`test_divide_left` but with numpy arrays."""
    return a // 2


@pytest.mark.math
@given(a=pos3)
@ensure_equivalent
def test_floor_divide_numpy_right(a):
    """Same as :code:`test_divide_right` but with numpy arrays."""
    return 2 // a


@pytest.mark.math
@given(a=vec3, b=pos3)
@ensure_equivalent
def test_floor_divide_numpy_both(a, b):
    """Same as :code:`test_divide_both` but with numpy arrays."""
    return a // b


#######################################################################################
#
#  StyPower
#
#######################################################################################


@pytest.mark.math
@given(a=real)
@ensure_equivalent
def test_power_left(a):
    """Ensure that users can raise a :code:`StyExpr` object to a power."""
    return a ** 2


@pytest.mark.math
@given(a=small_dimension)
@ensure_equivalent
def test_power_right(a):
    """Ensure that users can use a :code:`StyExpr` object as a power."""
    return 2 ** a


@pytest.mark.math
@given(a=real, b=power)
@ensure_equivalent
def test_power_both(a, b):
    """Ensure that users can use a code:`StyExpr` objects in a power expression."""
    return a ** b


@pytest.mark.math
@given(a=vec3)
@ensure_equivalent
def test_power_numpy_left(a):
    """Same as :code:`test_power_left` but with numpy arrays."""
    return a ** 2


#######################################################################################
#
#  StyModulo
#
#######################################################################################


@pytest.mark.math
@given(a=real)
@ensure_equivalent
def test_modulo_left(a):
    """Ensure that users can use the modulus with :code:`StyExpr` objects on the left."""
    return a % 2


@pytest.mark.math
@given(a=positive)
@ensure_equivalent
def test_modulo_right(a):
    """Ensure that users can use the modulus with :code:`StyExpr` objects on the right."""
    return 2 % a


@pytest.mark.math
@given(a=real, b=positive)
@ensure_equivalent
def test_modulo_both(a, b):
    """Ensure that users can use the modulus between :code:`StyExpr` objects."""
    return a % b


@pytest.mark.math
@given(a=vec3)
@ensure_equivalent
def test_modulo_numpy_left(a):
    """Same as :code:`test_modulo_left` but with numpy arrays."""
    return a % 2


#######################################################################################
#
#  StyAnd
#
#######################################################################################


@pytest.mark.math
@given(a=bools)
@ensure_equivalent
def test_and_left(a):
    """Ensure that users can use :code:`StyExpr` objects in :code:`and` expressions on
    the left."""
    return a & True


@pytest.mark.math
@given(a=bools)
@ensure_equivalent
def test_and_right(a):
    """Ensure that users can use :code:`StyExpr` objects in :code:`and` expressions on
    the right."""
    return True & a


@pytest.mark.math
@given(a=bools, b=bools)
@ensure_equivalent
def test_and_both(a, b):
    """Ensure that users can use :code:`StyExpr` objects in :code:`and` expressions
    together."""
    return a & b


@pytest.mark.math
@given(a=bool3)
@ensure_equivalent
def test_and_numpy_left(a):
    """Same as :code:`test_and_left` but with numpy arrays."""
    return a & True


@pytest.mark.math
@given(a=bool3)
@ensure_equivalent
def test_and_numpy_right(a):
    """Same as :code:`test_and_right` but with numpy arrays."""
    return True & a


@pytest.mark.math
@given(a=bool3, b=bool3)
@ensure_equivalent
def test_numpy_both(a, b):
    """Same as :code:`test_and_both` but with numpy arrays."""
    return a & b


#######################################################################################
#
#  StyOr
#
#######################################################################################


@pytest.mark.math
@given(a=bools)
@ensure_equivalent
def test_or_left(a):
    """Ensure that users can use :code:`StyExpr` objects in :code:`or` expressions
    on the left."""
    return a | True


@pytest.mark.math
@given(a=bools)
@ensure_equivalent
def test_or_right(a):
    """Ensure that users can use :code:`StyExpr` objects in :code:`or` expressions
    on the right."""
    return True | a


@pytest.mark.math
@given(a=bools, b=bools)
@ensure_equivalent
def test_or_both(a, b):
    """Ensure that users can use :code:`StyExpr` objects in :code:`or` expressions
    together."""
    return a | b


@pytest.mark.math
@given(a=bool3)
@ensure_equivalent
def test_or_numpy_left(a):
    """Same as :code:`test_or_left` but with numpy arrays."""
    return a | True


@pytest.mark.math
@given(a=bool3)
@ensure_equivalent
def test_or_numpy_right(a):
    """Same as :code:`test_or_right` but with numpy arrays."""
    return True | a


@pytest.mark.math
@given(a=bool3, b=bool3)
@ensure_equivalent
def test_or_numpy_both(a, b):
    """Same as :code:`test_or_both` but with numpy arrays."""
    return a | b


#######################################################################################
#
#  StyGreaterThan
#
#######################################################################################


@pytest.mark.math
@given(a=real)
@ensure_equivalent
def test_greater_than_left(a):
    """Ensure that users can use :code:`StyExpr` objects in greater than comparisons
    on the left."""
    return a > 1


@pytest.mark.math
@given(a=real)
@ensure_equivalent
def test_greater_than_right(a):
    """Ensure that users can use :code:`StyExpr` objects in greater than comparisons
    on the right."""
    return 1 > a


@pytest.mark.math
@given(a=real, b=real)
@ensure_equivalent
def test_greater_than_both(a, b):
    """Ensure that users can do greater than comparisons between :code:`StyExpr`
    objects."""
    return a > b


@pytest.mark.math
@given(a=vec3)
@ensure_equivalent
def test_greater_than_numpy_left(a):
    """Same as :code:`test_greater_than_left` but with numpy arrays."""
    return a > 1


@pytest.mark.math
@given(a=vec3)
@ensure_equivalent
def test_greater_than_numpy_right(a):
    """Same as :code:`test_greater_than_right` but with numpy arrays."""
    return 1 > a


@pytest.mark.math
@given(a=vec3, b=vec3)
@ensure_equivalent
def test_greater_than_numpy_both(a, b):
    """Same as :code:`test_greater_than_both` but with numpy arrays."""
    return a > b


#######################################################################################
#
#  StyLessThan
#
#######################################################################################


@pytest.mark.math
@given(a=real)
@ensure_equivalent
def test_less_than_left(a):
    """Ensure that users can use :code:`StyExpr` objects in less than comparisons
    on the left."""
    return a < 1


@pytest.mark.math
@given(a=real)
@ensure_equivalent
def test_less_than_right(a):
    """Ensure that users can use :code:`StyExpr` objects in less than comparisons
    on the right."""
    return 1 < a


@pytest.mark.math
@given(a=real, b=real)
@ensure_equivalent
def test_less_than_both(a, b):
    """Ensure that users can do less than comparisons between :code:`StyExpr`
    objects."""
    return a < b


@pytest.mark.math
@given(a=vec3)
@ensure_equivalent
def test_less_than_numpy_left(a):
    """Same as :code:`test_less_than_left` but with numpy arrays."""
    return a < 1


@pytest.mark.math
@given(a=vec3)
@ensure_equivalent
def test_less_than_numpy_right(a):
    """Same as :code:`test_less_than_right` but with numpy arrays."""
    return 1 < a


@pytest.mark.math
@given(a=vec3, b=vec3)
@ensure_equivalent
def test_less_than_numpy_both(a, b):
    """Same as :code:`test_less_than_both` but with numpy arrays."""
    return a < b


#######################################################################################
#
#  StyGreaterEqual
#
#######################################################################################


@pytest.mark.math
@given(a=real)
@ensure_equivalent
def test_greater_equal_left(a):
    """Ensure that users can use :code:`StyExpr` objects in greater equal comparisons
    on the left."""
    return a >= 1


@pytest.mark.math
@given(a=real)
@ensure_equivalent
def test_greater_equal_right(a):
    """Ensure that users can use :code:`StyExpr` objects in greater equal comparisons
    on the right."""
    return 1 >= a


@pytest.mark.math
@given(a=real, b=real)
@ensure_equivalent
def test_greater_equal_both(a, b):
    """Ensure that users can do greater equal comparisons between :code:`StyExpr`
    objects."""
    return a >= b


@pytest.mark.math
@given(a=vec3)
@ensure_equivalent
def test_greater_equal_numpy_left(a):
    """Same as :code:`test_greater_equal_left` but with numpy arrays."""
    return a >= 1


@pytest.mark.math
@given(a=vec3)
@ensure_equivalent
def test_greater_equal_numpy_right(a):
    """Same as :code:`test_greater_equal_right` but with numpy arrays."""
    return 1 >= a


@pytest.mark.math
@given(a=vec3, b=vec3)
@ensure_equivalent
def test_greater_equal_numpy_both(a, b):
    """Same as :code:`test_greater_equal_both` but with numpy arrays."""
    return a >= b


#######################################################################################
#
#  StyLessEqual
#
#######################################################################################


@pytest.mark.math
@given(a=real)
@ensure_equivalent
def test_less_equal_left(a):
    """Ensure that users can use :code:`StyExpr` objects in less equal comparisons
    on the left."""
    return a <= 1


@pytest.mark.math
@given(a=real)
@ensure_equivalent
def test_less_equal_right(a):
    """Ensure that users can use :code:`StyExpr` objects in less equal comparisons
    on the right."""
    return 1 <= a


@pytest.mark.math
@given(a=real, b=real)
@ensure_equivalent
def test_less_equal_both(a, b):
    """Ensure that users can do less equal comparisons between :code:`StyExpr`
    objects."""
    return a <= b


@pytest.mark.math
@given(a=vec3)
@ensure_equivalent
def test_less_equal_numpy_left(a):
    """Same as :code:`test_less_equal_left` but with numpy arrays."""
    return a <= 1


@pytest.mark.math
@given(a=vec3)
@ensure_equivalent
def test_less_equal_numpy_right(a):
    """Same as :code:`test_less_equal_right` but with numpy arrays."""
    return 1 <= a


@pytest.mark.math
@given(a=vec3, b=vec3)
@ensure_equivalent
def test_less_equal_numpy_both(a, b):
    """Same as :code:`test_less_equal_both` but with numpy arrays."""
    return a <= b
