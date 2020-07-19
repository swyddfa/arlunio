from __future__ import annotations

import inspect
import logging
import typing
import typing as t

import attr

from ._version import __version__

__all__ = [
    "Defn",
    "DefnAttribute",
    "DefnBase",
    "DefnInput",
    "definition",
    "__version__",
]

logger = logging.getLogger(__name__)


def _format_type(obj: t.Optional[t.Any] = None, type_: t.Optional[t.Any] = None) -> str:
    """Given an object, return an appropriate representation for its type."""

    if obj is not None and type_ is not None:
        raise ValueError("You can only specify 'obj' or 'type_'")

    if obj is not None and isinstance(obj, Defn):
        type_ = obj.produces()

        try:
            t = type_.__name__
        except AttributeError:
            t = str(type_).split(".")[-1]

        return f"{obj.__class__.__name__}[{t}]"

    if obj is not None:
        type_ = type(obj)

    try:
        return type_.__name__
    except AttributeError:
        return str(type_).split(".")[-1]


@attr.s(auto_attribs=True)
class DefnInput:
    """A class that represents an input to a definition"""

    name: str
    """The name of the input."""

    dtype: t.Any
    """The type of the input"""

    inherited: bool
    """Flag to indicate if the input has been inherited from another definition."""

    sources: "t.Optional[t.List[Defn]]" = None
    """List of definitions to indicate which definitions an input has been inherited
    from."""

    @classmethod
    def fromparam(cls, parameter: inspect.Parameter, dtype: t.Any):
        """Given a parameter and a type hint, construct an input."""

        name = parameter.name
        return cls(name=name, dtype=dtype, inherited=False)


@attr.s(auto_attribs=True)
class DefnBase:
    """A definition base."""

    name: str
    """The name of the base."""

    defn: "Defn"
    """The actual definition."""

    @classmethod
    def fromparam(cls, parameter: inspect.Parameter, defn: "Defn"):
        """Given a parameter and type hint, construct a base"""

        name = parameter.name
        return cls(name=name, defn=defn)


@attr.s(auto_attribs=True)
class DefnAttribute:
    """A definition attribute"""

    name: str
    """The name of the attribute."""

    default: t.Any
    """The default value of the attrbute."""

    inherited: bool
    """Indicates whether this attribute is inherited."""

    dtype: t.Optional[t.Any] = None
    """The type of the attribute."""

    @classmethod
    def copy(cls, existing):
        """Copy an existing attribute definition."""
        return cls(**attr.asdict(existing))

    @classmethod
    def fromparam(cls, parameter: inspect.Parameter, dtype: t.Any):
        """Given a parameter and type hints, construct an attribute."""

        args = {
            "name": parameter.name,
            "default": parameter.default,
            "dtype": dtype,
            "inherited": False,
        }

        return cls(**args)

    def to_attr(self):
        """Convert our representation of an attribute into an attrs attribute."""

        metadata = {Defn.ATTR_ID: {"inherited": self.inherited}}

        args = {
            "default": self.default,
            "kw_only": True,
            "metadata": metadata,
        }

        if self.dtype is not None:
            args["type"] = self.dtype

        return attr.ib(**args)


T = t.TypeVar("T")


