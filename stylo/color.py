import re
import struct


class RGB8:
    @staticmethod
    def parse(color):
        """Parse a color as an RGB8 value."""
        pattern = re.compile(r"\A[#]*[a-fA-F0-9]{6}\Z")

        if pattern.fullmatch(color):
            return struct.unpack("BBB", bytes.fromhex(color.replace("#", "")))

        raise ValueError(f"{color} does not represent a valid RGB8 color value.")
