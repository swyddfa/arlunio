import inspect
import logging

from typing import Any, ClassVar, Dict, List, Optional

import attr

logger = logging.getLogger(__name__)


def _format_type(obj: Optional[Any] = None, type_: Optional[Any] = None) -> str:
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


@attr.s(auto_attribs=True, repr=False, frozen=True)
class DefnSignature:
    """A class that represents the 'function signature' of a definition."""

    produces: Any
    """The type of object the definition produces."""

    def __repr__(self):
        t = _format_type(type_=self.produces)
        return f"Defn[{t}]"


class _BaseDefn(type):
    """A metaclass for prodviding a few goodies on the definition class itself."""

    def __getitem__(self, key):
        return DefnSignature(produces=key)


@attr.s(auto_attribs=True)
class Defn(metaclass=_BaseDefn):
    """Defn, short for 'Definition' is the object that powers the rest of
    :code:`arlunio`.
    """

    ATTR_ID: ClassVar[str] = "arlunio.attribute"

    OP_ADD: ClassVar[str] = "addition"
    OP_AND: ClassVar[str] = "and"
    OP_DIV: ClassVar[str] = "division"
    OP_FLOORDIV: ClassVar[str] = "floor_division"
    OP_LSHIFT: ClassVar[str] = "left_shift"
    OP_MATMUL: ClassVar[str] = "matrix_multiplication"
    OP_MOD: ClassVar[str] = "modulus"
    OP_MUL: ClassVar[str] = "multiplication"
    OP_OR: ClassVar[str] = "or"
    OP_POW: ClassVar[str] = "power"
    OP_RSHIFT: ClassVar[str] = "right_shift"
    OP_SUB: ClassVar[str] = "subtraction"
    OP_XOR: ClassVar[str] = "exclusive_or"

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
        attributes = self.attributes(inherited=True)
        bases = dict(self._bases)

        logger.debug("--> Attributes: %s", attributes)
        logger.debug("--> Bases: %s", bases)

        for name, defn in bases.items():

            if name in kwargs:
                logger.debug("%s: Using user provided override, %s", name, kwargs[name])
                args[name] = kwargs[name]
                continue

            attrs = {name: attributes[name] for name in defn.attribs(inherited=True)}
            instance = defn(**attrs)
            logger.debug("%s: Created instance, %s", name, instance)

            # And then evaluate it!
            args[name] = instance(**kwargs)

        message = "Executing '%s' with %s"
        logger.debug(message, self.__class__.__name__, args.keys())

        return self._impl(**args, **self.attributes())

    def _special_method(self, operation, a, b):
        """Implements the special methods in a standardized way."""

        op_name = operation.capitalize().replace("_", " ")
        a_is_defn = isinstance(a, Defn)
        b_is_defn = isinstance(b, Defn)

        t1 = type(a) if not a_is_defn else a.produces()
        t2 = type(b) if not b_is_defn else b.produces()

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

    def attributes(self, inherited=False):
        """Return all attributes and their values on this definition instance.

        Parameters
        ----------
        inherited:
            If :code:`True` return all inherited attributes also.
        """

        if inherited:
            return {
                a.name: getattr(self, a.name)
                for a in attr.fields(self.__class__)
                if Defn.ATTR_ID in a.metadata
            }

        return {
            a.name: getattr(self, a.name)
            for a in attr.fields(self.__class__)
            if not a.metadata[Defn.ATTR_ID]["inherited"]
        }

    @classmethod
    def attribs(cls, inherited=False):
        """Return all attributes defined on this definition.

        Parameters
        ----------
        inherited:
            If :code:`True` return all inherited attributes also.
        """

        if inherited:
            return {a.name: a for a in attr.fields(cls) if Defn.ATTR_ID in a.metadata}

        return {
            a.name: a
            for a in attr.fields(cls)
            if not a.metadata[Defn.ATTR_ID]["inherited"]
        }

    @classmethod
    def bases(cls):
        """Return all the definitions this defintion is derived from."""

        if not hasattr(cls, "_bases"):
            return {}

        return dict(cls._bases)

    @classmethod
    def inputs(cls, inherited=True):
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
        rtype = inspect.signature(cls._impl).return_annotation

        if rtype == inspect._empty:
            return Any

        return rtype


@attr.s(auto_attribs=True)
class DefnInput:
    """A class that represents an input to a definition"""

    name: str
    """The name of the input."""

    dtype: Any
    """The type of the input"""

    inherited: bool
    """Flag to indicate if the input has been inherited from another definition."""

    sources: Optional[List[Defn]] = None
    """List of definitions to indicate which definitions an input has been inherited
    from."""


