import numpy as np
from stylo.math.expr import Const


def ensure_equivalent(f):
    """A decorator that given a function, will execute it twice to ensure the
    output is consistent.

    The first run will be with regular Python objects to give us a reference
    result. The second will be with values wrapped in stylo's expression system
    with the result checked against the reference to ensure it functions as expected.

    TODO: Come up with a better name for this decorator!
    """

    def wrapped_func(**kwargs):
        wrapped_kwargs = {k: Const(v) for k, v in kwargs.items()}

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


class BaseBinaryOpTest:
    """A base class for testing :code:`BinaryOperations`.

    When writing your test case for a new :code:`BinaryOperation` implementation you
    need to declare it as follows.

    .. code-block:: python

       from unittest import TestCase
       from stylo.testing.math import BaseBinaryOpTest

       class TestMyOp(TestCase, BaseBinaryOpTest):
           ...

    .. note::

       The order in which you write the classes is *very* important.

    You also need to define the :code:`setUp` method to set the :code:`operation`
    attribute equal to your **class definition** and the :code:`examples` attribute
    to a list of tuples of the form :code:`(a, b, result)`.

    .. code-block:: python

       def setUp(self):
           self.operation = MyOp  # Notice we do *not* create an instance
           self.examples = [
                (1, 2, 3),    # 1 + 2    =  3
                (4, -5, -1),  # 4 + (-5) = -1
                ...
           ]
    """

    def test_examples_both_wrapped(self):
        """Ensure that the operation produces the correct output when both of the
        inputs are a :code:`Const` instance."""

        for a, b, res in self.examples:
            op = self.operation(Const(a), Const(b))

            if isinstance(res, (np.ndarray,)):
                assert (res == op.eval()).all()
                continue

            assert res == op.eval()

    def test_examples_left_wrapped(self):
        """Ensure that the operation produces the correct output when only the
        left input is a :code:`Const` instance."""

        for a, b, res in self.examples:
            op = self.operation(Const(a), b)

            if isinstance(res, (np.ndarray,)):
                assert (res == op.eval()).all()
                continue

            assert res == op.eval()

    def test_examples_right_wrapped(self):
        """Ensure that the operation produces the correct output when only the
        right input is a :code:`Const` instance."""

        for a, b, res in self.examples:
            op = self.operation(a, Const(b))

            if isinstance(res, (np.ndarray,)):
                assert (res == op.eval()).all()
                continue

            assert res == op.eval()

    def test_examples_unwrapped(self):
        """Ensure that the operation produces the correct output when none of the
        inputs are a :code:`Const` instance."""

        for a, b, res in self.examples:
            op = self.operation(a, b)

            if isinstance(res, (np.ndarray,)):
                assert (res == op.eval()).all()
                continue

            assert res == op.eval()
