import functools

from typing import Callable, Union

import numpy as np


def any(*args: Union[bool, np.ndarray]) -> Union[bool, np.ndarray]:
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


def all(*args: Union[bool, np.ndarray]) -> Union[bool, np.ndarray]:
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


def clamp(values, min_value=0, max_value=1):
    """Force an array of values to stay within a range of values.

    Parameters
    ----------
    values:
      The array of values to clamp
    min_value:
      The minimum value the result should contain
    max_value:
      The maximum value the resul should contain

    Examples
    --------

    By default values will be limited to between :code:`0` and :code:`1`

    >>> import arlunio as ar
    >>> import numpy as np
    >>> vs = np.linspace(-1, 2, 6)
    >>> ar.clamp(vs)
    array([0. , 0. , 0.2, 0.8, 1. , 1. ])

    But this can be changed with extra arguments to the :code:`clamp` function

    >>> ar.clamp(vs, min_value=-1, max_value=0.5)
    array([-1. , -0.4,  0.2,  0.5,  0.5,  0.5])
    """
    vs = np.array(values)
    vs[vs > max_value] = max_value
    vs[vs < min_value] = min_value

    return vs


def invert(x):
    return np.logical_not(x)


def lerp(start: float = 0, stop: float = 1) -> Callable[[float], float]:
    """Return a function that will linerarly interpolate between a and b.

    Parameters
    ----------
    start:
      The value the interpolation should start from.
    stop:
      The value the interpolation should stop at.

    Examples
    --------

    By default this function will interpolate between :code:`0` and :code:`1`

    >>> import arlunio as ar
    >>> f = ar.lerp()
    >>> f(0)
    0
    >>> f(1)
    1

    However by passing arguments to the :code:`lerp` function we can change the bounds
    of the interpolation.

    >>> import numpy as np
    >>> ts = np.linspace(0, 1, 4)
    >>> f = lerp(start=3, stop=-1)
    >>> f(ts)
    array([ 3.        ,  1.66666667,  0.33333333, -1.        ])

    """

    def f(t: float) -> float:
        return (1 - t) * start + t * stop

    return f


def normalise(x):
    """Normalise an array into the range :math:`[0, 1]`

    Parameters
    ----------
    x:
       The array to normalise.
    """
    minx = np.min(x)
    vs = np.array(x)

    vs = vs - minx
    return vs / np.max(vs)
