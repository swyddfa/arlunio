import numpy as np
from abc import ABC
from textwrap import indent

from .domain import RealDomain


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


class Translation(RealDomainTransform):
    """A domain that applies a translation to the domain provided to it."""

    def __init__(self, domain, dx, dy):
        super().__init__(domain)
        self._dx = dx
        self._dy = dy

    def _repr(self):
        return "Translation: ({0.dx}, {0.dy})".format(self)

    @property
    def dx(self):
        return self._dx

    @property
    def dy(self):
        return self._dy

    def _get_xs(self):

        xs = self.domain.x

        def mk_xs(width, height):
            return xs(width, height) + self.dx

        return mk_xs

    def _get_ys(self):

        ys = self.domain.y

        def mk_ys(width, height):
            return ys(width, height) + self.dy

        return mk_ys

    def _get_rs(self):

        xs = self._get_xs()
        ys = self._get_ys()

        def mk_rs(width, height):

            XS = xs(width, height)
            YS = ys(width, height)

            return np.sqrt(XS * XS + YS * YS)

        return mk_rs

    def _get_ts(self):

        xs = self._get_xs()
        ys = self._get_ys()

        def mk_ts(width, height):

            XS = xs(width, height)
            YS = ys(width, height)

            return np.arctan2(YS, XS)

        return mk_ts


def translate(drawable, dx=0, dy=0):
    """Apply a translation to a given drawable."""

    domain = drawable.domain
    translated = Translation(domain, -dx, -dy)
    drawable.domain = translated