@attr.s(auto_attribs=True)
class Defn(t.Generic[T]):
    """Defn, short for 'Definition' is the object that powers the rest of
    :code:`arlunio`.
    """

    ATTR_ID: t.ClassVar[str] = "arlunio.attribute"

    OP_ADD: t.ClassVar[str] = "addition"
    OP_AND: t.ClassVar[str] = "and"
    OP_DIV: t.ClassVar[str] = "division"
    OP_FLOORDIV: t.ClassVar[str] = "floor_division"
    OP_LSHIFT: t.ClassVar[str] = "left_shift"
    OP_MATMUL: t.ClassVar[str] = "matrix_multiplication"
    OP_MOD: t.ClassVar[str] = "modulus"
    OP_MUL: t.ClassVar[str] = "multiplication"
    OP_OR: t.ClassVar[str] = "or"
    OP_POW: t.ClassVar[str] = "power"
    OP_RSHIFT: t.ClassVar[str] = "right_shift"
    OP_SUB: t.ClassVar[str] = "subtraction"
    OP_XOR: t.ClassVar[str] = "exclusive_or"

    def __call__(self, *pos, **kwargs):
        logger.debug("Preparing: '%s'", self.__class__.__name__)
        logger.debug("--> Positional Args: %s", pos)
        logger.debug("--> Keyword arguments: %s", kwargs.keys())

        # Requiring inputs to be given as kw args makes the api less sensitive to
        # changes in the implementation
        if len(pos) != 0:
            raise TypeError("Definition inputs must be passed as keyword arguments")

        required = self.inputs(inherited=False)
        missing = ["'" + n + "'" for n in required.keys() if n not in kwargs]

        logger.debug("Preparing arguments")
        logger.debug("--> Directly required inputs: %s", list(required.keys()))

        if len(missing) != 0:
            name = self.__class__.__name__
            inpts = ", ".join(missing)
            message = f"Unable to evaluate definition '{name}', missing inputs: {inpts}"

            raise TypeError(message)

        # Start building a dict for the args to pass to the _impl function. Starting
        # with the actual values of the required inputs
        args = {inpt: kwargs[inpt] for inpt in required}

        # Now to evaluate any definitions this definition is derived from.
        attributes = self.values(inherited=True)
        bases = dict(self._bases)

        logger.debug("--> Attributes: %s", attributes)
        logger.debug("--> Bases: %s", bases)

        for name, base in bases.items():

            if name in kwargs:
                logger.debug("%s: Using user provided override, %s", name, kwargs[name])
                args[name] = kwargs[name]
                continue

            attrs = {
                name: attributes[name] for name in base.defn.attributes(inherited=True)
            }
            instance = base.defn(**attrs)
            logger.debug("%s: Created instance, %s", name, instance)

            # And then evaluate it!
            args[name] = instance(**kwargs)

        message = "Executing '%s' with %s"
        logger.debug(message, self.__class__.__name__, args.keys())

        return self._impl(**args, **self.values())

    def _special_method(self, operation, a, b):
        """Implements the special methods in a standardized way."""

        op_name = operation.capitalize().replace("_", " ")
        a_is_defn = isinstance(a, Defn)
        b_is_defn = isinstance(b, Defn)

        t1 = type(a) if not a_is_defn else Defn[a.produces()]
        t2 = type(b) if not b_is_defn else Defn[b.produces()]

        impl = self._operators.get((operation, t1, t2), None)

        if impl is None:
            a = _format_type(a)
            b = _format_type(b)

            raise TypeError(f"{op_name} is not supported between {a} and {b}")

        defn = impl(a=a, b=b)
        return defn

    def __add__(self, other):
        return self._special_method(self.OP_ADD, self, other)

    def __radd__(self, other):
        return self._special_method(self.OP_ADD, other, self)

    def __and__(self, other):
        return self._special_method(self.OP_AND, self, other)

    def __rand__(self, other):
        return self._special_method(self.OP_AND, other, self)

    def __floordiv__(self, other):
        return self._special_method(self.OP_FLOORDIV, self, other)

    def __rfloordiv__(self, other):
        return self._special_method(self.OP_FLOORDIV, other, self)

    def __lshift__(self, other):
        return self._special_method(self.OP_LSHIFT, self, other)

    def __rlshift__(self, other):
        return self._special_method(self.OP_LSHIFT, other, self)

    def __matmul__(self, other):
        return self._special_method(self.OP_MATMUL, self, other)

    def __rmatmul__(self, other):
        return self._special_method(self.OP_MATMUL, other, self)

    def __mod__(self, other):
        return self._special_method(self.OP_MOD, self, other)

    def __rmod__(self, other):
        return self._special_method(self.OP_MOD, other, self)

    def __mul__(self, other):
        return self._special_method(self.OP_MUL, self, other)

    def __rmul__(self, other):
        return self._special_method(self.OP_MUL, other, self)

    def __or__(self, other):
        return self._special_method(self.OP_OR, self, other)

    def __ror__(self, other):
        return self._special_method(self.OP_OR, other, self)

    def __pow__(self, other):
        return self._special_method(self.OP_POW, self, other)

    def __rpow__(self, other):
        return self._special_method(self.OP_POW, other, self)

    def __rshift__(self, other):
        return self._special_method(self.OP_RSHIFT, self, other)

    def __rrshift__(self, other):
        return self._special_method(self.OP_RSHIFT, other, self)

    def __sub__(self, other):
        return self._special_method(self.OP_SUB, self, other)

    def __rsub__(self, other):
        return self._special_method(self.OP_SUB, other, self)

    def __truediv__(self, other):
        return self._special_method(self.OP_DIV, self, other)

    def __rtruediv__(self, other):
        return self._special_method(self.OP_DIV, other, self)

    def __xor__(self, other):
        return self._special_method(self.OP_XOR, self, other)

    def __rxor__(self, other):
        return self._special_method(self.OP_XOR, other, self)

    def values(self, inherited=False) -> t.Dict[str, t.Any]:
        """Return all the attribute values on this definition."""
        return {k: getattr(self, k) for k in self.attributes(inherited)}

    @classmethod
    def attributes(cls, inherited=False) -> t.Dict[str, DefnAttribute]:
        """Return all attributes defined on this definition.

        Parameters
        ----------
        inherited:
            If :code:`True` return all inherited attributes also.
        """
        if not hasattr(cls, "_attributes"):
            return {}

        if inherited:
            return cls._attributes

        return {k: v for k, v in cls._attributes.items() if not v.inherited}

    @classmethod
    def bases(cls) -> t.Dict[str, DefnBase]:
        """Return all the definitions this defintion is derived from."""

        if not hasattr(cls, "_bases"):
            return {}

        return dict(cls._bases)

    @classmethod
    def inputs(cls, inherited=True) -> t.Dict[str, DefnInput]:
        """Return all the inputs required to evaluate this definition.

        Parameters
        ----------
        inherited:
            If :code:`True` (default) also return any inherited inputs.
        """
        if not hasattr(cls, "_inputs"):
            return {}

        if inherited:
            return {k: v for k, v in cls._inputs.items()}

        return {k: v for k, v in cls._inputs.items() if not v.inherited}

    @classmethod
    def produces(cls):
        """Return the type of the object that this definition produces."""

        if not hasattr(cls, "_produces"):
            return t.Any

        return cls._produces


