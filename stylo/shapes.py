import enum
import inspect
import logging
import pkg_resources

import numpy as np

from .color import RGB8
from .image import Image
from .loaders import load_parameters


Parameter = load_parameters()
logger = logging.getLogger(__name__)


class Shape:
    """The base class for all shapes."""

    def __init__(
        self, *, scale=1, origin=None, properties=None, color=None, background=None
    ):

        if color is None:
            color = "#000000"

        self.scale = scale
        self.origin = origin

        self.color = color
        self.background = background

        self._properties = properties

    def __repr__(self):
        name = self.__class__.__name__
        property_string = ", ".join(f"{k}={v}" for k, v in self._properties.items())

        return f"{name}({property_string})"

    def __call__(self, width, height, colorspace=None):

        if colorspace is None:
            colorspace = RGB8

        image = Image.new(
            width, height, background=self.background, colorspace=colorspace
        )

        mask = self.mask(width, height)
        fg_color = colorspace.parse(self.color)
        image[mask] = fg_color

        return image

    def _prepare_arguments(self, width, height):
        """Prepare all the arguments to pass to the mask function."""

        args = dict(self._properties)

        for p in self.parameters:
            parameter = getattr(Parameter, p)
            args[p] = parameter(width, height, self.scale)

        return args

    def mask(self, width, height):
        """Return a mask with the given width and height of the shape."""
        args = self._prepare_arguments(width, height)
        return self._mask(**args)

    @property
    def parameters(self):
        """Return the parameters the shape is defined with respect to."""
        params = inspect.signature(self._mask).parameters
        parameters = [k for k in params.keys() if k not in self._properties]

        return frozenset(parameters)


def _shape_init(f):
    """This defines the :code:`__init__` method for new shapes.

    Any kewyord only argument in a shape's mask function become a property
    of the resulting shape. This function will write the :code:`__init__`
    method for this new shape and has the following behavior.

    - If a property is given by the user the new shape instance will use
      that value.
    - If a property is not given by the user, the instance will use the
      default value.
    - Any keyword arguments that are not recognised as a property will be
      passed down to the base class' :code:`__init__` method.

    :param f: The user's mask function that defines the shape.
    :type f: function.
    """

    defaults = {} if f.__kwdefaults__ is None else f.__kwdefaults__
    property_string = " ".join(f"{k}={v}" for k, v in defaults.items())

    logger.debug(f"--> Shape has default properties: {property_string}")

    def init(self, *args, **kwargs):

        # This will hold the keyword arguments we pass down to the super class
        super_kwargs = {}
        properties = dict(defaults)

        for key, value in kwargs.items():

            # If the user has set a property, override the default.
            if key in properties:
                properties[key] = value
                continue

            # Otherwise, pass the keyword down to the base class.
            super_kwargs[key] = value

        # It appears that the implicit form of super() cannot work
        # with classes constructed using the `type()` function.
        #
        # It also isn't obvious if this will be fixed in a future
        # version of Python: https://bugs.python.org/issue29944
        super(self.__class__, self).__init__(
            properties=properties, *args, **super_kwargs
        )

    return init


def define_shape(f):
    """Define a new shape."""
    name = f.__name__
    logger.debug(f"Creating new shape: {f.__name__}")

    docstring = Shape.__doc__

    if f.__doc__ is not None:
        docstring += "\n" + f.__doc__

    attributes = {
        "__doc__": docstring,
        "__init__": _shape_init(f),
        "_mask": staticmethod(f),
    }

    return type(name, (Shape,), attributes)


def shape(f):
    """A decorator used to define a new shape."""
    return define_shape(f)


@shape
def Circle(x, y, *, x0=0, y0=0, r=0.8):
    """A circle."""

    xc = x - x0
    yc = y - y0

    return np.sqrt(xc * xc + yc * yc) < r * r


@shape
def Square(x, y, *, x0=0, y0=0, size=0.8):
    """A square."""

    xc = x - x0
    yc = y - y0

    size = size / 2

    return np.logical_and(np.abs(xc) < size, np.abs(y) < size)
