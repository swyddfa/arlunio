from stylo.domain.domain import CartesianConversion
from stylo.domain.transforms.transforms import RealDomainTransform


class Rotation(CartesianConversion, RealDomainTransform):
    """A domain that applies a rotation to the domain provided to it."""

    def __init__(self, domain, angle):
        super().__init__(domain)
        self.angle = angle

    def _get_rs(self):
        return self.domain.r

    def _get_ts(self):
        ts = self.domain.t

        def mk_ts(width, height):
            return ts(width, height) + self.angle

        return mk_ts


def rotate(drawable, angle):
    """Apply a rotation to a given drawable"""

    domain = drawable.domain
    rotated = Rotation(domain, angle)
    drawable.domain = rotated