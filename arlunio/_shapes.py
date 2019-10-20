import inspect
import json
import logging
import re

from typing import Any, Dict, List

import pkg_resources

import attr

from .color import RGB8
from .image import Image
from .loaders import load_parameters

Parameter = load_parameters()
logger = logging.getLogger(__name__)


class Canvas:
    """A good canvas is what every artist needs."""

    def __init__(self, layers=None, background=None):
        self.layers = layers

    def __repr__(self):
        return f"Canvas<{len(self.layers)} layers>"

    def __add__(self, other):

        if isinstance(other, Shape):
            layers = list(self.layers) + [other]
            return Canvas(layers=layers)

        if isinstance(other, Canvas):
            layers = list(self.layers) + list(other.layers)
            return Canvas(layers=layers)

        raise TypeError()

    def __call__(self, width, height):
        image = Image.new(width, height)

        for shape in self.layers:
            img = shape(width, height)
            image.pixels[img.mask] = img.pixels[img.mask]

        return image


class Property:
    """Parent class for properties."""

    IS_PROPERTY = "arlunio.isproperty"


@attr.s(auto_attribs=True)
class Shape:
    """This is the base class that all shapes inherit from and defines the interface
    that applies to all shapes.
    """

    scale: float = attr.ib(default=1.0, repr=False)
    """A property that can be set to control the overall size of the shape. Must be
    supported by the shape's parameters in order to take effect."""

    color: str = attr.ib(default="#000000", repr=False)
    """A property that controls the color of the shape when drawn, currently is
    specified as a color hex string. Default :code:`#000000`"""

    origin: Any = attr.ib(default=None, repr=False)
    """A property that can be used to control where the origin is in relation to the
    image. Must be supported by the shape's parameters in order to take effect
    *Currently not implemented.*
    """

    background: Any = attr.ib(default=None, repr=False)
    """A propety that can be used to set the background color of the image when the
    shape is drawn, currently is specified as a color hex string. Default
    :code:`#ffffff`
    """

    def __attrs_post_init__(self):
        self._logger = logger.getChild(self.__class__.__name__)

    def __add__(self, other):

        if isinstance(other, Shape):
            layers = [self, other]
            return Canvas(layers=layers)

        if isinstance(other, Canvas):
            layers = [self] + list(other.layers)
            return Canvas(layers=layers)

    def __call__(self, width=None, height=None, *, colorspace=None, **kwargs):
        self._logger.debug("Choosing draw method....")
        self._logger.debug(f"--> width: {width}, height: {height}")
        self._logger.debug(f"--> kwargs: {', '.join(kwargs.keys())}")

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
        self._logger.debug(f"Width and Height")

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
        self._logger.debug(f"Mask: {width}x{height}")

        args = dict(self.properties)
        self._logger.debug(f"Properties: {args}")

        for param in self.parameters:
            parameter = getattr(Parameter, param)
            p = parameter(width, height, self.scale)

            self._logger.debug(f"{param}: {p.shape}")
            args[param] = p

        self._logger.debug(f"Arguments: {', '.join(args.keys())}")
        return self._definition(**args)

    @property
    def properties(self):
        fields = attr.fields(self.__class__)
        props = [p.name for p in fields if Property.IS_PROPERTY in p.metadata]

        return {p: getattr(self, p) for p in props}

    @property
    def dict(self):
        """Return a dictionary representation of the current shape instance.

        For example the dictionary representation of a circle is::

           >>> import arlunio as ar
           >>> from pprint import pprint

           >>> circle = ar.S.Circle()
           >>> pprint(circle.dict)
           {'color': '#000000',
            'name': 'Circle',
            'properties': [{'name': 'x0', 'value': 0},
                           {'name': 'y0', 'value': 0},
                           {'name': 'r', 'value': 0.8},
                           {'name': 'pt', 'value': None}],
            'scale': 1.0}
        """

        dictionary = dict(
            name=self.__class__.__name__,
            scale=self.scale,
            color=self.color,
            properties=[{"name": k, "value": v} for k, v in self.properties.items()],
        )

        return dictionary

    @property
    def json(self):
        """Return a JSON representation of the current shape instance.

        For example the JSON representation of the circle is::

           >>> import arlunio as ar

           >>> circle = ar.S.Circle()
           >>> print(circle.json)
           {
             "name": "Circle",
             "scale": 1.0,
             "color": "#000000",
             "properties": [
               {
                 "name": "x0",
                 "value": 0
               },
               {
                 "name": "y0",
                 "value": 0
               },
               {
                 "name": "r",
                 "value": 0.8
               },
               {
                 "name": "pt",
                 "value": null
               }
             ]
           }

        """
        return json.dumps(self.dict, indent=2)

    @classmethod
    def from_json(cls, json_str):
        """Create an instance of a shape from its json representation.

        For example we can create an instance of the |Circle| shape as follows::

           >>> import arlunio as ar
        """
        dictionary = json.loads(json_str)
        return cls.from_dict(dictionary)

    @classmethod
    def from_dict(cls, dictionary):
        """Create an instance of a shape from its dictionary representaiton."""
        name, properties = get_fields(dictionary, "name", "properties")

        if name != cls.__name__:
            raise TypeError(f"Cannot parse shape '{name}' as a '{cls.__name__}'")

        params = {}
        allowed_properties = property_names(cls)

        for prop in dictionary["properties"]:
            name, value = get_fields(prop, "name", "value")

            if name not in allowed_properties:
                message = (
                    f"Cannot parse {cls.__name__} definition: "
                    f"unexpected property {name}"
                )
                raise TypeError(message)

            params[name] = value

        return cls(**params)


