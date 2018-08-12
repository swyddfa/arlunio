from abc import ABC, abstractmethod

from stylo.domain import RealDomain


class Drawable(ABC):
    """Something that can be drawn."""

    def __init__(self):
        self._domain = None

    def __call__(self, *args, **kwargs):
        shape_func = self.shape()
        return shape_func(*args, **kwargs)

    @property
    def domain(self):
        """Returns the domain where the drawable exists."""
        if self._domain is None:
            return self.default_domain()

        return self._domain

    @domain.setter
    def domain(self, value):
        if value is not None and not isinstance(value, (RealDomain,)):
            raise TypeError("Property domain: expected RealDomain instance")

        self._domain = value

    @abstractmethod
    def default_domain(self):
        pass

    @abstractmethod
    def shape(self):
        """Returns a yes/no, function that defines the drawable's shape."""
        pass
