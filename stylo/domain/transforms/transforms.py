from abc import ABC
from textwrap import indent

from stylo.domain.domain import RealDomain


class RealDomainTransform(RealDomain, ABC):
    """A base class for transformations.

    You cannot create an instance of this class as it leaves methods
    from the base Domain class unimplemented. It is meant to be used
    as a base for classes which transform the domain in some way.
    """

    def __init__(self, domain):
        self.domain = domain

    def __repr__(self):
        domain = self._repr()
        other_domain = repr(self.domain)

        return domain + "\n" + indent(other_domain, "  ")

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, value):

        if not isinstance(value, (RealDomain,)):
            raise TypeError("Property domain: expected Domain instance.")

        self._domain = value
