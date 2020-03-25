import inspect

from typing import Any, ClassVar, Dict, List

import attr


class Mask:
    """Currently just a type alias for boolean numpy arrays but gives us the flexibility
    to add smarts later."""


def _prepare_definition(defn, attributes):
    """Given a definiton and a bag of attributes, create an instance of it by passing
    in the applicable attributes into the constructor."""

    names = {a.name for a in attr.fields(defn) if a.metadata[Definition.ATTR_ID]}
    args = {name: attributes[name] for name in names}

    return defn(**args)


def _format_type(obj: Any) -> str:
    """Given an object, return an appropriate representation for its type."""

    if isinstance(obj, Definition):
        type_ = obj.produces()

        try:
            t = type_.__name__
        except AttributeError:
            t = str(type_).split(".")[-1]

        return f"{obj.__class__.__name__}[{t}]"

    type_ = type(obj)

    try:
        return type_.__name__
    except AttributeError:
        return str(type_).split(".")[-1]


_DEFN_OPERATIONS = {}


@attr.s(auto_attribs=True)
class Definition:
    """A definition is the representation of something that can be mapped onto an
    image."""

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

    def __call__(self, width: int = None, height: int = None, **kwargs):
        args = dict(self.definitions)
        attributes = self.attributes

        try:
            width, height = width
        except TypeError:
            pass

        for name in args:

            if name == "width" and args[name] == inspect.Parameter.empty:
                args[name] = width
                continue

            if name == "height" and args[name] == inspect.Parameter.empty:
                args[name] = height
                continue

            if name in kwargs:
                args[name] = kwargs[name]
                continue

            # Else it must be a definition so let's evaluate it
            defn = _prepare_definition(args[name], attributes)
            args[name] = defn(width, height)

        return self._definition(**args, **self.attribs)

    def _special_method(self, operation, a, b):
        """Implements the special methods in a standardized way."""

        op_name = operation.capitalize().replace("_", " ")
        a_is_defn = isinstance(a, Definition)
        b_is_defn = isinstance(b, Definition)

        t1 = type(a) if not a_is_defn else a.produces()
        t2 = type(b) if not b_is_defn else b.produces()

        impl = _DEFN_OPERATIONS.get((operation, t1, t2), None)

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

    @property
    def attributes(self):
        """All attributes on this definition"""
        return {
            a.name: getattr(self, a.name)
            for a in attr.fields(self.__class__)
            if Definition.ATTR_ID in a.metadata
        }

    @property
    def attribs(self):
        """All non-inherited attributes on this definition"""
        return {
            a.name: getattr(self, a.name)
            for a in attr.fields(self.__class__)
            if not a.metadata[Definition.ATTR_ID]["inherited"]
        }

    @classmethod
    def produces(cls):
        """Return the type of the object that this definition produces."""
        rtype = inspect.signature(cls._definition).return_annotation

        if rtype == inspect._empty:
            return Any

        return rtype


def _define_attribute(param: inspect.Parameter) -> attr.Attribute:
    """Given a parameter that represents some definition's attribute, write the
    corresponding attrs instance."""

    args = {"default": param.default, "kw_only": True}
    args["metadata"] = {Definition.ATTR_ID: {"inherited": False}}

    if param.annotation != inspect.Parameter.empty:
        args["type"] = param.annotation
        args["validator"] = [attr.validators.instance_of(param.annotation)]

    return attr.ib(**args)


def _inherit_attributes(defn: Definition, attributes):
    """Given a definition and the attributes for the current definition under
    construction copy over its attributes."""

    # Only look at the fields that represent attributes.
    for attrib in (a for a in attr.fields(defn) if a.metadata[Definition.ATTR_ID]):

        # For now we will skip any attributes that have already been defined.
        # This means that any definitions that share the same attribute name will
        # inherit the same value.
        #
        # This is probably what you would want in most(?) cases, but I'm sure we will
        # need the ability to do something more clever in the future...
        if attrib.name in attributes:
            continue

        metadata = dict(**attrib.metadata)
        metadata[Definition.ATTR_ID] = {"inherited": True}

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


def _process_parameters(
    signature: inspect.Signature, attributes: Dict[str, Any]
) -> List[inspect.Parameter]:
    """Ensure that the input parameters for the defintion are well defined.

    First this function will ensure any of the parameters that are not a known "base"
    (e.g. :code:`width` or :code:`height`) are instead a known :code:`Definition`.
    For any definitions that are referenced, their attributes are then exposed to the
    definition under construction.
    """

    # Input parameters are any arguments that are not attributes
    params = [p for p in signature.values() if p.name not in attributes]

    # We will hold a list of definitions we are based on.
    defns = []

    for param in params:

        if param.annotation == inspect.Parameter.empty:
            if param.name in {"width", "height"}:
                continue

            raise TypeError(f"Unknown input '{param.name}'")

        if not issubclass(param.annotation, Definition):
            raise TypeError(
                f"Invalid input '{param.name}', type '{param.annotation.__name__}'"
                " is not a Definition"
            )

        defns.append(param.annotation)

    # Now for each definition, inherit its attributes.
    for defn in defns:
        _inherit_attributes(defn, attributes)

    return params


def definition(f=None):
    """Create a new Definition."""

    def wrapper(defn):

        name = defn.__name__

        KW_ONLY = inspect.Parameter.KEYWORD_ONLY
        signature = inspect.signature(defn).parameters

        attrs = [attr for attr in signature.values() if attr.kind == KW_ONLY]

        attributes = {
            "__doc__": inspect.getdoc(defn),
            "__module__": defn.__module__,
            "_definition": staticmethod(defn),
        }

        for a in attrs:
            attributes[a.name] = _define_attribute(a)

        params = _process_parameters(signature, attributes)
        attributes["definitions"] = {p.name: p.annotation for p in params}

        return attr.s(type(name, (Definition,), attributes))

    # Allow the decorator to be used with or without a function call
    if f is None:
        return wrapper

    return wrapper(f)
