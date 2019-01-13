"""This module implements the groundwork for how stylo is able
to represent and evaluate expressions in multiple formats.
"""
import operator
import numpy as np
from abc import ABC, abstractmethod


class StyExpr(ABC):
    """This class is responsible for handling the conversions to/from
    the various formats.

    Implementing classes are responsible for the details.
    """

    # ------------------ Comparisons --------------------
    def __ge__(self, other):
        return StyGreaterEqual(self, other)

    def __gt__(self, other):
        return StyGreaterThan(self, other)

    def __le__(self, other):
        return StyLessEqual(self, other)

    def __lt__(self, other):
        return StyLessThan(self, other)

    # ------------------ Logic --------------------------
    def __and__(self, other):
        return StyAnd(self, other)

    def __rand__(self, other):
        return StyAnd(other, self)

    def __or__(self, other):
        return StyOr(self, other)

    def __ror__(self, other):
        return StyOr(other, self)

    # ------------------ Arithmetic ---------------------
    def __add__(self, other):
        return StyPlus(self, other)

    def __radd__(self, other):
        return StyPlus(other, self)

    def __floordiv__(self, other):
        return StyFloorDivide(self, other)

    def __rfloordiv__(self, other):
        return StyFloorDivide(other, self)

    def __mod__(self, other):
        return StyModulo(self, other)

    def __rmod__(self, other):
        return StyModulo(other, self)

    def __mul__(self, other):
        return StyMultiply(self, other)

    def __rmul__(self, other):
        return StyMultiply(other, self)

    def __pow__(self, other):
        return StyPower(self, other)

    def __rpow__(self, other):
        return StyPower(other, self)

    def __sub__(self, other):
        return StyMinus(self, other)

    def __rsub__(self, other):
        return StyMinus(other, self)

    def __truediv__(self, other):
        return StyDivide(self, other)

    def __rtruediv__(self, other):
        return StyDivide(other, self)

    @abstractmethod
    def eval(self):
        pass


class StyConst(StyExpr):
    def __init__(self, const):
        self.const = const

    def __repr__(self):
        return repr(self.const)

    def eval(self):
        return self.const


def _define_binary_op(name, symbol, impl):
    """This function declares a binary operation."""

    class BinaryOp(StyExpr):
        def __init__(self, a, b):
            self.a = a
            self.b = b

        def __repr__(self):
            a = repr(self.a)
            b = repr(self.b)

            return "({} {} {})".format(symbol, a, b)

        def eval(self):
            a = self.a
            b = self.b

            if isinstance(a, (StyExpr,)):
                a = a.eval()

            if isinstance(b, (StyExpr,)):
                b = b.eval()

            return impl(a, b)

    BinaryOp.__name__ = name
    return BinaryOp


def _define_function(name, symbol, impl):
    """This function defines a mathematical function within the :code:`StyExpr`
    system. As well as a function that we can export for users to use."""

    class StyFunc(StyExpr):
        def __init__(self, x):
            self.x = x

        def __repr__(self):
            x = repr(self.x)

            return "({} {})".format(symbol, x)

        def eval(self):
            x = self.x

            if isinstance(x, (StyExpr,)):
                x = x.eval()

            return impl(x)

    def func(x):
        if isinstance(x, (StyExpr,)):
            return StyFunc(x)

        return impl(x)

    StyFunc.__name__ = name
    func.__name__ = symbol

    return StyFunc, func


# Numeric operators
StyDivide = _define_binary_op("StyDivide", "/", operator.truediv)
StyFloorDivide = _define_binary_op("StyFloorDivide", "//", operator.floordiv)
StyMinus = _define_binary_op("StyMinus", "-", operator.sub)
StyModulo = _define_binary_op("StyModulo", "%", operator.mod)
StyMultiply = _define_binary_op("StyMultiply", "*", operator.mul)
StyPlus = _define_binary_op("StyPlus", "+", operator.add)
StyPower = _define_binary_op("StyPower", "**", operator.pow)

# Logic operators
StyAnd = _define_binary_op("StyAnd", "and", operator.and_)
StyOr = _define_binary_op("StyOr", "or", operator.or_)

# Comparison operators
StyGreaterEqual = _define_binary_op("StyGreaterEqual", ">=", operator.ge)
StyGreaterThan = _define_binary_op("StyGreaterThan", ">", operator.gt)
StyLessEqual = _define_binary_op("StyLessEqual", "<=", operator.le)
StyLessThan = _define_binary_op("StyLessThan", "<", operator.lt)

# Mathematical functions
StyCos, cos = _define_function("StyCos", "cos", np.cos)
StySqrt, sqrt = _define_function("StySqrt", "sqrt", np.sqrt)
StySin, sin = _define_function("StySin", "sin", np.sin)
