import PIL.ImageColor as Color


def getcolor(*args, **kwargs):
    """Exactly as Pillow's getrgb function."""

    return Color.getcolor(*args, **kwargs)


def getcolorf(*args, **kwargs):
    """Exactly as Pillow's getrgb function, but the values are returned as floats."""

    col = Color.getcolor(*args, **kwargs)
    return tuple([c / 255 for c in col])
