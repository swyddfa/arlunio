from math import sqrt, atan2


"""
An object is simply the pairing of two things. A domain, and the rule.

The domain is a transformation which takes two percentages i and j which
represent the percentage 'through' an image the current pixel is and maps it
into the mathematical domain that the rule is defined on.

This serves two purposes, one the rule can be mapped over images of
different sizes with no change, it also simplifies the process of applying
transformations and conversions.

We can split the domain up further, since the object will always eventually
be mapped onto a rectangular domain - the image, we can consider the max/min
values of x and y as their own thing.

Then we have the transformation, the function which takes the percentages
i and j and converts them to the input variables x1, x2 which we define the
rule for.

Therefore when defining the decorators they must produce an object with
the following form:

{
  'bounds': [(minX, maxX), (minY, maxY)]
  'transformation': <lambda: i, j> -> x1, x2
  'rule': <lambda x1, x2> -> RGB/RGBA
}

Then if all decorators assume this form, then we *should*, be able to
compose them nicely.

"""

def cartesian(X=[-1, 1], Y=[-1, 1]):
    """
    A function decorator which constructs a wrapper function that
    maps a given function onto a domain with given dimensions and
    cartesian coordinates
    """

    xmin, xmax = X
    ymin, ymax = Y

    def domain(f):
        """
        This is the constructed decorator made by _cartesian_ and is
        actually where we do the mapping onto the domain
        """

        def F(i, j):

            x = (1 - i)*xmin + i*xmax

            # Annoyingly convention for images is to have the orign in the
            # upper left of the image, but for maths convention for the origin
            # to be in the lower left of the image. Simply interpolating the
            # max, min y values the 'wrong' way should allow us to keep
            # thinking mathematically while the code behind the scenes works as
            # expected
            y = (1 - j)*ymax + j*ymin
            return f(x, y)

        return F

    return domain


def extend_periodically(X=[-1, 1], Y=[-1, 1]):
    """
    A function decorator which wraps a function defined on X x Y
    and extends it to an arbitrary domain by looping it back on itself
    """


    xmin, xmax = X
    xlength = xmax - xmin
    ymin, ymax = Y
    ylength = ymax - ymin

    def wrapper(f):

        def extended(x, y):

            # I have no idea why I can't find a more efficient way
            # to do this *shrug*
            while x < xmin:
                x += xlength
            while x > xmax:
                x -= xlength
            while y < ymin:
                y += ylength
            while y > ymax:
                y -= ylength

            return f(x, y)

        return extended

    return wrapper


def polar(X=[-1, 1], Y=[-1, 1]):
    """
    A function decorator which constructs a wrapper function that
    maps a given function onto a domain with given dimensions and
    polar coordinates
    """

    xmin, xmax = X
    ymin, ymax = Y

    def domain(f):
        """
        This is the constructed decorator made by _polar_ and is
        actually where we do the mapping onto the domain
        """

        def F(i, j):

            x = (1 - i)*xmin + i*xmax

            # Annoyingly convention for images is to have the orign in the
            # upper left of the image, but for maths convention for the origin
            # to be in the lower left of the image. Simply interpolating the
            # max, min y values the 'wrong' way should allow us to keep
            # thinking mathematically while the code behind the scenes works as
            # expected
            y = (1 - j)*ymax + j*ymin

            # Convert to polar coordinates
            r = sqrt(x**2 + y**2)
            t = atan2(y, x)

            return f(r, t)

        return F

    return domain
