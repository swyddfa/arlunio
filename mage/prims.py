
def ellipse(x0, y0, a, b):
    """
    An ellipse can be defined in the following manner:

        1/a(x - x0)^2 + 1/b(y - y0)^2 = r^2

    This function returns a function in (x, y) and will
    evaluate the LHS of the above equation

    Arguments:
    ----------

    x0 : float
        Represents the x coordinate of the ellipse's center
    y0 : float
        Represents the y coordinate of the ellipse's center
    a : float
        This controls how elongated the ellipse is in the x
        direction
    b : float
        This controls how elongated the ellipse is in the y
        direction
    """

    def mk_ellipse(x, y):

        return 1/a*(x - x0)**2 + 1/b*(y - y0)**2

    return mk_ellipse


def circle(x0, y0):
    """
    A circle can be defined in the following manner:

        (x - x0)^2 + (y - y0)^2 = r^2

    This function returns a function in (x, y) and
    will evaluate the LHS of the above equation

    Arugments:
    ----------

    x0 : float
        This is the x coordinate of the circle's center
    y0 : float
        This is the y coordinate of the circle's center
    """

    return ellipse(x0, y0, 1, 1)


def thicken(f, pt):
    """
    Mathematical paths are all well and good but in order
    to see them they have to have some amount of thickness.

    Given some function which describes a path and a thickness
    this function construct and returns a function which determines
    if some given y is in the neighbourhood of the given function
    at x

    Arguments:
    ----------

    f: callable
        The function you want 'thickened'
    pt: float
        Determines the size of the neighbourhood to test
        in
    """

    def test_func(x, y):

        if y >= f(x) - pt and y <= f(x) + pt:
            return True
        else:
            return False

    return test_func
