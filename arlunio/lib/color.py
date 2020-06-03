import PIL.ImageColor as Color


def getcolor(color):
    """Exactly as Pillow's getrgb function."""

    return Color.getrgb(color)


def getcolorf(color):
    """Exactly as Pillow's getrgb function, but the values are returned as floats."""

    r, g, b = Color.getrgb(color)
    return tuple([r / 255, g / 255, b / 255])
