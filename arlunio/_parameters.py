import inspect

from typing import Any, ClassVar, Dict, List

import attr

from ._core import Collection, Key


def _prepare_parameter(param, attribs):
    """Given a parameter and a bag of attributes, create an instance of it passing the
    right attributes into the constructor."""

    names = {a.name for a in attr.fields(param) if a.metadata[Parameter.ATTR_ID]}
    args = {name: attribs[name] for name in names}

    return param(**args)


@attr.s(auto_attribs=True)
class Parameter:
    META_ID: ClassVar[str] = "arlunio.parameter"
    ATTR_ID: ClassVar[str] = "arlunio.parameter.attribute"

    def __call__(self, width: int, height: int):
        args = dict(self.parameters)
        attribs = self.attributes

        for name in args:

            if name == "width" and args[name] == inspect.Parameter.empty:
                args[name] = width
                continue

            if name == "height" and args[name] == inspect.Parameter.empty:
                args[name] = height
                continue

            # Else it must be a derived parameter so evaluate it...
            p = _prepare_parameter(args[name], attribs)
            args[name] = p(width, height)

        return self._definition(**args, **self.attribs)

    @property
    def attributes(self):
        """All attributes for the parameter definition."""
        return {
            a.name: getattr(self, a.name)
            for a in attr.fields(self.__class__)
            if Parameter.ATTR_ID in a.metadata
        }

    @property
    def attribs(self):
        """Any non-inherited attributes for the parameter definition."""
        return {
            a.name: getattr(self, a.name)
            for a in attr.fields(self.__class__)
            if not a.metadata[Parameter.ATTR_ID]["inherited"]
        }


def _define_attribute(param: inspect.Parameter) -> attr.Attribute:
    """Given the parameter that represents some arlunio attribute, create the
    corresponding attrs definition.
    """

    args = {"default": param.default, "kw_only": True}
    args["metadata"] = {Parameter.ATTR_ID: {"inherited": False}}

    if param.annotation != inspect.Parameter.empty:
        args["type"] = param.annotation
        args["validator"] = [attr.validators.instance_of(param.annotation)]

    return attr.ib(**args)


def _inherit_attributes(param: Parameter, attributes):
    """Given a parameter and the attributes dict for the parameter under construction,
    inherit its attributes."""

    # Only look at the fields that have been defined to be a parameter attribute
    for attrib in (a for a in attr.fields(param) if a.metadata[Parameter.ATTR_ID]):

        # For now skip any attributes that have already been defined.
        if attrib.name in attributes:
            continue

        metadata = dict(**attrib.metadata)
        metadata[Parameter.ATTR_ID] = {"inherited": True}

        # It seems that the best way to copy an attrs attribute from one class to
        # another is to construct a fresh instance based on source...
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
    """Check each of the input parameters in the definition and process them.

    First this function checks to see if the inputs are either a known base parameter
    e.g. :code:`width` or :code:`height`. Or otherwise the input carries a type
    annotation declaring what parameter it represents.

    Once it has checked that the input parameters are well defined, it adds additional
    attribute definitions to expose the attributes of the parameter
    """

    # Determine which of the args in the signature are not attributes
    params = [p for p in signature.values() if p.name not in attributes]

    # We will build a list of all the parameter definitions that this parameter is
    # derived from.
    param_definitions = []

    for param in params:

        if param.annotation == inspect.Parameter.empty:
            if param.name in {"width", "height"}:
                continue

            raise TypeError(f"Unknown parameter '{param.name}''")

        if not issubclass(param.annotation, Parameter):
            raise TypeError(
                f"Invalid input '{param.name}', type '{param.annotation.__name__}'"
                " is not a Parameter"
            )

        param_definitions.append(param.annotation)

    # For each of the parameters we derive from, inherit its attributes
    for pdef in param_definitions:
        _inherit_attributes(pdef, attributes)

    return params


# The default parameter collection
Parameters = Collection()


def parameter(f=None, *, collection=None):
    """Define a new parameter."""

    if collection is None:
        collection = Parameters

    def wrapper(pdef):

        name = pdef.__name__

        kw_only = inspect.Parameter.KEYWORD_ONLY
        signature = inspect.signature(pdef).parameters

        attrs = [attr for attr in signature.values() if attr.kind == kw_only]

        attributes = {
            "__doc__": inspect.getdoc(pdef),
            "_definition": staticmethod(pdef),
        }

        for a in attrs:
            attributes[a.name] = _define_attribute(a)

        params = _process_parameters(signature, attributes)
        attributes["parameters"] = {p.name: p.annotation for p in params}

        p = attr.s(type(name, (Parameter,), attributes))
        collection._items[Key.fromstring(name)] = p

        return p

    # Allow the decorator to be used with or without a function call
    if f is None:
        return wrapper

    return wrapper(f)
