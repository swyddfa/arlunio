from stylo.domain.helpers import PolarConversion
from stylo.domain.transform import RealDomainTransform


class Translation(PolarConversion, RealDomainTransform):
    """A domain that applies a translation to the domain provided to it."""

    def __init__(self, domain, dx, dy):
        super().__init__(domain)
        self.dx = -dx
        self.dy = -dy

    def _repr(self):
        return "Translation: ({0}, {1})".format(-self.dx, -self.dy)

    def _get_x(self):

        xs = self.domain.x

        def mk_xs(width, height):
            return xs(width, height) + self.dx

        return mk_xs

    def _get_y(self):

        ys = self.domain.y

        def mk_ys(width, height):
            return ys(width, height) + self.dy

        return mk_ys


def translate(domain, dx=0, dy=0):
    """Apply a translation to a given drawable."""
    return Translation(domain, dx, dy)
