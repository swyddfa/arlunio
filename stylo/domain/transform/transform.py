from stylo.domain import RealDomain
from stylo.domain._factory import define_domain_transform

RealDomainTransform = define_domain_transform(RealDomain)


def find_base_transform(transform):
    """Given a domain transform, find its base class"""

    for base in transform.__bases__:

        if hasattr(base, "domain"):
            return base

    name = transform.__name__
    raise TypeError("{} is not a domain transform".format(name))


def find_base_domain(base_transform):
    """Given a base domain transform class, find the base domain that
    it transform."""

    for base in base_transform.__bases__:

        if hasattr(base, "_parameters") and not hasattr(base, "domain"):
            return base

    name = base_transform.__name__
    raise TypeError("{} is not a base domain transform".format(name))


def define_transform(transform):
    """Define a transformation function for a given domain transform.

    Given a domain transform this function will automatically write a function
    that can be used to apply the given transform to various objects in stylo.

    :param transform: The :code:`DomainTransform` to write the function for.
    """

    base_transform = find_base_transform(transform)
    base_domain = find_base_domain(base_transform)

    name = transform.__name__.lower()

    def transform_func(obj, *args, **kwargs):

        if isinstance(obj, (base_domain,)):
            return transform(obj, *args, **kwargs)

        obj_name = obj.__class__.__name__
        message = "Unable to perform a {} to a {}."
        raise TypeError(message.format(name, obj_name))

    return transform_func
