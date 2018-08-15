from stylo.domain.domain import PolarConversion
from stylo.domain.transforms.transforms import RealDomainTransform


class Translation(PolarConversion, RealDomainTransform):
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


def translate(drawable, dx=0, dy=0):
    """Apply a translation to a given drawable."""

    domain = drawable.domain
    translated = Translation(domain, -dx, -dy)
    drawable.domain = translated
