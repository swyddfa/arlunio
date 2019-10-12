import functools

from typing import Union

import numpy as np


def any(*args: Union[bool, np.ndarray]) -> Union[bool, np.ndarray]:
    """Given a number of conditions, return :code:`True` if any of the conditions
    are true.

    This function is implemented as a thin wrapper around numpy's
    :code:`np.logical_or` function so that it can take an arbitrary number of inputs.
    This also means that this function will accept arrays of differing sizes - assuming
    that they can be broadcasted to a common shape.

    .. seealso::

       |numpy.Broadcasting|
          Numpy documentation on broadcasting.

       |numpy.Array Broadcasting|
          Further background on broadcasting.

       |numpy.logical_or|
          Reference documentation on the :code:`np.logical_or` function

    :param args: A number of boolean conditions, a condition can either be a single
                 boolean value or a numpy array of boolean values.

    :Examples:

    >>> import arlunio as ar
    >>> ar.any(True, False, False)
    True

    >>> ar.any(False, False, False, False)
    False

    If the arguments are boolean numpy arrays, then the any condition is applied
    element-wise

    >>> import numpy as np

    >>> x1 = np.array([True, False, True])
    >>> x2 = np.array([False, False, True])
    >>> x3 = np.array([False, True, False])

    >>> ar.any(x1, x2, x3)
    array([ True,  True,  True])

    This function can even handle a mixture of arrays and single values - assuming
    their shapes can be broadcasted to a common shape.

    >>> ar.any(False, np.array([True, False]), np.array([[False, True], [True, False]]))
    array([[ True,  True],
           [ True, False]])
    """
    return functools.reduce(np.logical_or, args)


def all(*args: Union[bool, np.ndarray]) -> Union[bool, np.ndarray]:
    """Given a number of conditions, return :code:`True` only if **all**
    of the given conditions are true.

    This function is implemented as a thin wrapper around numpy's
    :code:`np.logical_and` function so that it can take an arbitrary number of inputs.
    This also means that this function will accept arrays of differing sizes - assuming
    that they can be broadcasted to a common shape.

    .. seealso::

       |numpy.Broadcasting|
          Numpy documentation on broadcasting.

       |numpy.Array Broadcasting|
          Further background on broadcasting.

       |numpy.logical_and|
          Reference documentation on the :code:`logical_and` function.

    :param args: A number of boolean conditions, a conditon can either be a single
                 boolean value, or a numpy array of boolean values.

    :Examples:

    >>> import arlunio as ar
    >>> ar.all(True, True, True)
    True

    >>> ar.all(True, False, True, True)
    False

    If the arguments are boolean numpy arrays, then the any condition is applied
    element-wise

    >>> import numpy as np

    >>> x1 = np.array([True, False, True])
    >>> x2 = np.array([False, False, True])
    >>> x3 = np.array([False, True, True])

    >>> ar.all(x1, x2, x3)
    array([False, False,  True])

    This function can even handle a mixture of arrays and single values - assuming
    their shapes can be broadcasted to a common shape.

    >>> ar.all(True, np.array([True, False]), np.array([[False, True], [True, False]]))
    array([[False, False],
           [ True, False]])
    """
    return functools.reduce(np.logical_and, args)


def invert(x):
    return np.logical_not(x)
