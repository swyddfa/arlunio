import arlunio as ar

from arlunio import Defn, Mask


@ar.definition(operation=Defn.OP_ADD)
def MaskAdd(width, height, *, a: Defn[Mask] = None, b: Defn[Mask] = None):
    return ar.any(a(width, height), b(width, height))


@ar.definition(operation=Defn.OP_SUB)
def MaskSub(width, height, *, a: Defn[Mask] = None, b: Defn[Mask] = None):
    return ar.all(a(width, height), ar.invert(b(width, height)))


@ar.definition(operation=Defn.OP_MUL)
def MaskMul(width, height, *, a: Defn[Mask] = None, b: Defn[Mask] = None):
    return ar.all(a(width, height), b(width, height))