def _inspect_arguments(fn: t.Callable):
    """Given a function, determine what its arguments are and their properties."""

    KW_ONLY = inspect.Parameter.KEYWORD_ONLY
    parameters = inspect.signature(fn).parameters
    hints = typing.get_type_hints(fn)

    inputs, bases, attributes = {}, {}, {}
    produces = hints.get("return", t.Any)

    for param in parameters.values():
        dtype = hints.get(param.name, None)

        if param.kind == KW_ONLY:
            attrib = DefnAttribute.fromparam(param, dtype)
            attributes[param.name] = attrib
            continue

        # Input parameters must have a type annotation
        if dtype is None:
            raise TypeError(f"Missing type annotation for parameter '{param.name}'")

        if issubclass(dtype, Defn):
            base = DefnBase.fromparam(param, dtype)
            bases[param.name] = base
            continue

        input_ = DefnInput.fromparam(param, dtype)
        inputs[param.name] = input_

    # Now for any bases, inherited all their attributes and inputs.
    for base in bases.values():
        _inherit_attributes(base, attributes)
        _inherit_inputs(base, inputs)

    return inputs, bases, attributes, produces


def _inherit_attributes(base: DefnBase, attributes):
    """Given a definition and the attributes for the current definition under
    construction copy over its attributes."""

    for name, attrib in base.defn.attributes(inherited=True).items():

        # For now we will skip any attributes that have already been defined.
        # This means that any definitions that share the same attribute name will
        # inherit the same value.
        #
        # This is probably what you would want in most(?) cases, but I'm sure we will
        # need the ability to do something more clever in the future...
        #
        # We may also at some point want to consider the case when attrbiutes carry
        # types which clash...
        if name in attributes:
            continue

        attrib = DefnAttribute.copy(attrib)
        attrib.inherited = True

        attributes[name] = attrib


