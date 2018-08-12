from abc import ABC, abstractmethod
from inspect import signature

from stylo.domain.domain import RealDomain


def get_coordinate_string(function):
    """Given a function this returns a string containing each of the arguments.
    This can be used to determine which coordinate systems a given function is
    written in.

    :param function: The function to inspect
    :type function: callable

    :return: The string containing each of the argument names.
    """
    return tuple(signature(function).parameters.keys())


class Renderer(ABC):
    """The renderer interface.

    The renderer is reponsible for taking some definition of a shape to be drawn
    and converting it to a bitmask. This could be as simple as a single function,
    or a complex tree of ifs ands or buts that is "compiled" to produce a final
    shape
    """

    @abstractmethod
    def render(self, domain, definition, width, height):
        """Actually do the rendering."""
        pass

    def __call__(self, domain, definition, width, height):

        if not isinstance(domain, (RealDomain,)):
            message = "Argument domain: expected instance of a Domain object."
            raise TypeError(message)

        if not isinstance(width, (int,)) or width <= 0:
            raise ValueError("Argument width: expected positive integer")

        if not isinstance(height, (int,)) or height <= 0:
            raise ValueError("Argument height: expected positive integer")

        return self.render(domain, definition, width, height)
