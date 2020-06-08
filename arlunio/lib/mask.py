import functools

from typing import Union

import arlunio as ar
import numpy as np


class Mask(np.ndarray):
    """Currently just a type alias for boolean numpy arrays but gives us the flexibility
    to add smarts later."""

    def __add__(self, other):
        return all_(self, other)


@ar.definition(operation=ar.Defn.OP_ADD)
def MaskAdd(
    width: int, height: int, *, a: ar.Defn[Mask] = None, b: ar.Defn[Mask] = None
) -> Mask:
    """Add any two mask producing definitions together.

    The resulting defintion will return a mask that is :code:`True` if a given point
    is :code:`True` in either :code:`a` or :code:`b`.

    Attributes
    ----------
    a:
        The first mask
    b:
        The second mask
    """

    return any_(a(width=width, height=height), b(width=width, height=height))


@ar.definition(operation=ar.Defn.OP_SUB)
def MaskSub(
    width: int, height: int, *, a: ar.Defn[Mask] = None, b: ar.Defn[Mask] = None
) -> Mask:
    """Subtract one mask away from another mask.

    The resulting definition will return a mask that is :code:`True` only if a given
    point is in :code:`a` **and not** in :code:`b`.

    .. note::

       You will get very different results depending on which way around you set
       :code:`a` and :code:`b`!

    Attributes
    ----------
    a:
        The first "base" mask
    b:
        The second mask that defines the region to remove from :code:`a`
    """
    return all_(a(width=width, height=height), ar.invert(b(width=width, height=height)))


@ar.definition(operation=ar.Defn.OP_MUL)
def MaskMul(
    width: int, height: int, *, a: ar.Defn[Mask] = None, b: ar.Defn[Mask] = None
) -> Mask:
    """Muliply any two mask producing definitions together.

    The resulting definition will return a mask that is :code:`True` only if a given
    point is in both :code:`a` and :code:`b`.

    Attributes
    ----------
    a:
        The first mask
    b:
        The second mask
    """
    return all_(a(width=width, height=height), b(width=width, height=height))


def any_(*args: Union[bool, np.ndarray]) -> Union[bool, np.ndarray]:
    """Given a number of conditions, return :code:`True` if any of the conditions
    are true.

    This function is implemented as a thin wrapper around numpy's
    :code:`np.logical_or` function so that it can take an arbitrary number of inputs.
    This also means that this function will accept arrays of differing sizes - assuming
    that they can be broadcasted to a common shape.

    Parameters
    ----------
    args:
      A number of boolean conditions, a condition can either be a single boolean value
      or a numpy array of boolean values.

    Examples
    --------

    >>> from arlunio.lib.math import any_
    >>> any_(True, False, False)
    True
    >>> any_(False, False, False, False)
    False

    If the arguments are boolean numpy arrays, then the any condition is applied
    element-wise

    >>> import numpy as np
    >>> x1 = np.array([True, False, True])
    >>> x2 = np.array([False, False, True])
    >>> x3 = np.array([False, True, False])
    >>> any_(x1, x2, x3)
    array([ True,  True,  True])

    This function can even handle a mixture of arrays and single values - assuming
    their shapes can be broadcasted to a common shape.

    >>> any_(False, np.array([True, False]), np.array([[False, True], [True, False]]))
    array([[ True,  True],
           [ True, False]])


    See Also
    --------

    |numpy.Broadcasting|
       Numpy documentation on broadcasting.

    |numpy.Array Broadcasting|
       Further background on broadcasting.

    |numpy.logical_or|
       Reference documentation on the :code:`np.logical_or` function
    """
    return functools.reduce(np.logical_or, args)


def all_(*args: Union[bool, np.ndarray]) -> Union[bool, np.ndarray]:
    """Given a number of conditions, return :code:`True` only if **all**
    of the given conditions are true.

    This function is implemented as a thin wrapper around numpy's
    :code:`np.logical_and` function so that it can take an arbitrary number of inputs.
    This also means that this function will accept arrays of differing sizes - assuming
    that they can be broadcasted to a common shape.

    Parameters
    ----------
    args:
      A number of boolean conditions, a conditon can either be a single boolean value,
      or a numpy array of boolean values.

    Examples
    --------

    >>> from arlunio.lib.math import all_
    >>> all_(True, True, True)
    True
    >>> all_(True, False, True, True)
    False

    If the arguments are boolean numpy arrays, then the any condition is applied
    element-wise

    >>> import numpy as np
    >>> x1 = np.array([True, False, True])
    >>> x2 = np.array([False, False, True])
    >>> x3 = np.array([False, True, True])
    >>> all_(x1, x2, x3)
    array([False, False,  True])

    This function can even handle a mixture of arrays and single values - assuming
    their shapes can be broadcasted to a common shape.

    >>> all_(True, np.array([True, False]), np.array([[False, True], [True, False]]))
    array([[False, False],
           [ True, False]])


    See Also
    --------

    |numpy.Broadcasting|
       Numpy documentation on broadcasting.

    |numpy.Array Broadcasting|
       Further background on broadcasting.

    |numpy.logical_and|
       Reference documentation on the :code:`logical_and` function.
    """
    return functools.reduce(np.logical_and, args)


def invert(x):
    return np.logical_not(x)
