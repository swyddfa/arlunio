import inspect

from typing import ClassVar

import attr

from ._core import Collection, Key


@attr.s(auto_attribs=True)
class Parameter:
    META_ID: ClassVar[str] = "arlunio.parameter.attribute"

    def __call__(self, width: int, height: int):
        return self._definition(width, height)


# The default parameter collection
Parameters = Collection()


def parameter(f=None, *, collection=None):
    """Define a new parameter."""

    if collection is None:
        collection = Parameters

    def wrapper(pdef):

        name = pdef.__name__
        attributes = {
            "__doc__": inspect.getdoc(pdef),
            "_definition": staticmethod(pdef),
        }

        p = attr.s(type(name, (Parameter,), attributes))
        collection._items[Key.fromstring(name)] = p

        return p

    # Allow the decorator to be used with or without a function call
    if f is None:
        return wrapper

    return wrapper(f)
