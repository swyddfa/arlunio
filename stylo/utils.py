from inspect import signature


def bounded_property(
    name,
    bounded_above=None,
    bounded_above_by=None,
    bounded_below=None,
    bounded_below_by=None,
):
    """Factory function to define a bounded property.

    This function writes a property definition for a numeric bounded property.
    It can be bounded above, below or both and the bound can either be a given
    number or another attribute/property on the same class.

    The bound can be specified by a constant numeric value e.g. :code:`1` or
    :code:`2.4` in which case you use the :code:`bounded_above` and
    :code:`bounded_below` arguments.

    Alternatively to specify the bound as the value of an attribute on the
    same class then use the :code:`bounded_above_by` and :code:`bounded_below_by`
    arugments and pass in the name of the attribute as a string.

    .. note::

       You cannot simultaneously use the :code:`bounded_xxx` and
       :code:`bounded_xxx_by` version of an argument.

    :param name: The name of the property
    :param bounded_above: The value to bound the property above by. This cannot
                          be used in conjunction with :code:`bounded_above_by`
    :param bounded_below: The value to bound the property below by. This cannot
                          be used in conjunction with :code:`bounded_below_by`
    :param bounded_above_by: The name of the attribute to bound the value by. This
                             cannot be used in conjunction with :code:`bounded_above`
    :param bounded_below_by: The name of the attribute to bound the value by. This
                             cannot be used in conjunction with :code:`bounded_below`.

    :type name: str
    :type bounded_above: float, int
    :type bounded_below: float, int
    :type bounded_below_by: str
    :type bounded_above_by: str

    :raises ValueError: If the given arguments are inconsistent in some way.
    :raises TypeError: If the given arguments do not have their expected types

    :returns: The constructed property instance
    """

    # First check that the given arguments make sense.
    if bounded_below is not None and bounded_below_by is not None:
        raise ValueError('You can only use "bounded_below" or "bounded_below_by"')

    if bounded_above is not None and bounded_above_by is not None:
        raise ValueError('You can only use "bounded_above" or "bounded_above_by"')

    if bounded_below is not None and not isinstance(bounded_below, (int, float)):
        raise TypeError("The value of bounded_below must be a number.")

    if bounded_above is not None and not isinstance(bounded_above, (int, float)):
        raise TypeError("The value of bounded_above must be a number.")

    if bounded_below_by is not None and not isinstance(bounded_below_by, (str,)):
        raise TypeError("The value of bounded_below_by must be a string")

    if bounded_above_by is not None and not isinstance(bounded_above_by, (str,)):
        raise TypeError("The value of bounded_above_by must be a string")

    hidden_name = "_" + name

    type_error_message = "Value of property {0} must be a number".format(name)
    bounded_below_message = "Value of property {0} must be strictly larger than {1}"
    bounded_below_by_message = (
        "Value of property {0} must be strictly larger than the value of property {1}"
    )
    bounded_above_message = "Value of property {0} must be strictly less than {1}"
    bounded_above_by_message = (
        "Value of property {0} must be strictly less than the value of property {1}"
    )

    checks = [(lambda s, v: isinstance(v, (int, float)), TypeError(type_error_message))]

    if bounded_above is not None:
        exception = ValueError(bounded_above_message.format(name, bounded_above))
        checks.append((lambda s, v: v < bounded_above, exception))

    if bounded_above_by is not None:
        exception = ValueError(bounded_above_by_message.format(name, bounded_above_by))
        checks.append(
            (lambda s, v: v < s.__getattribute__(bounded_above_by), exception)
        )

    if bounded_below is not None:
        exception = ValueError(bounded_below_message.format(name, bounded_below))
        checks.append((lambda s, v: v > bounded_below, exception))

    if bounded_below_by is not None:
        exception = ValueError(bounded_below_by_message.format(name, bounded_below_by))
        checks.append(
            (lambda s, v: v > s.__getattribute__(bounded_below_by), exception)
        )

    def getter(self):
        return self.__getattribute__(hidden_name)

    def setter(self, value):

        for (value_ok, err) in checks:
            if not value_ok(self, value):
                raise err

        self.__setattr__(hidden_name, value)

    return property(fget=getter, fset=setter)


def get_parameters(f):
    """
    Given a function f, return a tuple of all its
    parameters
    """

    return tuple(signature(f).parameters.keys())


class Mappable:
    """A base class for classes that want to map themselves onto a :code:`Domain`.

    For example the :code:`Shape` object takes the definition for some shape defined on
    some subset of :math:`\\mathbb{R}^2` (modelled by and instance of
    :code:`RealDomain`) and returns a boolean array that indicates which parts of the
    domain make up that shape.

    Similarly the :code:`Colormap` object takes the definition for some colormap and
    returns a numpy array representing the color at each point in the domain.

    What this class does is handle the boilerplate required to apply a domain to its
    arguments, while documenting the methods needed to be overriden if some custom
    behavior is required.
    """

    pass
