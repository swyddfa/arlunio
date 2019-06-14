import inspect
import json
import logging

import numpy as np

from .color import RGB8
from .image import Image
from .loaders import load_parameters

Parameter = load_parameters()
logger = logging.getLogger(__name__)


class Canvas:
    """A good canvas is what every artist needs."""

    def __init__(self, layers=None, background=None):
        self.layers = [] if layers is None else layers

    def __repr__(self):
        return f"Canvas<{len(self.layers)} layers>"

    def __add__(self, other):

        if isinstance(other, Shape):
            self.layers.append(other)
            return self

        if isinstance(other, Canvas):
            self.layers += other.layers
            return self

        raise TypeError()

    def __call__(self, width, height):
        image = Image.new(width, height)

        for shape in self.layers:
            img = shape(width, height)
            image.pixels[img.mask] = img.pixels[img.mask]

        return image


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

    def __getattr__(self, key):

        try:
            return self._properties[key]
        except KeyError as e:
            raise AttributeError from e

    def __setattr__(self, key, value):

        if key in self.properties:
            self._properties[key] = value
            return

        super().__setattr__(key, value)

    def __call__(self, width=None, height=None, *, colorspace=None, **kwargs):

        # If the user provides a width and height they want us to draw the
        # shape as an image
        if width is not None and height is not None:
            return self._draw(width, height, colorspace)

        # Otherwise assume that they are using the shape as a function in
        # a composite shape.
        args = dict(self._properties)

        try:
            for p in self.parameters:
                args[p] = kwargs[p]

        except KeyError as e:
            raise TypeError(f"Missing required parameter: {p}") from e

        return self._mask(**args)

    @property
    def json(self):

        name = self.__class__.__name__
        color = self.color
        properties = [dict(name=k, value=v) for k, v in self._properties.items()]
        parameters = sorted([p for p in self.parameters])

        return json.dumps(
            dict(name=name, color=color, parameters=parameters, properties=properties)
        )

    def _draw(self, width, height, colorspace):

        if colorspace is None:
            colorspace = RGB8

        image = Image.new(
            width, height, background=self.background, colorspace=colorspace
        )

        mask = self.mask(width, height)
        fg_color = colorspace.parse(self.color)

        image[mask] = fg_color
        image.mask = mask

        return image

    def __add__(self, other):

        if isinstance(other, Shape):
            layers = [self, other]
            return Canvas(layers=layers)

        if isinstance(other, Canvas):
            other.layers.insert(0, self)
            return other

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


def check_fields(item, expected_fields):
    """Check a dictionary to ensure that it has the exepected fields."""

    for field in expected_fields:
        if field not in item:
            raise TypeError("Missing expected field: '{}'".format(field))


def _shape_fromjson(f):
    """This writes the definition of the fromjson method for shapes."""

    def fromjson(cls, fromjson):
        shape = json.loads(fromjson)
        check_fields(shape, ["name", "properties"])

        name = shape["name"]

        if name != cls.__name__:
            message = "Cannot parse shape '{}' as a '{}'"
            raise TypeError(message.format(name, cls.__name__))

        params = {}

        for prop in shape["properties"]:
            check_fields(prop, ["name", "value"])

            name = prop["name"]
            value = prop["value"]

            if name not in cls.properties:
                raise TypeError("Unexpected property: '{}'".format(name))

            params[name] = value

        return cls(**params)

    return fromjson


def _shape_parameters(f):
    """This exposes the parameters that are defined for a shape."""

    kw_only = inspect.Parameter.KEYWORD_ONLY
    params = inspect.signature(f).parameters

    params = set([name for name, param in params.items() if param.kind != kw_only])
    return params


def _shape_properties(f):
    """This exposes the properties that are defined for a shape."""

    kw_only = inspect.Parameter.KEYWORD_ONLY
    params = inspect.signature(f).parameters

    props = set([name for name, param in params.items() if param.kind == kw_only])
    return props


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
        "fromjson": classmethod(_shape_fromjson(f)),
        "parameters": _shape_parameters(f),
        "properties": _shape_properties(f),
    }

    return type(name, (Shape,), attributes)


def shape(f):
    """A decorator used to define a new shape."""
    return define_shape(f)


@shape
def Circle(x, y, *, x0=0, y0=0, r=0.8, pt=None):
    """A circle."""

    xc = x - x0
    yc = y - y0
    circle = np.sqrt(xc * xc + yc * yc)

    if pt is None:
        return circle < r * r

    R = (r + pt) ** 2
    r = (r - pt) ** 2

    return np.logical_and(r < circle, circle < R)


@shape
def Ellipse(x, y, *, x0=0, y0=0, a=2, b=1, r=0.8):
    """An ellipse."""

    xc = (x - x0) ** 2
    yc = (y - y0) ** 2

    a = a * a
    b = b * b

    return np.sqrt(xc / a + yc / b) < r * r


@shape
def Square(x, y, *, x0=0, y0=0, size=0.8):
    """A square."""

    xc = x - x0
    yc = y - y0

    size = size / 2

    return np.logical_and(np.abs(xc) < size, np.abs(yc) < size)
