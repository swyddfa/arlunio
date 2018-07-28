from .rectangular import RectangularDomain


class SquareDomain(RectangularDomain):
    """ A sqaure domain [a, b] x [a, b]"""

    def __init__(self, x_min, x_max):
        super().__init__(x_min, x_max, x_min, x_max)


class UnitSquare(SquareDomain):

    def __init__(self):
        super().__init__(0, 1)
