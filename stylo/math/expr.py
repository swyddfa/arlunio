"""This module implements the groundwork for how stylo is able
to represent and evaluate expressions in multiple formats.
"""
import abc
import inspect
import json
import operator
import numpy as np


# We will maintain a dictionary of StyExpr objects.
EXPR = {}


def lookup_expr(name):
    """Lookup an implementation for a StyExpr object."""
    try:
        return EXPR[name]
    except KeyError:
        return None


class StyExpr(abc.ABC):
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

    def __neg__(self):
        return StyNeg(self)

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

    def json(self, pretty=False):
        indent = None

        if pretty:
            indent = 2

        return json.dumps(self.todict(), indent=indent)

    def todict(self):
        name = self.__class__.__name__
        params = {}

        for pname, pvalue in self.__dict__.items():

            if isinstance(pvalue, (StyExpr,)):
                pvalue = pvalue.todict()

            params[pname] = pvalue

        return {name: params}

    @classmethod
    def fromdict(cls, dictionary):
        name = list(dictionary.keys())[0]
        params = dictionary[name]

        for pname, p in params.items():

            if isinstance(p, (dict,)):
                params[pname] = cls.fromdict(p)

        expr = lookup_expr(name)

        if expr is None:
            message = "No implementation found for: {}"
            raise TypeError(message.format(name))

        return expr(**params)

    @classmethod
    def fromjson(cls, jsonstr):
        dictionary = json.loads(jsonstr)
        return cls.fromdict(dictionary)

    @abc.abstractmethod
    def eval(self, ctx=None, total=False):
        pass


class StyName(StyExpr):
    """A :code:`StyExpr` implementation that represents a variable."""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def eval(self, ctx=None, total=False):

        if ctx is None or self.name not in ctx:

            if total:
                message = "Variable {} is not defined.".format(self.name)
                raise NameError(message)

            return self

        return ctx[self.name]


class StyConst(StyExpr):
    """A :code:`StyExpr` implementation that represents a constant value."""

    def __init__(self, const):
        self.const = const

    def __repr__(self):
        return repr(self.const)

    def eval(self, ctx=None, total=False):
        return self.const


def define_binary_op(name, symbol, impl):
    """This function declares a binary operation."""

    class BinaryOp(StyExpr):
        def __init__(self, a, b):
            self.a = a
            self.b = b

        def __repr__(self):
            a = repr(self.a)
            b = repr(self.b)

            return "({} {} {})".format(symbol, a, b)

        def eval(self, ctx=None, total=False):
            a = self.a
            b = self.b

            if isinstance(a, (StyExpr,)):
                a = a.eval(ctx, total)

            if isinstance(b, (StyExpr,)):
                b = b.eval(ctx, total)

            return impl(a, b)

    BinaryOp.__name__ = name
    EXPR[name] = BinaryOp

    return BinaryOp


def define_function(name, symbol, impl):
    """This function defines a mathematical function within the :code:`StyExpr`
    system. As well as a function that we can export for users to use."""

    class StyFunc(StyExpr):
        def __init__(self, x):
            self.x = x

        def __repr__(self):
            x = repr(self.x)

            return "({} {})".format(symbol, x)

        def eval(self, ctx=None, total=False):
            x = self.x

            if isinstance(x, (StyExpr,)):
                x = x.eval(ctx, total)

            return impl(x)

    def func(x):
        if isinstance(x, (StyExpr,)):
            return StyFunc(x)

        return impl(x)

    StyFunc.__name__ = name
    EXPR[name] = StyFunc

    func.__name__ = symbol

    return StyFunc, func


# Register some StyExpr implementations.
EXPR["StyConst"] = StyConst
EXPR["StyName"] = StyName


# Arithmetic operators
StyDivide = define_binary_op("StyDivide", "/", operator.truediv)
StyFloorDivide = define_binary_op("StyFloorDivide", "//", operator.floordiv)
StyMinus = define_binary_op("StyMinus", "-", operator.sub)
StyModulo = define_binary_op("StyModulo", "%", operator.mod)
StyMultiply = define_binary_op("StyMultiply", "*", operator.mul)
StyPlus = define_binary_op("StyPlus", "+", operator.add)
StyPower = define_binary_op("StyPower", "**", operator.pow)


# Logic operators
StyAnd = define_binary_op("StyAnd", "and", operator.and_)
StyOr = define_binary_op("StyOr", "or", operator.or_)


# Comparison operators
StyGreaterEqual = define_binary_op("StyGreaterEqual", ">=", operator.ge)
StyGreaterThan = define_binary_op("StyGreaterThan", ">", operator.gt)
StyLessEqual = define_binary_op("StyLessEqual", "<=", operator.le)
StyLessThan = define_binary_op("StyLessThan", "<", operator.lt)


# Mathematical functions
StyAbs, abs = define_function("StyAbs", "abs", np.abs)
StyCos, cos = define_function("StyCos", "cos", np.cos)
StyNeg, neg = define_function("StyCos", "neg", operator.neg)
StySqrt, sqrt = define_function("StySqrt", "sqrt", np.sqrt)
StySin, sin = define_function("StySin", "sin", np.sin)


def trace(f):
    """Trace a given a function f in order to construct an expression."""

    params = inspect.signature(f).parameters.keys()
    names = {p: StyName(p) for p in params}

    return f(**names)
