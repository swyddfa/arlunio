import logging

import arlunio as ar
import numpy as np

from arlunio.lib.mask import all_
from arlunio.lib.math import dot, normalise

from .data import Rays, ScatterPoint


@ar.definition
def Sphere(
    rays: Rays, t_min: float, t_max: float, *, center=None, radius=0.5
) -> ScatterPoint:
    """A sphere."""

    logger = logging.getLogger(__name__)

    center = np.array([0, 0, -1]) if center is None else center

    oc = rays.origin - center

    a = dot(rays.direction, rays.direction)
    b = dot(oc, rays.direction)
    c = dot(oc, oc) - radius * radius

    logger.debug("a: %s, b: %s, c: %s", a.shape, b.shape, c.shape)

    # Determine which rays intersect
    disc = b * b - a * c
    hits = disc > 0

    logger.debug(
        "disc: %s, hits: %s, #hits: %s",
        disc.shape,
        hits.shape,
        hits[hits == True].shape,
    )

    a, b, root = a[hits], b[hits], np.sqrt(disc[hits])

    # Determine the smallest value of t for those intersections
    t1 = (-b - root) / a
    t2 = (-b + root) / a

    # Assume t1 is the correct value to choose
    t = t1

    # But where t1 < t_min, replace it with t2 if applicable
    mask = all_(t1 < t_min, t2 > t_min)
    t[mask] = t2[mask]

    # Now apply the bounds to t to get the actucal hits
    mask = all_(t > t_min, t < t_max[hits])
    hits[hits] = mask
    t = t[mask]

    # Determine the points of intersection and surface normals at t
    p = rays[hits].at(t)
    normals = normalise(p - center)

    # Finally determine which rays are hitting the outside surface of the sphere
    front_face = dot(rays.direction[hits], normals) < 0
    normals[front_face != True] = -normals[front_face != True]

    return ScatterPoint(hits, t, p, normals, front_face)
