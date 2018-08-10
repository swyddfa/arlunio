from abc import ABC, abstractmethod


class Painter(ABC):
    """Represents the painter interface.

    A Painter is responsible for taking one or more bitmasks and converting
    it into image data to be saved as an image.
    """

    @abstractmethod
    def paint(self):
        pass
