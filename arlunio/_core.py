import inspect

from typing import Any, ClassVar, Dict, List

import attr


def _prepare_definition(defn, attributes):
    """Given a definiton and a bag of attributes, create an instance of it by passing
    in the applicable attributes into the constructor."""

    names = {a.name for a in attr.fields(defn) if a.metadata[Definition.ATTR_ID]}
    args = {name: attributes[name] for name in names}

    return defn(**args)


@attr.s(auto_attribs=True)
class Definition:
    """A definition is the representation of something that can be mapped onto an
    image."""

    ATTR_ID: ClassVar[str] = "arlunio.attribute"

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
