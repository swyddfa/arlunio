import numpy as np
from stylo.shape.shape import Shape


class ImplicitXY(Shape):
    """Define a curve using an implicit function in the :math:`x` and :math:`y`
    coordinates.

    A point :math:`(x, y)` lies on the curve defined by the function
    :math:`f(x, y)` if the following holds.

    .. math::

       f(x, y) = 0

    However since paths are one dimensional objects and have no area, if we used
    this rule as it stands we would never see the curve in question. So instead we
    introduce some error margin :math:`e > 0` and say that a point is on the curve
    if the following holds.

    .. math::

       |f(x, y)| \\leq e
    """

    def __init__(self, f, pt=0.01, above=False, below=False):
        """Construct an instance of :code:`ImplicitXY` according to the given
        parameters.

        :param f: The function that defines the curve.
        :param pt: The error margin, corresponds to :math:`e` in the above.
                   (Default: 0.01)
        :param above: If :code:`True` draw the area above the curve as a shaded
                      region (Default: :code:`False`)
        :param below: If :code:`True` draw the area underneath the curve as a shaded
                      region (Default: False)
        """
        self.f = f
        self.pt = pt
        self.above = above
        self.below = below

    def draw(self):

        if self.below:

            def below_curve(x, y):
                return self.f(x, y) >= 0

            return below_curve

        if self.above:

            def above_curve(x, y):
                return self.f(x, y) <= 0

            return above_curve

        def curve(x, y):
            error = self.f(x, y)
            return np.abs(error) <= self.pt

        return curve
