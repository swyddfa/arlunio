import numpy as np
from stylo.math.expr import StyConst


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
        inputs are a :code:`StyConst` instance."""

        for a, b, res in self.examples:
            op = self.operation(StyConst(a), StyConst(b))

            if isinstance(res, (np.ndarray,)):
                assert (res == op.eval()).all()
                continue

            assert res == op.eval()

    def test_examples_left_wrapped(self):
        """Ensure that the operation produces the correct output when only the
        left input is a :code:`StyConst` instance."""

        for a, b, res in self.examples:
            op = self.operation(StyConst(a), b)

            if isinstance(res, (np.ndarray,)):
                assert (res == op.eval()).all()
                continue

            assert res == op.eval()

    def test_examples_right_wrapped(self):
        """Ensure that the operation produces the correct output when only the
        right input is a :code:`StyConst` instance."""

        for a, b, res in self.examples:
            op = self.operation(a, StyConst(b))

            if isinstance(res, (np.ndarray,)):
                assert (res == op.eval()).all()
                continue

            assert res == op.eval()

    def test_examples_unwrapped(self):
        """Ensure that the operation produces the correct output when none of the
        inputs are a :code:`StyConst` instance."""

        for a, b, res in self.examples:
            op = self.operation(a, b)

            if isinstance(res, (np.ndarray,)):
                assert (res == op.eval()).all()
                continue

            assert res == op.eval()
