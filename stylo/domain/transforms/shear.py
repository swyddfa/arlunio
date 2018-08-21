from stylo.domain.domain import PolarConversion
from stylo.domain.transforms.transforms import RealDomainTransform


class HorizontalShear(PolarConversion, RealDomainTransform):
    """A horizontal shear transform."""

    def __init__(self, domain, k=0):
        super().__init__(domain)
        self.k = -k

    def _get_ys(self):
        return self.domain.y

    def _get_xs(self):

        xs = self.domain.x
        ys = self.domain.y

        def mk_xs(width, height):
            return xs(width, height) + self.k*ys(width, height)

        return mk_xs


class VerticalShear(PolarConversion, RealDomainTransform):
    """A vertical shear transform."""

    def __init__(self, domain, k=0):
        super().__init__(domain)
        self.k = -k

    def _get_xs(self):
        return self.domain.x

    def _get_ys(self):

        xs = self.domain.x
        ys = self.domain.y

        def mk_ys(width, height):
            return ys(width, height) + self.k*xs(width, height)

        return mk_ys


def vertical_shear(drawable, k):

    domain = drawable.domain
    sheared = VerticalShear(domain, k)

    drawable.domain = sheared
    return drawable


def horizontal_shear(drawable, k):

    domain = drawable.domain
    sheared = HorizontalShear(domain, k)

    drawable.domain = sheared
    return drawable
