import arlunio as ar
import numpy as np
import numpy.random as npr

from .data import Rays


@ar.definition
def SimpleSampler(width: int, height: int):
    """The simplest sampler."""

    u = np.full((height, width), np.linspace(0, 1, width))

    v = np.linspace(1, 0, height).reshape(1, height).transpose()
    v = np.full((height, width), v)

    return np.dstack([u, v]).reshape(width * height, 2)


@ar.definition
def UniformSampler(width: int, height: int):
    """Generate samples according to the uniform distribution"""

    n = width * height
    u = np.full((height, width), np.linspace(0, 1, width))

    v = np.linspace(1, 0, height).reshape(1, height).transpose()
    v = np.full((height, width), v)

    uv = np.dstack([u, v]).reshape(n, 2)
    uv[:, 0] += npr.rand(n) / width
    uv[:, 1] += npr.rand(n) / height

    return uv


@ar.definition
def SimpleCamera(
    width: int,
    height: int,
    *,
    origin=np.array([0.0, 0.0, 0.0]),
    scale=2.0,
    focal_length=1.0,
    sampler=None
) -> Rays:
    """A simple camera that generates rays to be cast into the scene.

    Attributes
    ----------
    focal_length:
        Something something focal length
    origin:
        Set the position of the camera in space. If not set this will default to
        :math:`(0, 0, 0)`
    sampler:
        The sampler the camera should use in order to generate rays. If not set this
        will default to the |UniformSampler|
    scale:
        Something something scale.
    """

    # Pick sensible defaults if some attributes are not set
    origin = np.array(origin)
    sampler = UniformSampler() if sampler is None else sampler

    ratio = width / height

    # Not entirely sure how to describe the effect these have on the final image...
    horizontal = np.array([scale * ratio, 0.0, 0.0])
    vertical = np.array([0.0, scale, 0.0])

    uv = sampler(width=width, height=height)
    lower_left = (
        origin - (horizontal / 2) - (vertical / 2) - np.array([0, 0, focal_length])
    )

    n = uv.shape[0]

    hs = np.einsum("n,np->np", uv[:, 0], horizontal.reshape(1, 3))
    vs = np.einsum("n,np->np", uv[:, 1], vertical.reshape(1, 3))
    ll = np.full((n, 3), lower_left)

    origin = np.full((n, 3), origin)
    directions = ll + hs + vs

    return Rays(origin, directions)
