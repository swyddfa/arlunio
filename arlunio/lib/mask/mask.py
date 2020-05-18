import arlunio as ar


class Mask:
    """Currently just a type alias for boolean numpy arrays but gives us the flexibility
    to add smarts later."""


@ar.definition(operation=ar.Defn.OP_ADD)
def MaskAdd(
    width: int, height: int, *, a: ar.Defn[Mask] = None, b: ar.Defn[Mask] = None
) -> Mask:
    """Add any two mask producing definitions together.

    The resulting defintion will return a mask that is :code:`True` if a given point
    is :code:`True` in either :code:`a` or :code:`b`.

    Attributes
    ----------
    a:
        The first mask
    b:
        The second mask
    """

    return ar.any(a(width=width, height=height), b(width=width, height=height))


@ar.definition(operation=ar.Defn.OP_SUB)
def MaskSub(
    width: int, height: int, *, a: ar.Defn[Mask] = None, b: ar.Defn[Mask] = None
) -> Mask:
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
    """
    return ar.all(
        a(width=width, height=height), ar.invert(b(width=width, height=height))
    )


@ar.definition(operation=ar.Defn.OP_MUL)
def MaskMul(
    width: int, height: int, *, a: ar.Defn[Mask] = None, b: ar.Defn[Mask] = None
) -> Mask:
    """Muliply any two mask producing definitions together.

    The resulting definition will return a mask that is :code:`True` only if a given
    point is in both :code:`a` and :code:`b`.

    Attributes
    ----------
    a:
        The first mask
    b:
        The second mask
    """
    return ar.all(a(width=width, height=height), b(width=width, height=height))
