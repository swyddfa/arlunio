import arlunio as ar

from arlunio import Defn, Mask


@ar.definition(operation=Defn.OP_ADD)
def MaskAdd(width, height, *, a: Defn[Mask] = None, b: Defn[Mask] = None):
    """Add any two mask producing definitions together.

    The resulting defintion will return a mask that is :code:`True` if a given point
    is :code:`True` in either :code:`a` or :code:`b`.

    Attributes
    ----------
    a:
        The first mask
    b:
        The second mask

    Examples
    --------
    This definition is used implicitly when adding two masks together

    .. arlunio-image::
       :include-code: before

       import arlunio as ar
       from arlunio.lib import Circle, Square

       c1 = Square(xc=-0.25, yc=-0.25, size=0.55)
       c2 = Circle(xc=0.25, yc=0.25, r=0.7)

       c = c1 + c2
       image = ar.fill(c(1920,1080))

    Or can be used directly

    .. arlunio-image::
       :include-code: before

       import arlunio as ar
       from arlunio.lib import Circle, MaskAdd, Square

       a = Square(xc=-0.25, yc=-0.25, size=0.55)
       b = Circle(xc=0.25, yc=0.25, r=0.7)

       c = MaskAdd(a=a, b=b)
       image = ar.fill(c(1920, 1080))
    """

    return ar.any(a(width, height), b(width, height))


@ar.definition(operation=Defn.OP_SUB)
def MaskSub(width, height, *, a: Defn[Mask] = None, b: Defn[Mask] = None):
    """Subtract one mask away from another mask.

    The resulting definition will return a mask that is :code:`True` only if a given
    point is in :code:`a` **and not** in :code:`b`.

    .. note::

       You will get very different results depending on which way around you set
       :code:`a` and :code:`b`!

    Attributes
    ----------
    a:
        The first "base" mask
    b:
        The second mask that defines the region to remove from :code:`a`

    Examples
    --------
    This definition is used implicitly when subtracting one mask from another

    .. arlunio-image::
       :include-code: before

       import arlunio as ar
       from arlunio.lib import Circle, Square

       c1 = Square(xc=-0.25, yc=-0.25, size=0.55)
       c2 = Circle(xc=0.25, yc=0.25, r=0.7)

       c = c1 - c2
       image = ar.fill(c(1920,1080))

    Or can be used directly

    .. arlunio-image::
       :include-code: before

       import arlunio as ar
       from arlunio.lib import Circle, MaskMul, Square

       a = Square(xc=-0.25, yc=-0.25, size=0.55)
       b = Circle(xc=0.25, yc=0.25, r=0.7)

       c = MaskMul(a=b, b=a)
       image = ar.fill(c(1920, 1080))
    """
    return ar.all(a(width, height), ar.invert(b(width, height)))


@ar.definition(operation=Defn.OP_MUL)
def MaskMul(width, height, *, a: Defn[Mask] = None, b: Defn[Mask] = None):
    """Muliply any two mask producing definitions together.

    The resulting definition will return a mask that is :code:`True` only if a given
    point is in both :code:`a` and :code:`b`.

    Attributes
    ----------
    a:
        The first mask
    b:
        The second mask

    Examples
    --------
    This definition is used implicitly when multiplying two masks together

    .. arlunio-image::
       :include-code: before

       import arlunio as ar
       from arlunio.lib import Circle, Square

       c1 = Square(xc=-0.25, yc=-0.25, size=0.55)
       c2 = Circle(xc=0.25, yc=0.25, r=0.7)

       c = c1 * c2
       image = ar.fill(c(1920,1080))

    Or can be used directly

    .. arlunio-image::
       :include-code: before

       import arlunio as ar
       from arlunio.lib import Circle, MaskMul, Square

       a = Square(xc=-0.25, yc=-0.25, size=0.55)
       b = Circle(xc=0.25, yc=0.25, r=0.7)

       c = MaskMul(a=a, b=b)
       image = ar.fill(c(1920, 1080))
    """
    return ar.all(a(width, height), b(width, height))
