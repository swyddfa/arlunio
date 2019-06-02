import re
import struct


class RGB8:
    @staticmethod
    def parse(color):
        """Parse a color as an RGB8 value."""
        short = re.compile(r"\A[#]*[a-fA-F0-9]{3}\Z")
        full = re.compile(r"\A[#]*[a-fA-F0-9]{6}\Z")

        if short.fullmatch(color):
            color = "".join([c * 2 for c in color.replace("#", "")])

        if full.fullmatch(color):
            return struct.unpack("BBB", bytes.fromhex(color.replace("#", "")))

        raise ValueError(f"{color} does not represent a valid RGB8 color value.")
