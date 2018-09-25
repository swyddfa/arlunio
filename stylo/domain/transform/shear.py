from stylo.domain.helpers import PolarConversion
from stylo.domain.transform import RealDomainTransform, define_transform


class HorizontalShear(PolarConversion, RealDomainTransform):
    """A horizontal shear transform."""

    def __init__(self, domain, k=0):
        super().__init__(domain)
        self.k = -k

    def _repr(self):
        return "HorizontalShear: {}".format(-self.k)

    def _get_y(self):
        return self.domain.y

    def _get_x(self):

        xs = self.domain.x
        ys = self.domain.y

        def mk_xs(width, height):
            return xs(width, height) + self.k * ys(width, height)

        return mk_xs


class VerticalShear(PolarConversion, RealDomainTransform):
    """A vertical shear transform."""

    def __init__(self, domain, k=0):
        super().__init__(domain)
        self.k = -k

    def _repr(self):
        return "VerticalShear: {}".format(-self.k)

    def _get_x(self):
        return self.domain.x

    def _get_y(self):

        xs = self.domain.x
        ys = self.domain.y

        def mk_ys(width, height):
            return ys(width, height) + self.k * xs(width, height)

        return mk_ys


vertical_shear = define_transform(VerticalShear)
horizontal_shear = define_transform(HorizontalShear)
