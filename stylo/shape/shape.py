import numpy as np
from abc import ABC, abstractmethod
from textwrap import indent

from stylo.domain import RealDomain
from stylo.utils import get_parameters


class Shape(ABC):
    """A shape constructs a boolean 2D array that represents some shape or region."""

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._transforms = []

        return instance

    def __invert__(self):
        return InvertedShape(self)

    def __and__(self, other):
        return self._logical_op(ANDedShape, other)

    def __or__(self, other):
        return self._logical_op(ORedShape, other)

    def __xor__(self, other):
        return self._logical_op(XORedShape, other)

    def __call__(self, *args, **kwargs):
        return self._render(*args, **kwargs)

    def _logical_op(self, cls, other):

        if not isinstance(other, (Shape,)):
            raise TypeError("Shape: Expected Shape instance.")

        return cls(self, other)

    def _add_transform(self, transform_func):
        self._transforms.insert(0, transform_func)

    def _apply_transform(self, domain):

        if not self._transforms:
            return domain

        for transform in self._transforms:
            domain = transform(domain)

        return domain

    def _render(self, *args, **kwargs):
        """Override this function if you want to change the default evaluation rules."""

        if len(args) > 0 and isinstance(args[0], (RealDomain,)):
            return self._render_domain(*args)

        return self._render_args(**kwargs)

    def _render_domain(self, *args):

        domain = args[0]
        shape = self.draw()

        coordinates = get_parameters(shape)
        values = domain[coordinates]

        width, height = args[1], args[2]
        return shape(*values(width, height))

    def _render_args(self, **kwargs):
        shape = self.draw()
        return shape(**kwargs)

    @property
    def parameters(self):
        return get_parameters(self.draw())

    @abstractmethod
    def draw(self):
        pass


class InvertedShape(Shape):
    """A shape that has been inverted."""

    def __init__(self, shape):
        self.shape = shape

    def __repr__(self):
        return "NOT [ " + repr(self.shape) + " ]"

    def _render_domain(self, *args):
        mask = self.shape._render_domain(*args)
        return np.logical_not(mask)

    def _render_args(self, **kwargs):
        mask = self.shape._render_args(**kwargs)
        return np.logical_not(mask)

    def draw(self):
        pass

    @property
    def parameters(self):
        return self.shape.parameters


def composite_shape_factory(op, name, op_name):
    """A factory function that returns class definitions for composite shapes
    constructed using binary logical operations such as AND, OR, etc.

    :param op: The function that implements the operation in question
    :param name: The name to give the composite class.
    :param op_name: The name of the logical operation, this will be used in the object's
                    __repr__

    :type op: callable
    :type name: str
    :type op_name: str

    :rtype: class
    """

    class CompositeShape(Shape):
        """Represents a shape that has been anded together."""

        def __init__(self, a, b):
            self.a = a
            self.b = b

        def __repr__(self):
            a_repr = indent("-- " + repr(self.a), "| ")
            b_repr = indent("-- " + repr(self.b), "| ")

            return "\n".join([op_name, a_repr, b_repr])

        def _render_domain(self, *args):
            a = self.a._render_domain(*args)
            b = self.b._render_domain(*args)

            return op(a, b)

        def _render_args(self, **kwargs):

            a_params = self.a.parameters
            b_params = self.b.parameters

            a_values = {k: v for k, v in kwargs.items() if k in a_params}
            b_values = {k: v for k, v in kwargs.items() if k in b_params}

            aas = self.a._render_args(**a_values)
            bbs = self.b._render_args(**b_values)

            return op(aas, bbs)

        @property
        def parameters(self):
            a = {*self.a.parameters}
            b = {*self.b.parameters}

            return tuple(a | b)

        def draw(self):
            pass

    CompositeShape.__name__ = name
    return CompositeShape


ANDedShape = composite_shape_factory(np.logical_and, "ANDedShape", "AND")
ORedShape = composite_shape_factory(np.logical_or, "ORedShape", "OR")
XORedShape = composite_shape_factory(np.logical_xor, "XORedShape", "XOR")
