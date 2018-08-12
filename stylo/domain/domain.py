from abc import ABC, abstractmethod


class RealDomain(ABC):
    """Encapsulates the notion of a mathematical domain in :math:`\\mathbb{R}^2`

    This class only defines the interface for a real domain and it not meant to be
    created directly. Refer to implementations such as :class:`RectangularDomain`
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
