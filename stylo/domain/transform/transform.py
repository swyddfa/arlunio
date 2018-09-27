from stylo.domain import RealDomain
from stylo.domain._factory import define_domain_transform
from stylo.shape import Shape

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


class DomainTransformer:
    """A class used to apply transformations, it enables us to do the syntactic
    nicities when applying domain transforms."""

    def __init__(self, transform, *args, **kwargs):
        self.transform = transform
        self.args = args
        self.kwargs = kwargs

        self.base_transform = find_base_transform(transform)
        self.base_domain = find_base_domain(self.base_transform)
        self.name = transform.__name__.lower

    def __rrshift__(self, other):
        return self.apply_transform(other)

    def apply_transform(self, obj):

        transform = self.transform
        args = self.args
        kwargs = self.kwargs

        if isinstance(obj, (self.base_domain,)):
            return transform(obj, *args, **kwargs)

        if isinstance(obj, (Shape,)):
            obj._add_transform(lambda domain: self.transform(domain, *args, **kwargs))
            return obj

        obj_name = obj.__class__.__name__
        message = "Unable to perform a {} to a {}."
        raise TypeError(message.format(self.name, obj_name))


def define_transform(transform):
    def transform_func(*args, **kwargs):
        return DomainTransformer(transform, *args, **kwargs)

    return transform_func
