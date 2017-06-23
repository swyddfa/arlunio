
def ellipse(x0, y0, a, b, r, pt=0.2, fill=False):
    """
    An ellipse can be defined in the following manner:

        1/a(x - x0)^2 + 1/b(y - y0)^2 = r^2

    This function returns a function in (x, y) and will
    return true if the given point is in the ellipse

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
    r : float
        This represents the radius of the ellipse
    pt : float, optional
        Represents the thickness of the lines of the ellipse.
        Default: 0.2
    fill : bool, optional
        Fill the ellipse rather than outline it
        Default: False
        **Note:** If fill is true, this function will ignore the value
        of pt
    """

    lhs = lambda x, y: 1/a*(x - x0)**2 + 1/b*(y - y0)**2

    if fill:

        def ell(x, y):

            if lhs(x, y) <= r**2:
                return True

            return False

        return ell

    else:

        def ipse(x, y):

            val = lhs(x, y)

            if val <= (r + pt)**2 and val >= (r - pt)**2:
                return True

            return False
        return ipse


def circle(x0, y0, r, *args, **kwargs):
    """
    A circle can be defined in the following manner:

        (x - x0)^2 + (y - y0)^2 = r^2

    This function returns a function in (x, y) and
    will return true if the point is in the circle

    Arugments:
    ----------

    x0 : float
        This is the x coordinate of the circle's center
    y0 : float
        This is the y coordinate of the circle's center
    r : float
        This represents the radius of the ellipse
    pt : float, optional
        Represents the thickness of the lines of the circle.
        Default: 0.2
    fill : bool, optional
        Fill the circle rather than outline it
        Default: False
        **Note:** If fill is true, this function will ignore the value
        of pt
    """

    return ellipse(x0, y0, 1, 1, r, *args, **kwargs)


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


def rectangle(x0, y0, width, height, pt=0.2, fill=False):
    """
    Returns a function in (x, y) which returns true
    when the given point in in/on the rectangle defined by the
    arguments.

    Arguments:
    ----------

    x0 : float
        Represents the x-coordinate of the rectangle's center
    y0 : float
        Represents the y-coordinate of the rectangle's center
    width : float
        Represents the width of the rectangle
    height : float
        Represents the height of the rectangle
    pt : float, optional
        Represents the thickness of the lines of the rectangle.
        Default: 0.2
    fill : bool, optional
        Fill the rectangle rather than outline it
        Default: False
        **Note:** If fill is true, this function will ignore the value
        of pt
    """
    left = x0 - (width / 2)
    right = x0 + (width / 2)
    top = y0 + (height / 2)
    bottom = y0 - (height / 2)

    def rect(x, y):

        if x >= left and x <= right and\
           y >= bottom and y <= top:
            return True

        return False

    if fill:
        return rect

    def small(x, y):

        if x >= left + pt and x <= right - pt and\
           y >= bottom + pt and y <= top - pt:
            return True

        return False

    def test(x, y):

        if rect(x, y) and not small(x, y):
            return True

        return False

    return test


def square(x0, y0, size, *args, **kwargs):
    """
    Returns a function in (x, y) which returns true
    when the given point in in/on the square defined by the
    arguments.

    Arguments:
    ----------

    x0 : float
        Represents the x-coordinate of the rectangle's center
    y0 : float
        Represents the y-coordinate of the rectangle's center
    size : float
        Represents the size of the rectangle
    pt : float, optional
        Represents the thickness of the lines of the rectangle.
        Default: 0.2
    fill : bool, optional
        Fill the rectangle rather than outline it
        Default: False
        **Note:** If fill is true, this function will ignore the value
        of pt

    """
    return rectangle(x0, y0, size, size, *args, **kwargs)
