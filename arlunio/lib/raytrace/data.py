from typing import ClassVar

import attr
import numpy as np

from arlunio.lib.math import normalise


@attr.s(auto_attribs=True, repr=False)
class Rays:
    """A collection of rays"""

    origin: np.ndarray
    """The point where the rays originate from."""

    direction: np.ndarray
    """An array of vectors indicating which direction each ray is pointing"""

    def __repr__(self):
        return f"Rays(origin={self.origin.shape}, direction={self.direction.shape})"

    def __getitem__(self, key):
        return Rays(self.origin[key], self.direction[key])

    def at(self, t):
        """Get the position for each value of t."""
        return self.origin + t[:, np.newaxis] * self.direction


@attr.s(auto_attribs=True, repr=False)
class ScatterPoint:
    """A scatter point is where rays have intersected an object and where various
    calculations should take place."""

    MAX_FLOAT: ClassVar[float] = np.finfo(np.float64).max

    hit: np.ndarray
    """A boolean array with shape :code:`(n,)` indicating which rays have intersected
    some object."""

    t: np.ndarray
    """A scalar array with shape :code:`(n,)` indicating the value of the parameter
    :code:`t` at the point of intersection."""

    p: np.ndarray
    """An array of vectors with shape :code:`(n, 3)` indicating the point of
    intersection in space."""

    normal: np.ndarray
    """An array of vectors with shape :code:`(n, 3)` indicating the direction of the
    surface normal at the point of intersection."""

    front_face: np.ndarray
    """A boolean array with shape :code:`(n, 3)` indicating which side of the surface
    the incoming ray was on."""

    def __repr__(self):

        props = {
            "hit": self.hit.shape,
            "t": self.t.shape,
            "p": self.p.shape,
            "normal": self.normal.shape,
            "front_face": self.front_face.shape,
        }

        args = ", ".join([f"{k}={v}" for k, v in props.items()])
        return f"ScatterPoint({args})"

    def __getitem__(self, key):

        hit = self.hit[key]
        t = self.t[key]
        p = self.p[key]
        normal = self.normal[key]
        front_face = self.front_face[key]

        return ScatterPoint(hit, t, p, normal, front_face)

    def merge(self, other):
        """Merge the results of another scatter point in with this one."""

        self.hit = np.logical_or(self.hit, other.hit)

        self.t[other.hit] = other.t
        self.p[other.hit] = other.p
        self.normal[other.hit] = other.normal
        self.front_face[other.hit] = other.front_face

    @classmethod
    def new(cls, rays: Rays):
        """Create a new scatter point based on an initial cluster of rays."""

        n, _ = rays.direction.shape

        true = np.full((n,), True)
        false = np.full((n,), False)
        maxf = np.full((n,), cls.MAX_FLOAT)

        params = {
            "hit": false,
            "t": maxf,
            "p": rays.direction,
            "normal": normalise(rays.direction),
            "front_face": true,
        }

        return cls(**params)
