import numpy as np
from textwrap import indent

from .domain import Domain


class Translation(Domain):
    """A domain that applies a translation to the domain provided to it."""

    def __init__(self, domain, dx, dy):

        self._domain = domain
        self._dx = dx
        self._dy = dy

    def __repr__(self):
        domain = "Translation: ({0.dx}, {0.dy})".format(self)
        other_domain = repr(self.domain)

        return domain + "\n" + indent(other_domain, "  ")

    @property
    def domain(self):
        return self._domain

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


def translate(domain, dx=0, dy=0):
    """Apply a translation to a given domain."""
    return Translation(domain, dx, dy)