def _define_attribute(param: inspect.Parameter) -> attr.Attribute:
    """Given a parameter that represents some definition's attribute, write the
    corresponding attrs instance."""

    args = {"default": param.default, "kw_only": True}
    args["metadata"] = {Defn.ATTR_ID: {"inherited": False}}

    if param.annotation != inspect.Parameter.empty:
        args["type"] = param.annotation

        # TODO: Something, something validation...
        # args["validator"] = ...

    return attr.ib(**args)


def _inherit_attributes(defn: Defn, attributes):
    """Given a definition and the attributes for the current definition under
    construction copy over its attributes."""

    # Only look at the fields that represent attributes.
    for attrib in (a for a in attr.fields(defn) if a.metadata[Defn.ATTR_ID]):

        # For now we will skip any attributes that have already been defined.
        # This means that any definitions that share the same attribute name will
        # inherit the same value.
        #
        # This is probably what you would want in most(?) cases, but I'm sure we will
        # need the ability to do something more clever in the future...
        if attrib.name in attributes:
            continue

        metadata = dict(**attrib.metadata)
        metadata[Defn.ATTR_ID] = {"inherited": True}

        # It seems that the best way to copy an attrs attribute from one class to
        # another is to construct a fresh instance, copying over all the fields from
        # the source...
        attributes[attrib.name] = attr.ib(
            converter=attrib.converter,
            default=attrib.default,
            kw_only=attrib.kw_only,
            repr=False,
            metadata=metadata,
            validator=attrib.validator,
        )


def _inherit_inputs(defn: Defn, inputs):
    """Given a definition and the inputs for the current definition under construction
    copy over its inputs.

    Parameters
    ----------
    defn:
        The definition to inherit inputs from
    inputs:
        The dictionary carrying the inputs for the definition under construction.
    """
    logger.debug("Inherting inputs from definition: %s", defn.__name__)

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


def _process_parameters(
    signature: inspect.Signature, attributes: Dict[str, Any]
) -> List[inspect.Parameter]:
    """Ensure that the input parameters for the defintion are well defined.

    All parameters must carry a type annotation, if the annotation is not a
    Defn the parameter will be registered as an input that must be given when
    evaluating a definiton.

    Otherwise if the annotation is another definition then both the inputs and
    attributes of that definition will be inherited.
    """

    # Input parameters are any arguments that are not attributes
    params = [p for p in signature.values() if p.name not in attributes]

    # We will hold a dict of definitions we are based on.
    defns = {}

    # As well as a dict of inputs required to evaluate the definiton.
    inputs = {}

    for param in params:

        if param.annotation == inspect.Parameter.empty:
            raise TypeError(f"Missing type annotation for parameter '{param.name}'")

        if issubclass(param.annotation, Defn):
            defns[param.name] = param.annotation
            continue

        inpt = DefnInput(name=param.name, dtype=param.annotation, inherited=False)
        inputs[inpt.name] = inpt

    # Now for each definition, inherit its attributes and inputs.
    for defn in defns.values():
        _inherit_attributes(defn, attributes)
        _inherit_inputs(defn, inputs)

    return defns, inputs


_OPERATOR_POOL = {}


def _define_operator(defn: Defn, operation: str, operator_pool):
    """Given a definition, check to see if it matches the criteria to be an operator."""

    attrs = defn.attribs(inherited=True)

    if "a" not in attrs.keys() or "b" not in attrs.keys():
        message = "Operators must define 2 attributes 'a' and 'b'"
        raise TypeError(message)

    a = attrs["a"].type
    b = attrs["b"].type

    if a is None:
        raise TypeError("Operator input 'a' is missing a valid type annotation")

    if b is None:
        raise TypeError("Operator input 'b' is missing a valid type annotation")

    if isinstance(a, DefnSignature):
        a = a.produces

    if isinstance(b, DefnSignature):
        b = b.produces

    key = (operation, a, b)

    if key in operator_pool:
        raise TypeError(
            f"A {operation} operator between {a} and {b} has already been defined"
        )

    operator_pool[key] = defn


def definition(f=None, *, operation: str = None, operator_pool=None):
    """Create a new Definition.

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

        name = fn.__name__
        operators = operator_pool if operator_pool is not None else _OPERATOR_POOL

        KW_ONLY = inspect.Parameter.KEYWORD_ONLY
        signature = inspect.signature(fn).parameters

        attrs = [attr for attr in signature.values() if attr.kind == KW_ONLY]

        attributes = {
            "__doc__": inspect.getdoc(fn),
            "__module__": fn.__module__,
            "_impl": staticmethod(fn),
            "_operators": operators,
        }

        for a in attrs:
            attributes[a.name] = _define_attribute(a)

        bases, inputs = _process_parameters(signature, attributes)
        attributes["_bases"] = bases
        attributes["_inputs"] = inputs

        defn = attr.s(type(name, (Defn,), attributes))

        if operation is not None:
            _define_operator(defn, operation, operators)

        return defn

    # Allow the decorator to be used with or without a function call
    if f is None:
        return wrapper

    return wrapper(f)
