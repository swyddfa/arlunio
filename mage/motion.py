from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt


class Projectile:
    """
    An object responsible for modelling the motion of a
    particle using the "A-Level" model of projectiles.
    i.e. the SUVAT equations
    """

    def __init__(self, x0, y0, ux, uy, t=0, T=5, a=-9.8, fps=25):
        """
        Parameters
        ----------
        x0 : float
            The initial x coordinate of the particle
        y0 : float
            The initial y coordinate of the particle
        ux : float
            The initial velocity in the x-direction
        uy : float
            The initial velocity in the y-direction
        t : int, optional
            The start time of the simulation (in seconds)
            Default: 0s
        T : int, optional
            The length of time to simulate the motion
            (in seconds). Default: 5s
        a : float, optional
            The acceleration due to gravity (in
            meters per second). Default: -9.8m/s
        fps : int, optional
            The number of frames in each second of motion
            Default: 25
        """
        self._x0 = x0
        self._y0 = y0
        self._ux = ux
        self._uy = uy
        self._t = t
        self._T = T
        self._a = a
        self._fps = fps

        self.simulate()

    def __repr__(self):
        s = "Projectile Motion:\n"
        s += "    x0:\t%.2fm\n" % self._x0
        s += "    y0:\t%.2fm\n" % self._y0
        s += "    ux:\t%.2fm/s\n" % self._ux
        s += "    uy:\t%.2fm/s\n" % self._uy
        s += "     T:\t%is\n" % self._T
        s += "     a:\t%.2fm/s\n" % self._a
        s += "\n"
        s += "FPS: %i" % self._fps
        return s

    def __getitem__(self, index):
        return self._data[index]

    def _sx(self, t):
        return self._x0 + t*self._ux

    def _sy(self, t):
        return self._y0 + t*self._uy + t**2*self._a/2

    def _vx(self, t):
        return self._ux

    def _vy(self, t):
        return self._uy + t*self._a

    @property
    def x0(self):
        return self._x0

    @x0.setter
    def x0(self, value):
        self._x0 = value
        self.simulate()

    @property
    def y0(self):
        return self._y0

    @y0.setter
    def y0(self, value):
        self._y0 = value
        self.simulate()

    @property
    def ux(self):
        return self._ux

    @ux.setter
    def ux(self, value):
        self._ux = value
        self.simulate()

    @property
    def uy(self):
        return self._uy

    @uy.setter
    def uy(self, value):
        self._uy = value
        self.simulate()

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, value):

        if value <= 0:
            raise ValueError("Start time must be positive!")

        if value >= self._T:
            raise ValueError('Start time cannot be after end time!')

        self._t = value
        self.simulate()

    @property
    def T(self):
        return self._T

    @T.setter
    def T(self, value):

        if value <= 0:
            raise ValueError("End time must be positive!")

        self._T = value
        self.simulate()

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        self._a = value
        self.simulate()

    @property
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, value):

        if not isinstance(value, (int,)) or value <= 0:
            raise ValueError("FPS must be a positive integer!")

        self._fps = value
        self.simulate()

    @property
    def xs(self):
        return [sx for (sx, _, _, _) in self._data]

    @property
    def ys(self):
        return [sy for (_, sy, _, _) in self._data]

    @property
    def vx(self):
        return [vx for (_, _, vx, _) in self._data]

    @property
    def vy(self):
        return [vy for (_, _, _, vy) in self._data]

    def show(self):
        return plt.plot(self.xs, self.ys)

    def simulate(self):

        frames = np.linspace(self._t, self._T, self._T*self._fps)
        self._data = []

        for t in frames:
            vx, vy = self._vx(t), self._vy(t)
            sx, sy = self._sx(t), self._sy(t)
            self._data.append((sx, sy, vx, vy))
