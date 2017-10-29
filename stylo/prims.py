from math import floor


def ellipse(x0, y0, a, b, r, pt=0.2, fill=False):
    """
    Mathematically we can define an ellipse to be the set
    of points :math:`(x, y)` which satisfy:

    .. math::

        \\frac{(x - x_0)^2}{a^2} + \\frac{(y - y_0)^2}{b^2} = r^2

    where:

    - :math:`(x_0, y_0)` is the center of the ellipse
    - :math:`a` is known as the semi major axis, larger values make the
      ellipse more elongated in the :math:`x`-direction
    - :math:`b` is known as the semi minor axis, larger values make the
      ellipse more elongated in the :math:`y`-direction
    - :math:`r` is the "radius" of the ellipse and controls the overall
      size of the ellipse

    This function will return another function that when given a point
    :code:`(x,y)` that will return :code:`True` if the point is in the
    ellipse.

    Parameters
    ----------

    x0 : float
        Represents the x coordinate of the ellipse's center
    y0 : float
        Represents the y coordinate of the ellipse's center
    a : float
        Represents the semi major axis of the ellipse
    b : float
        Represents the semi minor axis of the ellipse
    r : float
        Represents the "radius" of the ellipse
    pt : float, optional
        Represents the thickness of the line of the ellipse.
        Default: 0.2
    fill : bool, optional
        Fill the ellipse rather than outline it
        Default: False
        **Note:** If fill is true, this function will ignore the value
        of pt

    Returns
    -------

    function:
        A function in 2 arguments :code:`(x,y)` which returns :code:`True`
        if that point is in the ellipse defined by the above parameters
    """

    lhs = lambda x, y: ((x - x0)**2)/a**2 + ((y - y0)**2)/b**2

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
    Mathematically a circle can be defined as the set of all
    points :math:`(x, y)` that satisfy

    .. math::

        (x - x_0)^2 + (y - y_0)^2 = r^2

    This function returns another function which when given
    a point :code:`(x, y)` will return :code:`True` if that
    point is in the circle

    Parameters
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

    Returns
    -------

    function:
        A function in 2 arguments :code:`(x, y)` that returns
        :code:`True` if that point is in the circle defined by the
        above parameters
    """

    return ellipse(x0, y0, 1, 1, r, *args, **kwargs)


def between(lower, value, upper):
    """
    A simple function which provides a shorthand
    for checking if a given value is between some lower
    and upper bound

    Parameters
    ----------
    lower : float
        The lower bound to check
    value : float
        The value you want checked
    upper: float
        The upper bound to check

    Returns
    -------
    bool
        :code:`True` if :code:`lower <= value` and
        :code:`value <= upper`. :code:`False` otherwise
    """
    return lower <= value and value <= upper


def rectangle(x0, y0, width, height, pt=0.2, fill=False):
    """
    It's quite simple to define a rectangle, simply pick a
    point :math:`(x_0,y_0)` that you want to be the center
    and then two numbers which will represent the width and
    height of the rectangle.

    Parameters
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

    Returns
    -------

    function
        A function in 2 arguments :code:`(x, y)` that returns :code:`True`
        if the point is in the rectangle defined by the above parameters
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
    It's quite simple to define a square, simply pick a
    point :math:`(x_0,y_0)` that you want to be the center
    and then a number which will represent the size of the
    square.

    Parameters
    ----------

    x0 : float
        Represents the x-coordinate of the square's center
    y0 : float
        Represents the y-coordinate of the square's center
    size : float
        Represents the size of the square
    pt : float, optional
        Represents the thickness of the lines of the square.
        Default: 0.2
    fill : bool, optional
        Fill the square rather than outline it
        Default: False
        **Note:** If fill is true, this function will ignore the value
        of pt

    Returns
    -------

    function
        A function in 2 arguments :code:`(x, y)` that returns :code:`True`
        if the point is in the square defined by the parameters above
    """
    return rectangle(x0, y0, size, size, *args, **kwargs)