def _inherit_inputs(base: DefnBase, inputs):
    """Given a definition and the inputs for the current definition under construction
    copy over its inputs.

    Parameters
    ----------
    base:
        The definition base to inherit inputs from
    inputs:
        The dictionary carrying the inputs for the definition under construction.
    """
    logger.debug("Inherting inputs from definition: %s", base.defn.__name__)
    defn = base.defn

    for name, inpt in defn.inputs().items():

        dname = defn.__name__

        if name not in inputs:
            inputs[name] = DefnInput(
                name=name, dtype=inpt.dtype, inherited=True, sources=[defn]
            )

            logger.debug("%s: inherited input, new", name)
            continue

        existing = inputs[name]

        # Check for a conflict between the types
        if existing.dtype != inpt.dtype:
            message = (
                f"Input '{name}' ({inpt.dtype}) inherited from '{dname}' conflicts"
                f" with existing input '{name}' ({existing.dtype})"
            )

            if existing.sources is not None:
                extras = ",".join(["'" + d.__name__ + "'" for d in existing.sources])
                message += f" inherited from {extras}"

            raise TypeError(message)

        # If the input is an inherited one, add this definition to the list of sources
        if existing.inherited:
            existing.sources.append(defn)
            logger.debug("%s: inherited input, updated", name)

            continue

        logger.debug("%s: already defined", name)


_OPERATOR_POOL = {}


def _define_operator(defn: Defn, operation: str, operator_pool):
    """Given a definition, check to see if it matches the criteria to be an operator."""

    attrs = defn.attributes(inherited=True)

    if "a" not in attrs.keys() or "b" not in attrs.keys():
        message = "Operators must define 2 attributes 'a' and 'b'"
        raise TypeError(message)

    a = attrs["a"].dtype
    b = attrs["b"].dtype

    if a is None:
        raise TypeError("Operator input 'a' is missing a valid type annotation")

    if b is None:
        raise TypeError("Operator input 'b' is missing a valid type annotation")

    key = (operation, a, b)

    if key in operator_pool:
        raise TypeError(
            f"A {operation} operator between {a} and {b} has already been defined"
        )

    operator_pool[key] = defn


def definition(f=None, *, operation: str = None, operator_pool=None) -> Defn:
    """Define a new Definition.

    Parameters
    ----------
    f:
        The function that is the definition
    operator:
        Flag used to indicate if this definition is an operator.
    operator_pool:
        Can be used to override the default operator pool
    """

    def wrapper(fn):

        defn_name = fn.__name__
        operators = operator_pool if operator_pool is not None else _OPERATOR_POOL

        attributes = {
            "__doc__": inspect.getdoc(fn),
            "__module__": fn.__module__,
            "_impl": staticmethod(fn),
            "_operators": operators,
        }

        inputs, bases, attribs, produces = _inspect_arguments(fn)

        for name, attrib in attribs.items():
            attributes[name] = attrib.to_attr()

        attributes["_attributes"] = attribs
        attributes["_bases"] = bases
        attributes["_inputs"] = inputs
        attributes["_produces"] = produces

        defn = attr.s(type(defn_name, (Defn,), attributes))

        if operation is not None:
            _define_operator(defn, operation, operators)

        return defn

    # Allow the decorator to be used with or without a function call
    if f is None:
        return wrapper

    return wrapper(f)
