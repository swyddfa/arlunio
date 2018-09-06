import re
import struct
from abc import ABC, abstractmethod


rgb8_pattern = re.compile("\A[a-fA-F0-9]{6}\Z")


class ColorSpace(ABC):
    @staticmethod
    @abstractmethod
    def parse(string):
        """Parse the color from its representation."""
        pass


class RGB8(ColorSpace):
    """Represents the 8-bit RGB colorspace."""

    @staticmethod
    def parse(string):

        if rgb8_pattern.match(string):
            return struct.unpack("BBB", bytes.fromhex(string))

        raise ValueError("String does not represent a valid color.")
