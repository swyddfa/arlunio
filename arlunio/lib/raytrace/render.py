import arlunio as ar
import numpy as np
import PIL.Image as Image

from arlunio.lib.math import clamp

from .camera import SimpleCamera
from .data import ScatterPoint
from .material import Gradient, NormalMap


@ar.definition
def SimpleWorld(width: int, height: int, *, background=None, camera=None, objects=None):
    """A world is responsible for bringing everything together in order to render a
    single sample of the scene."""

    camera = SimpleCamera() if camera is None else camera
    background = Gradient() if background is None else background
    objects = [] if objects is None else objects

    rays = camera(width=width, height=height)
    scatter = ScatterPoint.new(rays)
    color = background(scatter=scatter)

    for obj, _ in objects:
        test = obj(rays=rays, t_min=0, t_max=scatter.t)
        scatter.merge(test)

    mat = NormalMap()
    color[scatter.hit] = mat(scatter=scatter)[scatter.hit]

    return color


@ar.definition
def SimpleRenderer(width: int, height: int, *, world=None, samples=10):
    """A renderer is responsible for orchestrating the entire process."""

    if world is None:
        raise ValueError("Missing world definition")

    s = samples
    n = width * height
    scale = 1.0 / s

    cols = np.zeros((n, 3))
    for _ in range(s):
        cols += world(width=width, height=height) * scale

    r = clamp(cols[:, 0], 0, 0.99999) * 256
    g = clamp(cols[:, 1], 0, 0.99999) * 256
    b = clamp(cols[:, 2], 0, 0.99999) * 256

    color = np.array(np.dstack([r, g, b])[0], dtype=np.uint8)
    color = color.reshape(height, width, 3)

    return Image.fromarray(color, "RGB")
