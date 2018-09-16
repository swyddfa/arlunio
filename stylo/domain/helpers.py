import numpy as np


class PolarConversion:
    """A helper class for defining new domain classes.

    Say you are implementing a new class, perhaps the :code:`Translation` domain
    transform where the interesting part of that class is implementing the shift in
    :code:`x` or the shift in :code:`y`. The implementation of the :code:`r` and
    :code:`t` is then done with respect to the shifted :code:`x` and :code:`y`

    This class provides implementations of the :code:`_get_rs` and :code:`_get_ts` that
    handle this conversion for you automatically, leaving you to focus on implementing
    the transform that interest you.

    To use this class, simply include it in your :code:`class` definition as follows.

    .. code-block:: python

       class MyDomain(PolarConversion, RealDomain):

           def _get_xs(self):
              ...

            def _get_ys(self):
               ...

    .. note::

       The order in which the classes are listed is *very* important.
    """

    def _get_r(self):
        """The conversion to the radial component in terms of :math:`x` and :math:`y`.

        .. math::

           r = \\sqrt{x^2 + y^2}
        """

        xs = self._get_x()
        ys = self._get_y()

        def mk_rs(width, height):

            x = xs(width, height)
            y = ys(width, height)

            return np.sqrt(x * x + y * y)

        return mk_rs

    def _get_t(self):
        """The conversion to the angular component in terms of :math:`x` and :math:`y`.

        .. math::

           \\theta = \\tan^{-1}{\\left(\\frac{y}{x}\\right)}
        """

        xs = self._get_x()
        ys = self._get_y()

        def mk_ts(width, height):

            x = xs(width, height)
            y = ys(width, height)

            return np.arctan2(y, x)

        return mk_ts


class CartesianConversion:
    """A helper class for defining new domain classes.

    Say you are implementing a new class, perhaps the :code:`Rotation` domain transform
    where the interesting part is the adjustments to the :code:`r` and :code:`t`
    coordinates. The implementation of :code:`x` and :code:`y` is then done with respect
    to the transformed :code:`r` and :code:`t` variables.

    This class provides implementations of the :code:`_get_xs` and :code:`_get_ys`
    methods to handle this conversion for you automatically, leaving you to focus on
    implementing the transform that interest you.

    To use this class, simply include it in your :code:`class` definition as follows

    .. code-block:: python

       class MyDomain(CartesianConversion, RealDomain):

           def _get_xs(self):
               ...

           def _get_ys(self):
               ...

    .. note::

       The order in which the classes are listed is *very* important.
    """

    def _get_x(self):
        """The conversion to the :math:`x` component in terms of :math:`r` and
        :math:`\\theta`

        .. math::

           x = r\\cos{(\\theta)}

        """

        rs = self._get_r()
        ts = self._get_t()

        def mk_xs(width, height):

            r = rs(width, height)
            t = ts(width, height)

            return r * np.cos(t)

        return mk_xs

    def _get_y(self):
        """The conversion to the :math:`y` component in terms of :math:`r` and
        :math:`\\theta`

        .. math::

           y = r\\sin{(\\theta)}

        """

        rs = self._get_r()
        ts = self._get_t()

        def mk_ys(width, height):

            r = rs(width, height)
            t = ts(width, height)

            return r * np.sin(t)

        return mk_ys
