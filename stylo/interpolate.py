import numpy as np
import matplotlib.pyplot as plt

from itertools import cycle


class Channel:
    """
    A Channel is a single 'track' of Sampler objects and the
    like and is resonsible for all time conversions etc. everything
    it takes to construct, index and manage all the data for a single
    animation track.
    """

    def __init__(self, segments=[], FPS=25, name='', cycle=False):
        self._segments = segments
        self._FPS = FPS
        self._name = name
        self._cycle = cycle
        self._data = []

        self._construct()

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        # Although it is enough to define __getitem__ to make an object
        # iterable we have extended it to essentially make this object
        # infinitely iterable. This means any for loop will never terminate
        # so we have to define __iter__ to return the actual data we have so
        # we hopefully avoid that problem
        return iter(self._data)

    def _gen_fake_data(self, index):

        if isinstance(index, (int,)):
            return 0.0

        if isinstance(index, (slice,)):
            return np.array([0.0 for _ in range(index.start, index.stop)])

    def _get_single(self, index):

        if self._cycle:
            return self._data[index % len(self._data)]

        if index > len(self._data) - 1:
            return self._data[-1]

        if index < 0:
            return self._data[0]

        return self._data[index]

    def _get_slice(self, index):

        # Unpack the slice
        start = 0 if index.start is None else index.start
        stop = len(self._data) if index.stop is None else index.stop
        data_length = len(self._data)

        # Some conditions
        must_extend = stop > data_length
        must_prepend = start < 0

        # Handle the simplest case
        if not must_prepend and not must_extend:
            return self._data[index]

        # Oh dear, looks like we need to do some fancy stuff...
        # To start with we will extract the inner region of the
        # data and then decide on which directions it might need
        # extending
        inner_start = max(0, start)
        inner_end = min(stop, data_length)
        inner_data = self._data[slice(inner_start, inner_end)]

        # Assume we don't need to extend anything
        extension = []
        prepension = []

        # Do we have to extend it?
        if must_extend:
            # By how much?
            length = stop - inner_end

            # With what?
            if self._cycle:

                data = cycle(self._data)
                extension = [next(data) for _ in range(length)]

            else:
                extension = [self._data[-1] for _ in range(length)]

        # Do we have to prepend it?
        if must_prepend:
            # By how much?
            length = abs(start)

            # With what?
            if self._cycle:

                data = cycle(reversed(self._data))
                prepension = list(reversed([next(data) for _ in range(length)]))

            else:
                prepension = [self._data[0] for _ in range(length)]

        # Finally return the 'new data'
        return np.append(np.append(prepension, inner_data), extension)

    def __getitem__(self, index):

        if not isinstance(index, (int, slice)):
            raise TypeError('indices must be an integer or slices!')

        if self._segments == []:
            return self._gen_fake_data(index)

        if isinstance(index, (int,)):
            return self._get_single(index)

        if isinstance(index, (slice,)):
            return self._get_slice(index)

    @property
    def data(self):
        return self._data

    @property
    def cycle(self):
        return self._cycle

    @cycle.setter
    def cycle(self, value):

        if not isinstance(value, (bool,)):
            raise TypeError('Cycle property must be a bool!')

        self._cycle = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):

        if not isinstance(value, (str,)):
            raise TypeError('Name property must be a string!')

        self._name = value

    @property
    def FPS(self):
        return self._FPS

    @FPS.setter
    def FPS(self, value):

        if not isinstance(value, (int,)):
            raise TypeError('FPS property must be an integer!')

        if value <= 0:
            raise ValueError('FPS property must be larger than 0!')

        self._FPS = value
        self._construct()

    @property
    def segments(self):
        return self._get_sorted_segments()

    @segments.setter
    def segments(self, value):

        # Before we do anything make sure the segments are
        # given in the right format
        if not isinstance(value, (list,)):
            raise TypeError('Segments property must be a list!')

        for item in value:

            if not isinstance(item, (tuple,)) or len(item) != 2:
                raise TypeError('Each segment must be a tuple of '
                                'length 2!')

            # Unpack the tuple
            frame = item[0]

            if not isinstance(frame, (int,)):
                raise TypeError('The frame number must be an integer!')

            if frame < 0:
                raise ValueError('The frame number cannot be negative!')

            data = item[1]

            try:
                _ = (v for v in data)
            except:
                raise TypeError('The segment data must be iterable!')

        # Only now do we accept it and do our thing
        self._segments = value
        self._construct()

    def _get_sorted_segments(self):
        return sorted(self._segments, key=lambda x: x[0])

    def _construct(self):
        # This function takes the segments and combines them
        # into a single continuous array of data.
        #
        # To make things simple, we assume that the data starts
        # at frame 0 and if a segment starts before the previous
        # has finished then we shift it so that it starts immediately
        # afterwards

        # Get the segments and setup
        segments = self._get_sorted_segments()
        array = []
        current_time = 0

        for segment in segments:

            # Unpack the segment
            frame, data = segment

            if frame > current_time:

                # Pad the data until its time to start with the
                # previous value
                value = data[0] if len(array) == 0 else array[-1]
                array = np.append(array,
                                  [value for _ in range(frame - current_time)])

            # Add on the data
            array = np.append(array, data)
            current_time = len(array)

        # Set the data
        self._data = np.array(array)


class Driver:
    """
    A Driver can be used to control a Puppet, it has one or
    more channels that represent a single 'string' on a given
    puppet. It is responsible for ensuring consistency across
    each of the tracks.
    """

    def __init__(self, channels=None, FPS=25):

        self._channels = {}

        if channels is not None:
            for c in channels:
                self.add_channel(c)
                self._channels[c] = c

        self._FPS = FPS

    def __getitem__(self, index):

        if isinstance(index, (str,)):
            if index in self._channels:
                return self.__getattribute__(index)

        return None

    def add_channel(self, name):

        if name in self._channels:
            raise RuntimeError('There is already a %s channel!' % name)

        # Add the actual channel object
        self.__setattr__(name, Channel(name=name))

        # Also don't forget to add the name to the dict of channels
        self._channels[name] = name

    def del_channel(self, name):

        if name in self._channels:

            # Delete it from the dict of channels
            del self._channels[name]

            # Don't forget the actual channels
            self.__delattr__(name)

    @property
    def channels(self):
        return list(self._channels.keys())


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
