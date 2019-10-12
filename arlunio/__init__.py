from ._expressions import all, any, invert  # noqa: F401
from ._shapes import Canvas, Shape, ShapeCollection, load_shapes, shape  # noqa: F401
from ._version import __version__  # noqa: F401
from .color import RGB8  # noqa: F401
from .image import Image, Resolutions  # noqa: F401
from .loaders import load_parameters

Parameters = load_parameters()  # noqa: F401
Shapes = load_shapes()  # noqa: F401

# Define some aliases
S = Shapes  # noqa: F401
R = Resolutions  # noqa: F401
