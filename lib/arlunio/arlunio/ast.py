from __future__ import annotations

import enum
from typing import Any, Dict, List, Optional

import attr


class NodeType(enum.IntEnum):

    SCALAR = enum.auto()
    BUILTIN = enum.auto()

    LESS = enum.auto()
    GREATER = enum.auto()

    PLUS = enum.auto()
    MINUS = enum.auto()
    MULTIPLY = enum.auto()
    DIVIDE = enum.auto()
    POW = enum.auto()

    SIN = enum.auto()
    COS = enum.auto()
    SQRT = enum.auto()

    # Maybe make the "language" smarter in the future?
    # Overload 'PLUS' and 'MULTIPLY' to handle "region" types??
    INTERSECT = enum.auto()
    UNION = enum.auto()

    FILL = enum.auto()


def binary_op(ntype: NodeType, a, b) -> Node:
    """Construct a binary operation."""

    if not isinstance(a, Node):
        a = Node.scalar(a)

    if not isinstance(b, Node):
        b = Node.scalar(b)

    return Node(ntype=ntype, children=[a, b])


class Node:
    """Base class that represents an AST node."""

    def __init__(
        self,
        ntype: NodeType,
        attributes: Optional[Dict[str, Any]] = None,
        children: Optional[List[Node]] = None,
    ):

        self.ntype = ntype
        self.attributes = attributes
        self.children = children

    @classmethod
    def scalar(cls, value):
        attribs = {"value": float(value)}
        return cls(ntype=NodeType.SCALAR, attributes=attribs)

    @classmethod
    def builtin(cls, **kwargs):
        return cls(ntype=NodeType.BUILTIN, attributes=kwargs)

    @classmethod
    def sqrt(cls, expr):
        return cls(ntype=NodeType.SQRT, children=[expr])

    @classmethod
    def intersect(cls, r1, r2):
        return cls(ntype=NodeType.INTERSECT, children=[r1, r2])

    @classmethod
    def union(cls, r1, r2):
        return cls(ntype=NodeType.UNION, children=[r1, r2])

    @classmethod
    def fill(cls, image, region, color):
        return cls(
            ntype=NodeType.FILL, children=[image, region], attributes={"color": color}
        )

    def __len__(self):
        if self.children is not None:
            return 1 + sum([len(c) for c in self.children])

        return 1

    def __lt__(self, other):
        return binary_op(NodeType.LESS, self, other)

    def __le__(self, other):
        return binary_op(NodeType.LESS, self, other)

    def __gt__(self, other):
        return binary_op(NodeType.GREATER, self, other)

    def __ge__(self, other):
        return binary_op(NodeType.GREATER, self, other)

    def __add__(self, other):
        return binary_op(NodeType.PLUS, self, other)

    def __radd__(self, other):
        return binary_op(NodeType.PLUS, other, self)

    def __sub__(self, other):
        return binary_op(NodeType.MINUS, self, other)

    def __rsub__(self, other):
        return binary_op(NodeType.MINUS, other, self)

    def __mul__(self, other):
        return binary_op(NodeType.MULTIPLY, self, other)

    def __rmul__(self, other):
        return binary_op(NodeType.MULTIPLY, other, self)

    def __truediv__(self, other):
        return binary_op(NodeType.DIVIDE, self, other)

    def __rtruediv__(self, other):
        return binary_op(NodeType.DIVIDE, other, self)

    def __pow__(self, other):
        return binary_op(NodeType.POW, self, other)

    def __rpow__(self, other):
        return binary_op(NodeType.POW, other, self)