def property_names(cls: Shape) -> List[str]:
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
    """Decorator that is used to define new shapes.

    Shapes are functions that are called on every pixel in an image to determine
    if a given pixel is considered a part of the shape. Shape functions should
    return a boolean, :code:`True` if the pixel is a part of the shape and
    :code:`False` otherwise. The simplest possible shape definition would look
    like the following::

        >>> import arlunio as ar

        >>> @ar.shape
        ... def Everywhere():
        ...     return True

    This is a shape that exists "everywhere", if we were to create an image from
    this shape we would see that every pixel is colored in::

       >>> everywhere = Everywhere()
       >>> image = everywhere(width=2, height=2)
       >>> image.pixels
       array([[[0, 0, 0],
               [0, 0, 0]],
       <BLANKLINE>
              [[0, 0, 0],
               [0, 0, 0]]], dtype=uint8)

    However, while simple this shape is not particuarly interesting to look
    at. In order to do something more interesting shape functions typically
    accept one or more parameters. See the section on parameters for more
    information on what these are but typically they are a numpy array where
    each element is some value associated with a pixel in the image.

    As an example we will use the :code:`y` parameter which maps a value onto a
    pixel based on its vertical position in the image. Let's create a shape that
    colors in the lower half of the image::

        >>> @ar.shape
        ... def LowerHalf(y):
        ...     return y < 0

        >>> lower = LowerHalf()
        >>> image = lower(width=1, height=5)
        >>> image.pixels
        array([[[255, 255, 255]],
        <BLANKLINE>
               [[255, 255, 255]],
        <BLANKLINE>
               [[255, 255, 255]],
        <BLANKLINE>
               [[  0,   0,   0]],
        <BLANKLINE>
               [[  0,   0,   0]]], dtype=uint8)

    Finally you probably want your shape to be configurable in some way, for
    this we have properties. Properties are defined by declaring your shape
    function with keyword only arguments which will then become arugments you
    can pass to your shape's constructor. Let's tweak our :code:`LowerHalf`
    shape to take a :code:`height` property that we can use to control how much
    of the image we color in::

        >>> @ar.shape
        ... def FillHeight(y, *, height=0):
        ...     return y < height

    .. important::

       Properties *must* be defined as keyword only arguments i.e. arguments
       that come after the :code:`*` in the function definition

    Now we can control how much of the image we want filled in::

        >>> fill = FillHeight(height=0.5)
        >>> image = fill(width=1, height=5)
        >>> image.pixels
        array([[[255, 255, 255]],
        <BLANKLINE>
               [[255, 255, 255]],
        <BLANKLINE>
               [[  0,   0,   0]],
        <BLANKLINE>
               [[  0,   0,   0]],
        <BLANKLINE>
               [[  0,   0,   0]]], dtype=uint8)

    That just about covers the different features supported by the shape
    decorator. Be sure to check out some of the other documentation for more
    creative examples on how these features are used.

    """

    name = f.__name__
    logger.debug(f"Defining shape: {name}")

    attributes = {"__doc__": inspect.getdoc(f), "_definition": staticmethod(f)}

    params, props = get_shape_parameters(f)
    attributes["parameters"] = set([p.name for p in params])

    for prop in props:
        logger.debug(f"--> {prop.name}")
        define_property(prop, attributes)

    return attr.s(type(name, (Shape,), attributes))


