import struct


def hex_to_rgb(hexstr):
    """
    Given hexstr, a color in Hex notation convert it
    to (R, G, B)
    """

    return struct.unpack('BBB', bytes.fromhex(hexstr))


