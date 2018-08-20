from abc import ABC, abstractmethod
import numpy as np


class RealDomain(ABC):
    """Encapsulates the notion of a mathematical domain in :math:`\\mathbb{R}^2`

    This class only defines the interface that every instance of :class:`RealDomain`
    must adhere to. In order to make use of this interface you need to use one of the
    many implementations such as :class:`RectangularDomain`.

    There are two coordinate systems that are currently supported by :class:`RealDomain`
    objects, these are the :term:`Cartesian coordinates` and :term:`Polar coordinates`.

    """

    _coords = "xyrt"

    def __getitem__(self, key):

        return lambda w, h: tuple(
            self.__getattribute__(c)(w, h) for c in key if c in self._coords
        )

    @property
    def x(self):
        """Returns a function in width and height that returns the values of
        the :math:`x` coordinate."""
        return self._get_xs()

    @property
    def y(self):
        """Returns a function in width and height that returns the values of
        the :math:`y` coordinate."""
        return self._get_ys()

    @property
    def r(self):
        """Returns a function in width and height that returns the values of
        the :math:`r` coordinate."""
        return self._get_rs()

    @property
    def t(self):
        """Returns a function in width and height that returns the values of
        the :math:`\\theta` coordinate."""
        return self._get_ts()

    @abstractmethod
    def _get_xs(self):
        """:code:`Domain` instances should implement this function to return a
        function matching the one described in the :code:`x` property"""
        pass

    @abstractmethod
    def _get_ys(self):
        """:code:`Domain` instances should implement this function to return a
        function matching the one described in the :code:`y` property"""
        pass

    @abstractmethod
    def _get_rs(self):
        """:code:`Domain` instances should implement this function to return a
        function matching the one described in the :code:`r` property"""
        pass

    @abstractmethod
    def _get_ts(self):
        """:code:`Domain` instances should implement this function to return a
        function matching the one described in the :code:`t` property"""
        pass


class PolarConversion:
    """A helper class for defining new domain classes.

    Say you are implementing a new class, perhaps the :code:`Translation` domain
    transform where the interesting part of that class is implementing the shift in
    :code:`x` or the shift in :code:`y`. The implementation of the :code:`r` and
    :code:`t` is then done with respect to the shifted :code:`x` and :code:`y`

    This class provides implementations of the :code:`_get_rs` and :code:`_get_ts` that
    handle this conversion for you automatically, leaving you to focus on implementing
    the transforms that interest you.

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

    def _get_rs(self):
        """The conversion to the radial component in terms of :math:`x` and :math:`y`.

        .. math::

           r = \\sqrt{x^2 + y^2}
        """

        xs = self._get_xs()
        ys = self._get_ys()

        def mk_rs(width, height):

            x = xs(width, height)
            y = ys(width, height)

            return np.sqrt(x * x + y * y)

        return mk_rs

    def _get_ts(self):
        """The conversion to the angular component in terms of :math:`x` and :math:`y`.

        .. math::

           \\theta = \\tan^{-1}{\\left(\\frac{y}{x}\\right)}
        """

        xs = self._get_xs()
        ys = self._get_ys()

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
    implementing the transforms that interest you.

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

    def _get_xs(self):
        """The conversion to the :math:`x` component in terms of :math:`r` and
        :math:`\\theta`

        .. math::

           x = r\\cos{(\\theta)}

        """

        rs = self._get_rs()
        ts = self._get_ts()

        def mk_xs(width, height):

            r = rs(width, height)
            t = ts(width, height)

            return r * np.cos(t)

        return mk_xs

    def _get_ys(self):
        """The conversion to the :math:`y` component in terms of :math:`r` and
        :math:`\\theta`

        .. math::

           y = r\\sin{(\\theta)}

        """

        rs = self._get_rs()
        ts = self._get_ts()

        def mk_ys(width, height):

            r = rs(width, height)
            t = ts(width, height)

            return r * np.sin(t)

        return mk_ys
