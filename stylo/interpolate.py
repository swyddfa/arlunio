import numpy as np
import matplotlib.pyplot as plt


from itertools import cycle
from math import floor


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
                prepension = list(
                                reversed([next(data) for _ in range(length)]))

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
                (v for v in data)
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

    def __init__(self, FPS=25):
        self._channels = {}
        self._FPS = FPS

    def __len__(self):

        lengths = []

        for name in self._channels:
            channel = self.__getattribute__(name)
            lengths.append(len(channel))

        return max(lengths)

    def _to_frame_number(self, realtime):

        if isinstance(realtime, (int,)):
            return realtime

        return floor(realtime * self.FPS)

    def _get_from_str(self, index):

        if index not in self._channels:
            raise IndexError('No such Channel: {}'.format(index))

        return self.__getattribute__(index)

    def __getitem__(self, index):

        if isinstance(index, (str,)):
            return self._get_from_str(index)

    def add_channel(self, name, channel=None, offset=0.0, *args, **kwargs):
        """
        Add a Channel to the Driver object.

        Either you can provide a name and the relevant __init__ arguments
        to this method and a new Channel instance will be created and added
        under the given name.

        Or you can provide a name and an existing Channel instance which will
        be added to the Driver under the given name

        Parameters:
        -----------

        name: str
            The name you want to give to the Channel
        offset: float, optional
            The time you want to delay the start of the channel by, in seconds
            Default: 0.0
        channel : Channel, optional
            The instance of the Channel you want to add.
            Default: None

        See the documentation for the Channel's __init__ for more information
        on what can be passed to this function
        """

        if not isinstance(name, (str,)):
            raise TypeError('Channel names must be a string!')

        if name == '':
            raise ValueError('Channel names cannot be the empty string')

        if name in self._channels:
            raise RuntimeError('A Channel with the name "{}" '.format(name)
                               + 'already exists!')

        if channel is not None and not isinstance(channel, (Channel,)):
            raise TypeError('Expected Channel instance, got ' +
                            '{} instead'.format(type(channel)))

        # Did the user provide an exisiting channel?
        if channel is not None:
            # Enforce the new name on the channel
            channel.name = name
            self.__setattr__(name, channel)

        else:
            # Otherwise add new Channel object, accessible as an attribute
            # of the same name
            self.__setattr__(name, Channel(name=name, *args, **kwargs))

        # Don't forget to add the name to the internal record
        self._channels[name] = offset

    def del_channel(self, name):
        """
        Delete a Channel from the Driver instance.

        Given a name representing the channel you want deleted
        the method removes the channel instance from the driver.

        Parameters:
        -----------

        name: str
            The name of the channel you want deleted
        """

        if not isinstance(name, (str,)):
            raise TypeError('Channel names must be referenced by a string')

        if name not in self._channels:
            raise RuntimeError('Channel name "{}" '.format(name) +
                               'does not exist!')

        # Delete the Channel instance
        self.__delattr__(name)

        # Remove the entry from the internal record
        del self._channels[name]

    @property
    def channels(self):
        return list(self._channels.keys())

    @property
    def FPS(self):
        return self._FPS

    @FPS.setter
    def FPS(self, value):

        if not isinstance(value, (int,)):
            raise TypeError('FPS property must be an integer!')

        if value < 1:
            raise ValueError('FPS property must be larger than zero!')

        self._FPS = value


class Sampler:

    def __init__(self, f=None, num_points=25, name=None, domain=[0, 1]):

        if f is not None and not callable(f):
            raise TypeError('f must be a function!')

        self._f = f
        self._num_points = num_points
        self._name = name
        self._domain = domain
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

    def __neg__(self):
        return Sampler(lambda x: -self.f(x))

    def __add__(self, other):

        if not isinstance(other, (Sampler,)):
            raise TypeError('Addition is only supported '
                            'between Sampler objects!')

        return Sampler(lambda x: self.f(x) + other.f(x))

    def __sub__(self, other):

        if not isinstance(other, (Sampler,)):
            raise TypeError('Subtraction is only supported '
                            'between Sampler objects!')

        return Sampler(lambda x: self.f(x) - other.f(x))

    def __mul__(self, other):

        if not isinstance(other, (Sampler,)):
            raise TypeError('Multiplication is only supported '
                            'between Sampler objects!')

        return Sampler(lambda x: self.f(x) * other.f(x))

    def _sample(self):
        a, b = self.domain
        points = np.linspace(a, b, self._num_points)

        if self._f is None:
            self._data = points
        else:
            self._data = np.array([self._f(t) for t in points])

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, value):

        if not isinstance(value, (list,)):
            raise TypeError('Domain property must be a list in the form [a,b]')

        a, b = value

        if a >= b:
            raise ValueError('The start of the domain must be strictly less '
                             'than the end!')

        self._domain = value
        self._sample()

    @property
    def f(self):
        if self._f is None:
            return lambda t: t
        else:
            return self._f

    @f.setter
    def f(self, value):

        if not callable(value):
            raise TypeError('f property must be a function!')

        # I'd love to use __code__.co_argcount to make sure we are given
        # a function in a single argument. However this breaks for
        # builtin functions such as math.cos

        self._f = value
        self._sample()

    @property
    def num_points(self):
        return self._num_points

    @num_points.setter
    def num_points(self, value):

        if not isinstance(value, (int,)):
            raise TypeError('num_points must be an integer!')

        if value <= 1:
            raise ValueError('num_points must be larger than 1!')

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
        a, b = self.domain
        points = np.linspace(a, b, self._num_points)
        interval = np.linspace(a, b, 512)
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
