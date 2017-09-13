import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I


class Motion:
    """
    **Note:** This class is not intended to be used directly.
    In order to implement a particular type of motion create
    a new class and inherit from this one.

    The way the motion simulation works is that you specify
    the initial position of the object (x0,y0) and the initial
    velocity of the object (vx0, vy0).

    Then given functions which describe the acceleration in both
    the x and y directions the simulation will integrate them
    up until the current time to get the velocities and positions
    at the current instance.

    Therefore since the intial conditions are all handled by this
    class, in order to implement a new type of motion, inherit from
    this class and override the `_acceleration_x` and
    `_acceleration_y` methods.

    Parameters
    ----------
    These are all the parameters that will be common to any
    motion simualtion:

    x0 : float
        The x coordinate of the starting position of the object.
        Changing this value will trigger the simulation.
        Default: 0
    y0 : float
        The y coordinate of the starting position of the object.
        Changing this value will trigger the simulation.
        Default: 1

    vx0 : float
        The initial x component of velocity of the object.
        Changing this value will trigger the simulation.
        Default: 1
    vy0 : float
        The intial y component of the velocity of the object.
        Changing this value will trigger the simulation.
        Default: 0

    t : int
        This is the time (in seconds) that the simulaion starts
        at. Changing this value will trigger the simulation.
        Default: 0s
    T : int
        This is the time (in seconds) that the simulation will
        finish at. Changing this value will trigger the simulation
        Default: 1s
    FPS: int
        This sets the resolution of the motion, it should match
        the value for the animation. Changing this value will trigger
        the simulation. Default: 25

    Attributes
    ----------
    These are all the attributes that are common to any motion
    simulation

    x : [float]
        This is a list of the x coordinates of the object at each time
        instance
    y : [float]
        This is a list of the y coordinates of the object at each time
        instance
    p : [(float, float)]
        A list of the x-y coordinate of the object at each time instance

    vx : [float]
        A list of the velocities in the x direction at each time
        instance
    vy : [float]
        A list of the velocities in the y direction at each time
        instance
    v : [(float, float)]
        A list of the velocity of the object at each time instance

    ax : [float]
        List of the acceleration in the x direction at each time
        instance
    ay : [float]
        List of the acceleration in the y direction at each time
        instance
    a : [(float, float)]
        List of the acceleration of the object at each time instance
    """

    def __init__(self, x0=0, y0=1, vx0=1, vy0=0, t=0, T=1, FPS=25):
        self._x0 = x0
        self._y0 = y0
        self._vx0 = vx0
        self._vy0 = vy0

        self._t = t
        self._T = T
        self._FPS = FPS

    def __repr__(self):
        s = f"x0:\t{self._x0}\n"
        s += f"y0:\t{self._y0}\n"
        s += f"vx0:\t{self._vx0}\n"
        s += f"vy0:\t{self._vy0}\n"
        s += "\n"
        s += f"t:\t{self._t}\n"
        s += f"T:\t{self._T}\n"
        s += f"FPS:\t{self._FPS}\n"

        return s

    def _velocity_x(self, t):
        return I.quad(lambda s: self._acceleration_x(s), self._t, t)[0]\
               + self._vx0

    def _velocity_y(self, t):
        return I.quad(lambda s: self._acceleration_y(s), self._t, t)[0]\
               + self._vy0

    def _position_x(self, t):
        return I.quad(lambda s: self._velocity_x(s), self._t, t)[0]\
               + self._x0

    def _position_y(self, t):
        return I.quad(lambda s: + self._velocity_y(s), self._t, t)[0]\
               + self._y0

    @property
    def x0(self):
        return self._x0

    @x0.setter
    def x0(self, value):
        self._x0 = value
        self._simulate()

    @property
    def y0(self):
        return self._y0

    @y0.setter
    def y0(self, value):
        self._y0 = value
        self._simulate()

    @property
    def vx0(self):
        return self._vx0

    @vx0.setter
    def vx0(self, value):
        self._vx0 = value
        self._simulate()

    @property
    def vy0(self):
        return self._vy0

    @vy0.setter
    def vy0(self, value):
        self._vy0 = value
        self._simulate()

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, value):

        if value < 0:
            raise ValueError('Start time cannot be negative!')

        if value >= self._T:
            raise ValueError('Start time cannot be later than end time!')

        self._t = value
        self._simulate()

    @property
    def T(self):
        return self._T

    @T.setter
    def T(self, value):

        if value <= 0:
            raise ValueError('End time must be positive!')

        if value <= self._t:
            raise ValueError('End time cannot be before start time!')

        self._T = value
        self._simulate()

    @property
    def FPS(self):
        return self._FPS

    @FPS.setter
    def FPS(self, value):

        if not isinstance(value, (int,)):
            raise ValueError('FPS must be an integer!')

        if value <= 0:
            raise ValueError('FPS must be positive!')

        self._FPS = value
        self._simulate()

    @property
    def x(self):
        return [x for (x, _, _, _, _, _) in self._data]

    @property
    def y(self):
        return [y for (_, y, _, _, _, _) in self._data]

    @property
    def p(self):
        return list(zip(self.x, self.y))

    @property
    def vx(self):
        return [vx for (_, _, vx, _, _, _) in self._data]

    @property
    def vy(self):
        return [vy for (_, _, _, vy, _, _) in self._data]

    @property
    def v(self):
        return list(zip(self.vx, self.vy))

    @property
    def ax(self):
        return [ax for (_, _, _, _, ax, _) in self._data]

    @property
    def ay(self):
        return [ay for (_, _, _, _, _, ay) in self._data]

    @property
    def a(self):
        return list(zip(self.ax, self.ay))

    def _acceleration_x(self, t):
        return 0

    def _acceleration_y(self, t):
        return 0

    def _simulate(self):

        self._data = []
        frames = np.linspace(self._t, self._T, (self._T - self._t) * self._FPS)

        for t in frames:

            # Compute the _accelerations
            ax = self._acceleration_x(t)
            ay = self._acceleration_y(t)

            # Compute the velocities
            vx = self._velocity_x(t)
            vy = self._velocity_y(t)

            # Compute the positions
            x = self._position_x(t)
            y = self._position_y(t)

            self._data.append((x, y, vx, vy, ax, ay))

    def show(self, vel=False, acc=False):

        if vel or acc:
            fig, (pos, velacc) = plt.subplots(1, 2, figsize=(12, 4))
        else:
            fig, pos = plt.subplots(1)

        pos.plot(self.x, self.y, label='position')
        pos.set_xlabel(r'$x$')
        pos.set_ylabel(r'$y$')
        pos.legend(loc=0)

        if vel:
            velacc.plot(self.vx, label=r'$v_x$')
            velacc.plot(self.vy, label=r'$v_y$')

        if acc:
            velacc.plot(self.ax, label=r'$a_x$')
            velacc.plot(self.ay, label=r'$a_y$')

        if vel or acc:
            velacc.set_xlabel(r'$t$')
            velacc.legend(loc=0)


class Projectile(Motion):
    """
    This implements a very basic notion of projectile motion.
    We assume the following:
      - The object experiences no drag
      - The object has acceleration given by the constant g
    """

    def __init__(self, g=-9.8, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._g = g
        self._simulate()

    def __repr__(self):
        s = "Projectile Motion\n"
        s += "-----------------\n"
        s += f"g:\t{self._g}\n"
        s += '\n'
        s += super().__repr__()

        return s

    def _acceleration_y(self, t):
        return self.g

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, value):
        self._g = value
        self._simulate()
