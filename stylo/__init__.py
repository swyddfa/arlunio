from ._shapes import Canvas, Shape, shape  # noqa: F401
from ._version import __version__  # noqa: F401
from .color import RGB8  # noqa: F401
from .image import Image  # noqa: F401
from .loaders import load_parameters, load_shapes

Parameter = load_parameters()  # noqa: F401
Shapes = load_shapes()  # noqa: F401

HD = (1280, 720)  # noqa: F401
FHD = (1920, 1080)  # noqa: F401
QHD = (2560, 1440)  # noqa: F401
