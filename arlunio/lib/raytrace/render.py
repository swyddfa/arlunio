import logging

import arlunio as ar
import numpy as np
import numpy.random as npr
import PIL.Image as Image

from arlunio.lib.math import clamp, normalise

from .camera import SimpleCamera
from .data import Rays, ScatterPoint
from .material import Gradient, NormalMap

logger = logging.getLogger(__name__)


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
def ZDepthRenderer(width: int, height: int, *, camera=None, objects=None):
    """A renderer that returns a z-depth pass."""

    camera = SimpleCamera() if camera is None else camera
    objects = [] if objects is None else objects

    rays = camera(width=width, height=height)
    scatter = ScatterPoint.new(rays)

    for obj in objects:
        test = obj(rays=rays, t_min=0, t_max=scatter.t)
        scatter.merge(test)

    depth = np.abs(scatter.p[:, 2] - camera.origin[2])
    depth[scatter.t == ScatterPoint.MAX_FLOAT] = np.max(depth)

    vs = np.array((depth / np.max(depth)) * 255, dtype=np.uint8)
    vs = vs.reshape(height, width)

    return Image.fromarray(vs, "L")


@ar.definition
def ClayRenderer(
    width: int, height: int, *, background=None, camera=None, objects=None, bounces=8,
):
    """A simple clay renderer."""

    background = Gradient() if background is None else background
    camera = SimpleCamera() if camera is None else camera
    objects = [] if objects is None else objects

    rays = camera(width=width, height=height)
    scatter = ScatterPoint.new(rays)
    color = background(scatter=scatter)

    depth = 1
    mask = np.full((scatter.hit.shape), True)

    while depth < bounces:

        print(".", end="")
        for obj in objects:
            test = obj(rays=rays, t_min=0, t_max=scatter.t)
            scatter.merge(test)

        # If there were no hits, then there's nothing to do
        if not np.any(scatter.hit):
            break

        # Update the mask to reflect where we have intersections.
        mask[mask] = scatter.hit
        color[mask] *= 0.5
        n = mask[mask].shape[0]

        # Increasee the bounce counter and run again
        depth += 1

        origin = scatter.p[scatter.hit]
        directions = scatter.normal[scatter.hit] + normalise(npr.rand(n, 3))

        rays = Rays(origin, directions)
        scatter = ScatterPoint.new(rays)

    return color


@ar.definition
def SampledRenderer(width: int, height: int, *, kernel=None, samples=10):
    """A renderer is responsible for orchestrating the entire process."""

    if kernel is None:
        raise ValueError("Missing renderer kernel")

    s = samples
    n = width * height
    scale = 1.0 / s

    cols = np.zeros((n, 3))
    for _ in range(s):
        cols += kernel(width=width, height=height) * scale
        print("+")

    r = clamp(cols[:, 0], 0, 0.99999) * 256
    g = clamp(cols[:, 1], 0, 0.99999) * 256
    b = clamp(cols[:, 2], 0, 0.99999) * 256

    color = np.array(np.dstack([r, g, b])[0], dtype=np.uint8)
    color = color.reshape(height, width, 3)

    return Image.fromarray(color, "RGB")
