import arlunio as ar
import numpy as np
import numpy.random as npr

from arlunio.lib.color import getcolorf

from .data import Rays, ScatterPoint


def random_unit_sphere(n):
    a = npr.rand(n) * 2 * np.pi
    z = (npr.rand(n) * 2) - 1
    r = np.sqrt(1 - (z * z))

    return np.dstack([r * np.cos(a), r * np.sin(a), z])[0]


@ar.definition
def Gradient(scatter: ScatterPoint, *, color1=None, color2=None):
    """A basic gradient color."""

    color1 = np.array([1.0, 1.0, 1.0]) if color1 is None else color1
    color2 = np.array([0.5, 0.7, 1.0]) if color2 is None else color2

    t = 0.5 * (scatter.normal[:, 1]) + 1

    start = np.einsum("n,np->np", (1 - t), color1.reshape(1, 3))
    stop = np.einsum("n,np->np", t, color2.reshape(1, 3))

    return start + stop


@ar.definition
def NormalMap(scatter: ScatterPoint):
    """Visualise the normals on a given surface."""

    r = scatter.normal[:, 0] + 1
    g = scatter.normal[:, 1] + 1
    b = scatter.normal[:, 2] + 1

    return 0.5 * np.dstack([r, g, b])[0]


@ar.definition
def LambertianDiffuse(scatter: ScatterPoint, *, color="lightgrey"):
    """Lambertian diffuse material."""

    color = getcolorf(color)
    n = scatter.p.shape[0]

    origin = scatter.p
    directions = scatter.normal + random_unit_sphere(n)

    return (color, Rays(origin, directions))
