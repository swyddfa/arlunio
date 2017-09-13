import numpy as np
import matplotlib.pyplot as plt


class Sampler:

    def __init__(self, f=None, num_points=25, name=None):

        if f is not None and not callable(f):
            raise TypeError('f must be a function!')

        self._f = f
        self._num_points = num_points
        self._name = name
        self._sample()

    def __getitem__(self, index):
        return self._data[index]

    def __call__(self, x):

        # Default lambda x: x
        if self._f is None:
            return x
        else:
            return self._f(x)

    def __repr__(self):
        s = '%s\n' % self.name
        s += 'Num Points: %s' % self.num_points
        return s

    def __len__(self):
        return len(self._data)

    def _sample(self):
        points = np.linspace(0, 1, self._num_points)

        if self._f is None:
            self._data = points
        else:
            self._data = np.array([self._f(t) for t in points])

    @property
    def f(self):
        if self._f is None:
            return lambda t: t
        else:
            return self._f

    @f.setter
    def f(self, value):

        if not callable(value):
            raise TypeError('f must be a function!')

        self._f = value
        self._sample()

    @property
    def num_points(self):
        return self._num_points

    @num_points.setter
    def num_points(self, value):

        if not isinstance(value, (int,)):
            raise TypeError('num_points must be an integer!')

        if value < 2:
            raise ValueError('num_points must be larger than 2!')

        self._num_points = value
        self._sample()

    @property
    def name(self):

        if self._name is None:
            return 'Sampled function:'
        else:
            return self._name

    @name.setter
    def name(self, value):

        if not isinstance(value, (str,)):
            raise TypeError('property name must be a string!')

        self._name = value

    def show(self):
        """
        Returns a matplotlib figure of both the function and the sampled points
        """
        points = np.linspace(0, 1, self._num_points)
        interval = np.linspace(0, 1, 512)
        fs = [self._f(x) for x in interval]

        plt.plot(interval, fs, 'k')
        return plt.scatter(points, self._data, c='k')


def sampled(num_points=25):

    def sampler(f):

        name = f.__name__

        return Sampler(f, num_points=num_points, name=name)

    return sampler


def linear(x0, x1, num_points=25):
    """
    Linearly interpolate between x0 and x1 between times 0 and 1
    """
    def f(t):
        return (1 - t)*x0 + t*x1

    name = 'Linear Interpolation\nFrom:\t%s\nTo:\t%s\n' % (str(x0), str(x1))

    return Sampler(f, num_points=num_points, name=name)


def quadratic_ease_in(x0, x1, a=1):
    """
    Quadratic interpolation between x0 and x1
    which eases in. tuning parameter a gives control over
    the trajectory of the interpolation
    """

    # Make sure that the parameter is always positive
    a = abs(a)

    def f(t):
        return a*t**2 + t*(x1 - x0 - a) + x0

    return Sampler(f)


def quadratic_ease_out(x0, x1, a=-1):
    """
    Quadratic interpolation between x0 and x1
    which eases out tuning parameter a gives control over
    the trajectory of the interpolation
    """

    # Make sure that the parameter is always negative
    a = -abs(a)

    def f(t):
        return a*t**2 + t*(x1 - x0 - a) + x0

    return Sampler(f)
