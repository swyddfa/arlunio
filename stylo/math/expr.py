"""This module implements the groundwork for how stylo is able
to represent and evaluate expressions in multiple formats.
"""
import operator
import numpy as np
from abc import ABC, abstractmethod


class StyExpr(ABC):
    """This class is responsible for handling all details of converting an
    expression to/from the various formats.

    Implementing classes are responsible for the details.
    """

    def __add__(self, other):
        return StyPlus(self, other)

    def __radd__(self, other):
        return StyPlus(other, self)

    def __sub__(self, other):
        return StyMinus(self, other)

    def __rsub__(self, other):
        return StyMinus(other, self)

    def __mul__(self, other):
        return StyMultiply(self, other)

    def __rmul__(self, other):
        return StyMultiply(other, self)

    def __truediv__(self, other):
        return StyDivide(self, other)

    def __rtruediv__(self, other):
        return StyDivide(other, self)

    def __pow__(self, other):
        return StyPower(self, other)

    def __rpow__(self, other):
        return StyPower(other, self)

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
StyGreaterEqual = _define_binary_op("StyGreaterEqual", ">=", operator.ge)
StyGreaterThan = _define_binary_op("StyGreaterThan", ">", operator.gt)
StyLessEqual = _define_binary_op("StyLessEqual", "<=", operator.le)
StyLessThan = _define_binary_op("StyLessThan", "<", operator.lt)
StyOr = _define_binary_op("StyOr", "or", operator.or_)
