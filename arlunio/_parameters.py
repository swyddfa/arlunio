import inspect

from typing import ClassVar

import attr

from ._core import Collection, Key


@attr.s(auto_attribs=True)
class Parameter:
    META_ID: ClassVar[str] = "arlunio.parameter"
    ATTR_ID: ClassVar[str] = "arlunio.parameter.attribute"

    def __call__(self, width: int, height: int):
        args = dict(self.parameters)

        for name in args:

            if name == "width" and args[name] == inspect.Parameter.empty:
                args[name] = width
                continue

            if name == "height" and args[name] == inspect.Parameter.empty:
                args[name] = height
                continue

        return self._definition(**args, **self.attributes)

    @property
    def attributes(self):
        fields = attr.fields(self.__class__)
        return {
            a.name: getattr(self, a.name)
            for a in fields
            if Parameter.ATTR_ID in a.metadata
        }


def _define_attribute(param: inspect.Parameter) -> attr.Attribute:
    """Given the parameter that represents some arlunio attribute, create the
    corresponding attrs definition.
    """

    args = {"default": param.default, "kw_only": True}
    args["metadata"] = {Parameter.ATTR_ID: True}

    if param.annotation != inspect.Parameter.empty:
        args["type"] = param.annotation
        args["validator"] = [attr.validators.instance_of(param.annotation)]

    return attr.ib(**args)


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
        params = [param for param in signature.values() if param not in attrs]

        attributes = {
            "__doc__": inspect.getdoc(pdef),
            "_definition": staticmethod(pdef),
            "parameters": {p.name: p.annotation for p in params},
        }

        for a in attrs:
            attributes[a.name] = _define_attribute(a)

        p = attr.s(type(name, (Parameter,), attributes))
        collection._items[Key.fromstring(name)] = p

        return p

    # Allow the decorator to be used with or without a function call
    if f is None:
        return wrapper

    return wrapper(f)
