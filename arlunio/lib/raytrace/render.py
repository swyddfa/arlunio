import logging

import arlunio as ar
import numpy as np
import PIL.Image as Image

from arlunio.lib.math import clamp

from .camera import SimpleCamera
from .data import Rays, ScatterPoint
from .material import Gradient, LambertianDiffuse


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
    width: int,
    height: int,
    *,
    background=None,
    color="lightgrey",
    camera=None,
    objects=None,
    bounces=8,
):
    """A simple clay renderer."""

    background = Gradient() if background is None else background
    camera = SimpleCamera() if camera is None else camera
    objects = [] if objects is None else objects

    rays = camera(width=width, height=height)
    scatter = ScatterPoint.new(rays)
    mat = LambertianDiffuse(color=color)
    color = background(scatter=scatter)

    depth = 1
    mask = np.full((scatter.hit.shape), True)

    while depth < bounces:

        for obj in objects:
            test = obj(rays=rays, t_min=0.001, t_max=scatter.t)
            scatter.merge(test)

        # If there were no hits, then there's nothing to do
        if not np.any(scatter.hit):
            break

        # Update the mask to reflect where we have intersections.
        mask[mask] = scatter.hit

        matcol, rays = mat(scatter=scatter[scatter.hit])
        color[mask] *= matcol

        # Increasee the bounce counter and run again
        depth += 1
        scatter = ScatterPoint.new(rays)

    return color


@ar.definition
def MaterialRenderer(
    width: int, height: int, *, objects=None, bounces=8, camera=None, background=None
):
    """A renderer capable of rendering materials."""

    logger = logging.getLogger(__name__)

    background = Gradient() if background is None else background
    camera = SimpleCamera() if camera is None else camera
    objects = [] if objects is None else objects

    rays = camera(width=width, height=height)
    scatter = ScatterPoint.new(rays)
    color = background(scatter=scatter)

    depth = 1
    mask = np.full((scatter.hit.shape), True)

    materials = [mat for _, mat in objects]

    logger.info("Starting render.")

    while depth < bounces:

        matmap = np.full((scatter.hit.shape), -1)

        logger.debug(" Depth: %i ".center(80, "-"), depth)
        logger.debug("Mask: %s", mask.shape)
        logger.debug("Material Map: %s", matmap.shape)
        logger.debug("%s", scatter)

        for idx, (obj, _) in enumerate(objects):
            logger.debug(" Obj: %i ".center(80, "-"), idx)
            test = obj(rays=rays, t_min=0.001, t_max=scatter.t)

            # Record which material should be used for these intersections.
            matmap[test.hit] = idx
            scatter.merge(test)

        if not np.any(scatter.hit):
            logger.debug("Nothing hit, stopping")
            break

        matids = np.unique(matmap[matmap != -1])
        logger.debug("-" * 80)
        logger.debug("Mat Ids: %s", matids)
        logger.debug("#hits: %s", scatter.hit[scatter.hit == True].shape)

        mask[mask] = scatter.hit
        origin = scatter.p[scatter.hit]
        directions = scatter.normal[scatter.hit]

        for idx in matids:
            logger.debug(" Mat: %i ".center(80, "-"), idx)
            mat = materials[idx]

            # Only select the intersections that correspond with this material
            mat_mask = matmap[scatter.hit] == idx

            scatter_mask = np.array(scatter.hit)
            scatter_mask[scatter.hit] = mat_mask

            color_mask = np.array(mask)
            color_mask[color_mask] = scatter_mask[scatter.hit]

            logger.debug("Mat Mask: %s", mat_mask.shape)
            logger.debug("Scatter Mask: %s", scatter_mask.shape)
            logger.debug("Color Mask: %s", color_mask.shape)

            mat_scatter = scatter[scatter_mask]
            logger.debug("Mat Scatter: %s", mat_scatter)

            matcol, matrays = mat(scatter=mat_scatter)
            color[color_mask] *= matcol

            origin[mat_mask] = matrays.origin
            directions[mat_mask] = matrays.direction

        depth += 1

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

    # Gamma correction...
    cols = np.sqrt(cols)

    r = clamp(cols[:, 0], 0, 0.99999) * 256
    g = clamp(cols[:, 1], 0, 0.99999) * 256
    b = clamp(cols[:, 2], 0, 0.99999) * 256

    color = np.array(np.dstack([r, g, b])[0], dtype=np.uint8)
    color = color.reshape(height, width, 3)

    return Image.fromarray(color, "RGB")
