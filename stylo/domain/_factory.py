"""A :code:`Domain` is responsible for converting some abstract notion of a mathematical
space into a discrete representation. Since :code:`stylo` is about creating images this
representation is typically a 2D grid of numbers.

This document details the machinery behind the :code:`Domain` system. More specifically
how the :code:`define_domain` and :code:`define_domain_transform` functions work. It
assumes you are already familiar with how the user interacts with :code:`Domain` objects
and is written for someone who wishes to understand how they work behind the scenes.

This module contains all the code that is required to automatically write both the
definition of a new Domain type and the test case that users can use to verify that
their implementations of said domains adhere to the expected interface.
"""
from abc import ABC, abstractmethod
from textwrap import indent


def domain_getitem(self, key):
    """Enable the domain[...] syntax for domains.

    Domains support the ability to return a function in :code:`(width, height)`
    of multiple parameters, for example for a :code:`RealDomain` you might want a
    function in both the :math:`x` and :math:`y` coordinates in which case you would
    write

    .. code-block:: python

       >>> values = domain['xy']
       >>> values(N, N)
       (array([[x0, x1, ..., xN],
               [x0, x1, ..., XN],
               ...
               [x0, x1, ..., xN]]),
        array([[y0, y0, ..., y0],
               [y1, y1, ..., y1],
               ...,
               [yN, yN, ..., yN]]))

    .. note::

       The string argument :code:`'xy'` only works in the case of single letter
       parameters. For multi-character parameters such as :code:`pt` this argument
       must be some other iterable such as a tuple e.g. :code:`('x', 'pt')`.

    This function constructs the implementation for the :code:`__getitem__` method that
    will be added to new :code:`Domain` definitions

    :param self: The standard python instance argument for methods
    :param key: The input that is given to the getitem syntax e.g. :code:`'xy'`

    :type self: object
    :type key: iterable
    """

    return lambda w, h: tuple(
        self.__getattribute__(p)(w, h) for p in key if p in self._parameters
    )


def domain_property(base):
    """Construct the domain property for the domain transform base class.

    :param base: The base Domain class
    :type base: class
    """

    transform_name = base.__name__ + "Transform"

    def getter(self):
        return self._domain

    def setter(self, value):

        if not isinstance(value, (base,)):
            message = "{transform}: Expected {base} instance."
            raise TypeError(
                message.format(transform=transform_name, base=base.__name__)
            )

        self._domain = value

    return property(fget=getter, fset=setter)


def domain_call(self, width, height):
    return lambda parameters: self[parameters](width, height)


def parameters_property(parameters):
    """Given the list of parameters this function constructs a property that simply
    returns the given list. It doesn't provide a setter so that the list of parameters
    cannot be overridden."""

    def getter(self):
        return parameters

    return property(fget=getter)


def parameter_property(name):
    """Given the name of the parameter, construct the property definition that calls the
    abstract :code:`_get_name()` method that users will implement.

    :param name: The name of the parameter
    :type name: str
    """

    def getter(self):
        return self.__getattribute__("_get_" + name)()

    return property(fget=getter)


def mk_abstractmethod():
    """Construct an abstractmethod that user must override when they create an instance
    of a class.
    """

    def method(self):
        pass

    return abstractmethod(method)


def transform_init(self, domain):
    """This implements the :code:`__init__` method for DomainTransform classes."""
    self.domain = domain


def transform_repr(self):
    """This implements the :code:`__repr__` method for DomainTransform classes."""
    transform = self._repr()
    domain = repr(self.domain)

    return transform + "\n" + indent(domain, "  ")


def define_domain(name, parameters):
    """Given the name and the input parameters, construct the Domain definition.

    :param name: The name of the :code:`Domain`
    :param parameters: A list of strings that encode the names of the parameters within
           the domain

    :type name: str
    :type parameters: list(str)
    """
    params = parameters.split(",")

    attributes = {
        "_parameters": params,
        "parameters": parameters_property(params),
        "__doc__": "A docstring",
        "__getitem__": domain_getitem,
        "__call__": domain_call,
    }

    for p in params:
        attributes[p] = parameter_property(p)
        attributes["_get_" + p] = mk_abstractmethod()

    return type(name, (ABC,), attributes)


def define_domain_transform(base):
    """This constructs the class definition for a domain transform.

    :param name: The name of the base domain
    :param base: The class definition of the base domain

    :type name: str
    :type base: class
    """

    transform_name = base.__name__ + "Transform"

    attributes = {
        "__init__": transform_init,
        "__repr__": transform_repr,
        "_repr": mk_abstractmethod(),
        "domain": domain_property(base),
    }

    return type(transform_name, (base, ABC), attributes)
