import re
import struct


rgb = re.compile('\A[0-9a-fA-F]{6}\Z')
rgba = re.compile('\A[0-9a-fA-F]{8}\Z')


def is_rgba(color):
    """
    This function validates if the given argument can behave
    like an RGB color. That is

    - The argument has a length of 4
    - Each element is an integer 0-225
    """

    try:
        n = len(color)

        if n != 4:
            return False

        for c in color:

            if not isinstance(c, (int,)):
                return False

            if not (0 <= c and c <= 255):
                return False

        return True

    except TypeError:
        return False


def is_rgb(color):
    """
    This function validates if the given argument can behave
    like an RGB color. That is

    - The argument has a length of 3
    - Each element is an integer 0-225
    """

    try:
        n = len(color)

        if n != 3:
            return False

        for c in color:

            if not isinstance(c, (int,)):
                return False

            if not (0 <= c and c <= 255):
                return False

        return True

    except TypeError:
        return False


def hexcolor(hexstr, alpha=False):
    """
    This function converts colours written as a hex code - like
    those found on the web into an RGB or RGBA format needed by
    Image objects.

    Parameters
    ----------
    hexstr: str
        The colour code to convert
    alpha: bool, optional
        If True this will promote RGB colours to RGBA by automatically
        adding an alpha channel set to fully opaque

    Returns
    -------
    tuple:
        A tuple of length 3 or 4 depending on if the colour is RGB or RGBA
        with integer elements between 0 and 255.
    """

    if not isinstance(hexstr, (str,)):
        raise TypeError('Hex color codes must be a string!')

    is_rgb = rgb.match(hexstr)
    is_rgba = rgba.match(hexstr)

    if is_rgb and not alpha:
        return struct.unpack('BBB', bytes.fromhex(hexstr))

    if is_rgb and alpha:
        col = struct.unpack('BBB', bytes.fromhex(hexstr))
        return (*col, 255)

    if is_rgba:
        return struct.unpack('BBBB', bytes.fromhex(hexstr))

    # If we get here then the color code was not recognised!
    raise ValueError('String does not match a known color code format!')
