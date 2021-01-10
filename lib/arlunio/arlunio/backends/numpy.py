from __future__ import annotations

import numpy as np
import PIL.Image as Image

from arlunio import ast


def builtin_x(backend: NumpyBackend, tree: ast.Node):
    ratio = backend.width / backend.height

    scale = tree.attributes["scale"]
    stretch = tree.attributes["stretch"]
    x0 = tree.attributes["x0"]

    if not stretch and ratio > 1:
        scale = scale * ratio

    x = np.linspace(-scale, scale, backend.width)
    x = np.array([x for _ in range(backend.height)])

    return x - x0


def builtin_y(backend: NumpyBackend, tree: ast.Node):
    ratio = backend.height / backend.width

    scale = tree.attributes["scale"]
    stretch = tree.attributes["stretch"]
    y0 = tree.attributes["y0"]

    if not stretch and ratio > 1:
        scale = scale * ratio

    y = np.linspace(scale, -scale, backend.height)
    y = np.array([y for _ in range(backend.width)]).transpose()

    return y - y0


BUILTINS = {"x": builtin_x, "y": builtin_y}


class NumpyBackend:
    def __init__(self, width=1920, height=1080):
        self.width = width
        self.height = height

    def preview(self, tree: ast.Node):
        result = self.eval(tree)

        if isinstance(result, Image.Image):
            result.show()
            return result

        return result

    def eval(self, tree: ast.Node):
        ntype = tree.ntype.name.lower()
        impl = getattr(self, f"eval_{ntype}", None)

        if impl is None:
            message = f'Backend does not support node type "{tree.ntype.name}"'
            raise NotImplementedError(message)

        return impl(tree)

    def eval_builtin(self, tree: ast.Node):
        name = tree.attributes["name"]
        impl = BUILTINS.get(name, None)

        if impl is None:
            message = f'Unrecognised builtin "{name}"'
            raise NotImplementedError(message)

        return impl(self, tree)

    def eval_greater(self, tree: ast.Node):
        a, b = tree.children

        a = self.eval(a)
        b = self.eval(b)

        return a > b

    def eval_intersect(self, tree: ast.Node):
        a, *bs = tree.children
        a = self.eval(a)

        for b in bs:
            a = np.logical_and(a, self.eval(b))

        return a

    def eval_less(self, tree: ast.Node):
        a, b = tree.children

        a = self.eval(a)
        b = self.eval(b)

        return a < b

    def eval_minus(self, tree: ast.Node):
        a, *bs = tree.children
        a = self.eval(a)

        for b in bs:
            a -= self.eval(b)

        return a

    def eval_plus(self, tree: ast.Node):
        a, *bs = tree.children
        a = self.eval(a)

        for b in bs:
            a += self.eval(b)

        return a

    def eval_pow(self, tree: ast.Node):
        a, b = tree.children

        a = self.eval(a)
        b = self.eval(b)

        return a ** b

    def eval_scalar(self, tree: ast.Node):
        return tree.attributes["value"]

    def eval_sqrt(self, tree: ast.Node):
        a = tree.children[0]
        return np.sqrt(self.eval(a))
