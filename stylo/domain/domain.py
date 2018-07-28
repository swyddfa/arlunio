from abc import ABC, abstractmethod


class Domain(ABC):
    """Encapsulates the notion of a mathematical domain."""

    _coords = "xyrt"

    def __getitem__(self, key):

        return lambda w, h: tuple(
            self.__getattribute__(c)(w, h) for c in key if c in self._coords
        )

    @property
    def x(self):
        """The x coordinates."""
        return self._get_xs()

    @property
    def y(self):
        """The y coordinates."""
        return self._get_ys()

    @property
    def r(self):
        """The r coordinates."""
        return self._get_rs()

    @property
    def t(self):
        """The theta coordinates."""
        return self._get_ts()

    @abstractmethod
    def _get_xs(self):
        pass

    @abstractmethod
    def _get_ys(self):
        pass

    @abstractmethod
    def _get_rs(self):
        pass

    @abstractmethod
    def _get_ts(self):
        pass
