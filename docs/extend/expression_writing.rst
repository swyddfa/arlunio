.. _extend_expression_writing:

Writing Expressions
===================

The most common way of constructing |Expression| objects is by writing normal
Python functions that accept some variables as input, do some work on those
variables and then returns the result.

.. todo::

   Link to other relevant expression topics

It is probably easiest to demonstrate with some examples.

.. _extend_expressions_writing_arithmetic:

Basic Arithmetic
----------------

|Expression| objects support all of the most common arithmetic operators::

    >>> import stylo as st

    >>> st.Name("a") + 2
    (+ a 2)

    >>> st.Const(1) - st.Name("x")
    (- 1 x)

    >>> 4 * st.Name("x")
    (* 4 x)

    >>> st.Name("x") / st.Name("y")
    (/ x y)

    >>> st.Name("x") ** 2
    (** x 2)

Please refer to the |Expressions Reference| page for a full list of supported operations.

.. _extend_expressions_writing_math:

Mathematical Functions
^^^^^^^^^^^^^^^^^^^^^^

If you want to make use of mathematical functions like :math:`\sqrt{x}`,
:math:`\sin{(\theta)}` etc. Then stylo provides implementations of many of
these that integrate with the expression system. Taking the |sqrt| function as
an example these functions can be used with regular Python numbers::

    >>> st.sqrt(4)
    2.0

With numpy arrays::

    >>> import numpy as np

    >>> st.sqrt(np.array([1, 4, 9]))
    array([1., 2., 3.])

Or with objects from stylo's expression system::

    >>> st.sqrt(st.Name("x"))
    (sqrt x)

    >>> _.eval({'x': 4})
    2.0

Please refer to the |Expressions Reference| page for a full list of supported
functions. If you wish to use a function that is not currently supported by
stylo you can extend the system to include it.

.. todo::

   Link to the extending page when it exists.

.. _extend_expressions_writing_tips:

Tips, Tricks and Gotchas
------------------------

Here we will outline a number of things you should keep in mind when writing
expressions.

If Statements
^^^^^^^^^^^^^

:code:`if` statements cannot be used with |Expression| objects (at least without
modifying the code) however they can be used in their construction. For example
here is a function that will construct an expression optionally doubling the
input based on the :code:`double` argument::

    >>> def maybe_double(x, double=False):
    ...     if not double:
    ...         return x
    ...     return x * 2

    >>> maybe_double(st.Name("x"), double=True)
    (* x 2)

    >>> maybe_double(st.Name("x"))
    x

Functions
^^^^^^^^^

Assuming that a function returns a value that is compatible with the expression
system then it can be used in the construction of an expression::

    >>> def multiply(x, y):
    ...     return x * y

    >>> def plus(x, y):
    ...     return x + y

    >>> def line(x, m, c):
    ...     return plus(multiply(m, x), c)

    >>> line(st.Name("x"), 2, 1)
    (+ (* 2 x) 1)

Note how the function calls are invisible to the final constructed expression.

.. _extend_expressions_writing_examples:

Examples
--------

Finally we'll conclude with a handful of example expressions constructed with a
variety of different methods.

Writing an Average Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is a function that will construct an |Expression| that will compute the
average value of its inputs::

    >>> def average(*args):
    ...     total = 0
    ...     count = len(args)
    ...     for value in args:
    ...         total += value
    ...     return total / count

We can use this either as a normal Python function::

    >>> average(1, 2, 3, 4)
    2.5

Or with |Const| objects::

    >>> average(st.Const(1), st.Const(2), st.Const(3), st.Const(4))
    (/ (+ (+ (+ (+ 0 1) 2) 3) 4) 4)

    >>> _.eval()
    2.5

Or even as a factory for constructing an averaging function that can take
:code:`N` arguments::

    >>> def make_averager(N):
    ...     names = [st.Name("x" + str(n)) for n in range(1, N + 1)]
    ...     return average(*names)

    >>> avg3 = make_averager(3)
    >>> avg3
    (/ (+ (+ (+ 0 x1) x2) x3) 3)

    >>> avg3.eval({'x1': 1, 'x2': 2, 'x3': 3})
    2.0

    >>> avg4 = make_averager(4)
    >>> avg4
    (/ (+ (+ (+ (+ 0 x1) x2) x3) x4) 4)

    >>> avg4.eval({'x1': 1, 'x2': 2, 'x3': 3, 'x4': 4})
    2.5
