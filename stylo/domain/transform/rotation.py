from stylo.domain.helpers import CartesianConversion
from stylo.domain.transform import RealDomainTransform


class Rotation(CartesianConversion, RealDomainTransform):
    """A domain that applies a rotation to the domain provided to it."""

    def __init__(self, domain, angle):
        super().__init__(domain)
        self.angle = angle

    def _repr(self):
        return "Rotation: {}".format(self.angle)

    def _get_r(self):
        return self.domain.r

    def _get_t(self):
        ts = self.domain.t

        def mk_ts(width, height):
            return ts(width, height) + self.angle

        return mk_ts


def rotate(drawable, angle):
    """Apply a rotation to a given drawable"""

    domain = drawable.domain
    rotated = Rotation(domain, angle)

    drawable.domain = rotated
    return drawable
