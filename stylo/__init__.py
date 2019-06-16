from ._version import __version__  # noqa: F401
from .color import RGB8  # noqa: F401
from .image import Image  # noqa: F401
from .loaders import load_parameters, load_shapes
from .shapes import Canvas, shape  # noqa: F401

Parameter = load_parameters()  # noqa: F401
Shapes = load_shapes()  # noqa: F401
