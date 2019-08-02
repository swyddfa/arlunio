import inspect
import json
import logging
import typing

import attr

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


class Property:
    """Parent class for properties."""

    IS_PROPERTY = "stylo.isproperty"


@attr.s(auto_attribs=True)
class Shape:
    """Docstring template."""

    scale: float = attr.ib(default=1.0, repr=False)
    color: str = attr.ib(default="#000000", repr=False)
    origin: typing.Any = attr.ib(default=None, repr=False)
    background: typing.Any = attr.ib(default=None, repr=False)

    def __add__(self, other):

        if isinstance(other, Shape):
            layers = [self, other]
            return Canvas(layers=layers)

        if isinstance(other, Canvas):
            other.layers.insert(0, self)
            return other

    def __call__(self, width=None, height=None, *, colorspace=None, **kwargs):

        # If given a width and a height draw the shape as an image.
        if width is not None and height is not None:
            return self._draw(width, height, colorspace)

        try:
            w, h = width
            return self._draw(w, h, colorspace)
        except TypeError:
            pass

        # Otherwise assume that we are being called as part as another shape's
        # definition
        args = dict(self.properties)

        try:
            for param in self.parameters:
                args[param] = kwargs[param]

        except KeyError as e:
            raise TypeError(f"Missing parameter: {param}") from e

        return self._definition(**args)

    def _draw(self, width: int, height: int, colorspace):

        if colorspace is None:
            colorspace = RGB8

        image = Image.new(
            width, height, background=self.background, colorspace=colorspace
        )

        mask = self.mask(width, height)
        fg = colorspace.parse(self.color)

        image[mask] = fg
        image.mask = mask

        return image

    def mask(self, width: int, height: int):

        args = dict(self.properties)

        for param in self.parameters:
            parameter = getattr(Parameter, param)
            args[param] = parameter(width, height, self.scale)

        return self._definition(**args)

    @property
    def properties(self):
        fields = attr.fields(self.__class__)
        props = [p.name for p in fields if Property.IS_PROPERTY in p.metadata]

        return {p: getattr(self, p) for p in props}

    @property
    def json(self):
        """Return a json representation of the current shape instance."""

        d = dict(
            name=self.__class__.__name__,
            scale=self.scale,
            color=self.color,
            properties=[{"name": k, "value": v} for k, v in self.properties.items()],
        )
        return json.dumps(d)

    @classmethod
    def from_json(cls, json_str):
        """Create an instance of a shape from its json representation."""
        shape = json.loads(json_str)
        name, properties = get_fields(shape, "name", "properties")

        if name != cls.__name__:
            raise TypeError(f"Cannot parse shape '{name}' as a '{cls.__name__}'")

        params = {}
        allowed_properties = property_names(cls)

        for prop in shape["properties"]:
            name, value = get_fields(prop, "name", "value")

            if name not in allowed_properties:
                message = (
                    f"Cannot parse {cls.__name__} definition: "
                    f"unexpected property {name}"
                )
                raise TypeError(message)

            params[name] = value

        return cls(**params)


def property_names(cls: Shape) -> typing.List[str]:
    """Given a shape return a list of all property names."""
    fields = attr.fields(cls)
    props = [p.name for p in fields if Property.IS_PROPERTY in p.metadata]

    return props


def get_fields(item, *args):
    """Get the named field(s) from a dictionary.

    If any of the fields do not exist a :code:`TypeError` will be raised.
    """

    values = []

    for field in args:
        logger.debug(f"Checking field: {field}")

        if field not in item:
            raise TypeError("Missing expected field: '{}'".format(field))

        values.append(item[field])

    return values


def define_property(param: inspect.Parameter, attributes):
    """Given a function parameter representing a property define an appropriate
    attribute definition."""
    params = {"default": param.default, "kw_only": True}
    metadata = {Property.IS_PROPERTY: True}

    if param.annotation != inspect._empty:
        params["type"] = param.annotation
        params["validator"] = [attr.validators.instance_of(param.annotation)]

    params["metadata"] = metadata
    attributes[param.name] = attr.ib(**params)


def get_shape_parameters(f):
    """Given the user's function, sort the arguments into parameters and
    properties."""

    kw_only = inspect.Parameter.KEYWORD_ONLY
    parameters = inspect.signature(f).parameters

    props = [p for p in parameters.values() if p.kind == kw_only]
    params = [p for p in parameters.values() if p not in props]

    logger.debug("--> Parameters: {}".format(", ".join(p.name for p in params)))
    logger.debug("--> Properties: {}".format(", ".join(p.name for p in props)))

    return params, props


def shape(f) -> type:
    """Define a new shape."""

    name = f.__name__
    logger.debug(f"Defining shape: {name}")

    attributes = {"__doc__": inspect.getdoc(f), "_definition": staticmethod(f)}

    params, props = get_shape_parameters(f)
    attributes["parameters"] = set([p.name for p in params])

    for prop in props:
        logger.debug(f"--> {prop.name}")
        define_property(prop, attributes)

    return attr.s(type(name, (Shape,), attributes))