class Key:
    """This class is used to represent x.y.z keys in a collection.

    It's only a thin wrapper around a tuple that should make the implementation of
    collections easier to reason about. A key can be created from a number of strings

    >>> from arlunio._shapes import Key
    >>> Key('a', 'b', 'c')
    k'a.b.c'

    Alternatively from a single string with each part delimited with a dot.

    >>> Key.fromstring('a.b.c')
    k'a.b.c'

    Keys have a length which is equal to the number of components that makes up the
    key.

    >>> k = Key('a', 'b', 'c')
    >>> len(k)
    3

    They can be checked to see if they are equal against other keys, or their string
    representation

    >>> k == Key.fromstring('a.b.c')
    True

    >>> k == "a.b.c"
    True

    Keys can be indexed

    >>> k[0]
    'a'

    But not mutated

    >>> k[1] = 'd'
    Traceback (most recent call last):
        ...
    TypeError: 'Key' object does not support item assignment
    """

    __slots__ = "_key"

    def __init__(self, *args):
        self._key = args

    def __repr__(self):
        return f"k'{str(self)}'"

    def __str__(self):
        return ".".join(self._key)

    def __hash__(self):
        return hash(self._key)

    def __eq__(self, other):

        if isinstance(other, Key):
            return self._key == other._key

        if isinstance(other, str):
            return str(self) == other

        return False

    def __len__(self):
        return len(self._key)

    def __getitem__(self, index):
        return self._key[index]

    def __add__(self, other):
        return Key.fromstring(str(self) + "." + str(other))

    @classmethod
    def fromstring(cls, string):
        return cls(*string.split("."))


@attr.s(auto_attribs=True)
class Collection:
    """A group of related items, indexed by keys."""

    _items: Dict[Key, Any] = attr.Factory(dict)

    def __str__(self):
        sep = "\n|  "
        name = self.__class__.__name__
        header = f"{name}: {len(self)} items{sep}"
        items = sep.join(str(k) for k in self._items.keys())

        return header + items

    def __len__(self):
        return len(self._items)

    def __getitem__(self, key):

        if isinstance(key, int):
            return list(self._items.values())[key]

        raise KeyError(key)

    def __getattr__(self, name):
        candidates = self.find(name)
        cls = self.__class__

        if len(candidates) == 0:
            items = {k: v for k, v in self._items.items() if k[0] == name}

            if len(items) == 0:
                raise AttributeError(f"No item with name: {name}")

            return cls(items=items)

        if len(candidates) == 1:
            return candidates[0]

        raise AttributeError(f"Ambiguous reference: {name}")

    def find(self, name: str):
        """Return a collection of all the items that have the given name."""

        items = {k: v for k, v in self._items.items() if k[-1] == name}
        return Collection(items=items)

    def merge(self, prefix: str, collection) -> None:
        """Given a collection and a prefix, merge its items into the collection."""

        prefix = Key.fromstring(prefix)

        for k, item in collection._items.items():
            self._items[prefix + k] = item


class ShapeCollection(Collection):
    """A class used to group related shapes together."""

    def shape(self, f):
        """Create a new shape within the collection."""

        shape_cls = shape(f)
        key = Key.fromstring(shape_cls.__name__)

        self._items[key] = shape_cls
        return shape_cls


def load_shapes():
    """Load all available shapes."""
    logger.debug("Loading shapes")

    pattern = re.compile(r"\Aarlunio[.]")
    library = Collection()

    for collection in pkg_resources.iter_entry_points("arlunio.shapes"):
        prefix = re.sub(pattern, "", f"{collection.module_name}.{collection.name}")
        logger.debug("Found collection: %s", prefix)

        library.merge(prefix, collection.load())

    return library
