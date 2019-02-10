"""This module implements the groundwork for how stylo is able
to represent and evaluate expressions in multiple formats.
"""
import abc
import inspect
import json
import operator

import numpy as np

# We will maintain a dictionary of Expr objects.
EXPR = {}


def lookup_expr(name):
    """Lookup an implementation for a Expr object."""
    try:
        return EXPR[name]
    except KeyError:
        return None


class Expression(abc.ABC):
    """This class is responsible for handling the conversions to/from
    the various formats.

    Implementing classes are responsible for the details.
    """

    # ------------------ Comparisons --------------------
    def __ge__(self, other):
        return GreaterEqual(self, other)

    def __gt__(self, other):
        return GreaterThan(self, other)

    def __le__(self, other):
        return LessEqual(self, other)

    def __lt__(self, other):
        return LessThan(self, other)

    # ------------------ Logic --------------------------
    def __and__(self, other):
        return And(self, other)

    def __rand__(self, other):
        return And(other, self)

    def __or__(self, other):
        return Or(self, other)

    def __ror__(self, other):
        return Or(other, self)

    # ------------------ Arithmetic ---------------------
    def __add__(self, other):
        return Plus(self, other)

    def __radd__(self, other):
        return Plus(other, self)

    def __floordiv__(self, other):
        return FloorDivide(self, other)

    def __rfloordiv__(self, other):
        return FloorDivide(other, self)

    def __mod__(self, other):
        return Modulo(self, other)

    def __rmod__(self, other):
        return Modulo(other, self)

    def __mul__(self, other):
        return Multiply(self, other)

    def __rmul__(self, other):
        return Multiply(other, self)

    def __neg__(self):
        return Neg(self)

    def __pow__(self, other):
        return Power(self, other)

    def __rpow__(self, other):
        return Power(other, self)

    def __sub__(self, other):
        return Minus(self, other)

    def __rsub__(self, other):
        return Minus(other, self)

    def __truediv__(self, other):
        return Divide(self, other)

    def __rtruediv__(self, other):
        return Divide(other, self)

    def json(self, pretty=False):
        indent = None

        if pretty:
            indent = 2

        return json.dumps(self.todict(), indent=indent)

    def todict(self):
        name = self.__class__.__name__
        params = {}

        for pname, pvalue in self.__dict__.items():

            if isinstance(pvalue, (Expression,)):
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


class Name(Expression):
    """A :code:`Expr` implementation that represents a variable."""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def eval(self, ctx=None, total=False):

        if ctx is None or self.name not in ctx:

            if total:
                message = "Variable '{}' is not defined.".format(self.name)
                raise NameError(message)

            return self

        return ctx[self.name]


class Const(Expression):
    """A :code:`Expr` implementation that represents a constant value."""

    def __init__(self, const):
        self.const = const

    def __repr__(self):
        return repr(self.const)

    def eval(self, ctx=None, total=False):
        return self.const


def define_binary_op(name, symbol, impl):
    """This function declares a binary operation."""

    class BinaryOp(Expression):
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

            if isinstance(a, (Expression,)):
                a = a.eval(ctx, total)

            if isinstance(b, (Expression,)):
                b = b.eval(ctx, total)

            return impl(a, b)

    BinaryOp.__name__ = name
    EXPR[name] = BinaryOp

    return BinaryOp


def define_function(name, symbol, impl):
    """This function defines a mathematical function within the :code:`Expr`
    system. As well as a function that we can export for users to use."""

    class Func(Expression):
        def __init__(self, x):
            self.x = x

        def __repr__(self):
            x = repr(self.x)

            return "({} {})".format(symbol, x)

        def eval(self, ctx=None, total=False):
            x = self.x

            if isinstance(x, (Expression,)):
                x = x.eval(ctx, total)

            return impl(x)

    def func(x):
        if isinstance(x, (Expression,)):
            return Func(x)

        return impl(x)

    Func.__name__ = name
    EXPR[name] = Func

    func.__name__ = symbol

    return Func, func


# Register some Expr implementations.
EXPR["Const"] = Const
EXPR["Name"] = Name


# Arithmetic operators
Divide = define_binary_op("Divide", "/", operator.truediv)
FloorDivide = define_binary_op("FloorDivide", "//", operator.floordiv)
Minus = define_binary_op("Minus", "-", operator.sub)
Modulo = define_binary_op("Modulo", "%", operator.mod)
Multiply = define_binary_op("Multiply", "*", operator.mul)
Plus = define_binary_op("Plus", "+", operator.add)
Power = define_binary_op("Power", "**", operator.pow)


# Logic operators
And = define_binary_op("And", "and", operator.and_)
Or = define_binary_op("Or", "or", operator.or_)


# Comparison operators
GreaterEqual = define_binary_op("GreaterEqual", ">=", operator.ge)
GreaterThan = define_binary_op("GreaterThan", ">", operator.gt)
LessEqual = define_binary_op("LessEqual", "<=", operator.le)
LessThan = define_binary_op("LessThan", "<", operator.lt)


# Mathematical functions
Abs, abs = define_function("Abs", "abs", np.abs)
Cos, cos = define_function("Cos", "cos", np.cos)
Neg, neg = define_function("Cos", "neg", operator.neg)
Sqrt, sqrt = define_function("Sqrt", "sqrt", np.sqrt)
Sin, sin = define_function("Sin", "sin", np.sin)


def trace(f):
    """Trace a given a function f in order to construct an expression."""

    params = inspect.signature(f).parameters.keys()
    names = {p: Name(p) for p in params}

    return f(**names)
