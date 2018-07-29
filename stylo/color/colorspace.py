from abc import ABC, abstractmethod


class ColorSpace(ABC):
    """Abstracts over the representation of colour."""

    def __repr__(self):
        name = self.__class__.__name__
        w, h = self.width, self.height

        return "ColorSpace<{0}, {1}x{2}>".format(name, w, h)

    @staticmethod
    @abstractmethod
    def parse(color):
        """Parse the given string as member of the color space."""
        pass

    @property
    @abstractmethod
    def data(self):
        pass

    @property
    @abstractmethod
    def width(self):
        """The width of this block of data"""
        pass

    @property
    @abstractmethod
    def height(self):
        """The height of this block of data"""
        pass

    @property
    @abstractmethod
    def bitdepth(self):
        """The bitdepth in the representation."""
        pass

    @property
    @abstractmethod
    def red(self):
        """The red color channel."""
        pass

    @property
    @abstractmethod
    def green(self):
        """The green color channel."""
        pass

    @property
    @abstractmethod
    def blue(self):
        """The blue color channel."""
        pass

    @property
    @abstractmethod
    def alpha(self):
        """The alpha color channel."""
        pass

    @abstractmethod
    def as_rgb8(self):
        pass


