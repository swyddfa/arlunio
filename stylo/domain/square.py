from .rectangular import RectangularDomain


class SquareDomain(RectangularDomain):
    """ A domain of the form :math:`[a, b] \\times [a, b] \\subset \\mathbb{R}^2`."""

    def __init__(self, x_min, x_max):
        super().__init__(x_min, x_max, x_min, x_max)

    @RectangularDomain.xmin.setter
    def xmin(self, value):
        RectangularDomain.xmin.fset(self, value)
        RectangularDomain.ymin.fset(self, value)

    @RectangularDomain.ymin.setter
    def ymin(self, value):
        RectangularDomain.ymin.fset(self, value)
        RectangularDomain.xmin.fset(self, value)

    @RectangularDomain.xmax.setter
    def xmax(self, value):
        RectangularDomain.xmax.fset(self, value)
        RectangularDomain.ymax.fset(self, value)

    @RectangularDomain.ymax.setter
    def ymax(self, value):
        RectangularDomain.ymax.fset(self, value)
        RectangularDomain.xmax.fset(self, value)


class UnitSquare(SquareDomain):
    """The domain :math:`[0, 1] \\times [0, 1] \\subset \\mathbb{R}^2`."""

    def __init__(self):
        super().__init__(0, 1)

    @SquareDomain.xmax.setter
    def xmax(self, value):
        raise AttributeError("can't set attribute")

    @SquareDomain.xmin.setter
    def xmin(self, value):
        raise AttributeError("can't set attribute")

    @SquareDomain.ymin.setter
    def ymin(self, value):
        raise AttributeError("can't set attribute")

    @SquareDomain.ymax.setter
    def ymax(self, value):
        raise AttributeError("can't set attribute")
