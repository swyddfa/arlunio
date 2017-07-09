from math import floor

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I


class Driver:
    """
    A Driver is typically used to control a certain parameter over time
    for example - the thickness of a line etc.

    In certain respects it's very similar to a Motion object but I think
    it's different enough to warrant its own class

    Attrbiutes
    ----------

    name : string, optional
        The name associated with a particular driver
        Default: ''
    keyframes: [(int/float, float)], optional
        These represent the desired values and times at which they should
        be attained. Time can either be given by the frame number (int) or
        the 'real time' measured in seconds (float). If you wish to specify
        a whole unit of time e.g. 5s it **must** be written as 5.0, otherwise
        it will be interpreted as the frame number 5.
        Default: [(0.0, 0), (1.0, 1)]
    cycle : bool, optional
        If True, any requests for indicies outside the range of the data,
        will be mapped back into it - effectively looping the data.
        Default: False
    FPS : int, optional
        Represents the number of frames and hence data points in each
        second. Default: 25
    """

    def __init__(self, name=None, keyframes=None, cycle=False, FPS=25):
        self._FPS = FPS
        self._cycle = cycle
        self._name = '' if name is None else name

        if keyframes is None:
            self._keys = [(0.0, 0), (1.0, 1)]
        else:
            self._keys = keyframes

        self._calculate()

    def __repr__(self):
        s = "Driver: %s\n\nKeyframes:\n" % self._name

        for key in self._sorted_keys():
            s += "\t%i\t%.2f\t%.2fs\n" %\
                             (key[0], key[1], key[0] / self._FPS)

        s += "\nFPS: %i" % (self._FPS)

        return s

    def _get_single(self, idx):
        """
        This provides the logic for getting a single value
        at a point in time. There are two possible behaviors
        depending on the value of the cycle property.

        If the index is within the length of the _data array
        then this behaves as expected and returns the value at
        that index.

        If however the index is out of bounds of the array then:
            - If cycle is not set and the index is larger than the
              length of the array, then the final value is returned
            - If cycle is not set and the index is less than 0,
              then the first value is returned
            - If cycles is set then the value of index is shifted
              until it lies within the array and that value is retured.
              This effectively extends the array indefinitely. Useful
              for cyclical motion, e.g. a pendulum.
        """
        length = len(self._data)

        # Possibly a bad idea, but we will override the default ability
        # to access from the end of an array by using negative indices
        if idx < 0:
            if not self._cycle:
                return self._data[0]
            else:
                return self._get_single(idx % length)

        # If the index is not negative, just try using it normally
        try:
            return self._data[idx]
        except IndexError:

            # Deal with the consequences of being outside the range
            if not self._cycle:
                return self._data[-1]
            else:
                return self._get_single(idx % length)

    def _get_slice(self, key):
        """
        This implements the ability to get a slice of the
        interpolation data.

        Again depending on if cycle is set we get different
        behavior:
            - If the slice is within the bounds of the array, then
              this behaves as expected.
            - If the slice extends outside of either end of the array
              then:
              + If cycle is set, relevant copies of the values are
                repeated
              + If cycle is not set, the final/first value is repeated
                forever.
        """
        # First unpack the slice to know where we want to slice to and
        # from
        return self._data[key]

    def __getitem__(self, key):
        if isinstance(key, (int,)):
            return self._get_single(key)

        if isinstance(key, (float,)):
            idx = floor(key * self._FPS)
            return self._get_single(idx)

        if isinstance(key, (slice,)):
            return self._get_slice(key)

    def _sorted_keys(self):

        def convert_key(key):
            time, *rest = key

            if isinstance(time, (float,)):
                time = floor(time * self._FPS)

            return tuple([time, *rest])

        return sorted([convert_key(key) for key in self._keys],
                      key=lambda i: i[0])

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):

        if not isinstance(value, (str,)):
            raise TypeError('Name must be a string!')

        self._name = value

    @property
    def frames(self):
        return self._data

    @property
    def keyframes(self):
        return self._keys

    @property
    def cycle(self):
        return self._cycle

    @cycle.setter
    def cycle(self, value):

        if not isinstance(value, (bool,)):
            raise TypeError('Cycle property must be a boolean!')

        self._cycle = value

    @property
    def FPS(self):
        return self._FPS

    @FPS.setter
    def FPS(self, value):

        if not isinstance(value, (int,)):
            raise TypeError('FPS must be an integer!')

        if value <= 0:
            raise ValueError('FPS must be a positive integer!')

        self._FPS = value
        self._calculate()

    def _calculate(self):
        """
        This is the method responsible for doing all the
        interpolation.
        """

        keys = self._sorted_keys()

        # Loop through and interpolate
        self._data = np.array([])

        for idx, key in enumerate(keys[:-1]):
            nextkey = keys[idx + 1]
            newvalues = np.linspace(key[1], nextkey[1],
                                    (nextkey[0] - key[0]))

            if len(newvalues) == 1:
                self._data = np.append(self._data, newvalues)
            else:
                self._data = np.append(self._data, newvalues)[:-1]

        self._data = np.append(self._data, np.array([keys[-1][1]]))

    def show(self):

        fig, ax = plt.subplots(1)
        ax.plot(self._data)
        ax.set_xlabel('Time (in frames)')
        ax.set_ylabel('Value')


def driver(cycle=False, FPS=25):
    """
    This is a decorator which streamlines the process of creating a driver.
    Simply define a function with the times and values you want and the
    decorator does the rest using Python kung-fu!
    """
    def wrapper(f):
        keys = f()

        if keys is None:
            constants = f.__code__.co_consts
            keys = list(filter(lambda i: isinstance(i, (tuple,)), constants))

        return Driver(name=f.__name__, keyframes=keys, cycle=cycle, FPS=FPS)

    return wrapper


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
