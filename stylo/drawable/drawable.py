from abc import ABC, abstractmethod


class Drawable(ABC):
    """Something that can be drawn."""

    @property
    @abstractmethod
    def domain(self):
        """Returns the domain where the drawable exists."""
        pass

    @property
    @abstractmethod
    def shape(self):
        """Returns a yes/no, function that defines the drawable's shape."""
        pass