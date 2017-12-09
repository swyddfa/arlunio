import numpy as np
import re

from math import sin, cos

from .interpolate import Sampler


def mk_repeater(x_min, x_max):
    """
    Factory function produce a repeater function. Given the
    bounds of the domain, the resulting function will shift values
    until it lies within the resulting domain

    Parameters
    ----------
    x_min : float
        The minimum value of the domain
    x_max : float
        The maximum value of the domain

    Returns
    -------
    A function that accepts a numpy array and shifts each of the
    elements until they lie within the specified domain
    """

    x_length = x_max - x_min

    def repeat(x):

        while x > x_max:
            x -= x_length

        while x < x_min:
            x += x_length

        return x

    return np.vectorize(repeat)


class Domain:
    """
    How we represent a 2D mathematical domain.
    """

    def __init__(self, x_min=-1, x_max=1, y_min=-1, y_max=1):

        if x_min >= x_max:
            message = 'Invalid range for X domain: '
            message += '[{}, {}]\n'.format(x_min, x_max)
            message += 'x_min must be less than x_max'

            raise ValueError(message)

        if y_min >= y_max:
            message = 'Invalid range for Y domain: '
            message += '[{}, {}]\n'.format(y_min, y_max)
            message += 'y_min must be less than y_max'

            raise ValueError(message)

        self._xmin = x_min
        self._xmax = x_max
        self._ymin = y_min
        self._ymax = y_max

        # A list to put all the modification functions in to be applied
        # later
        self._mods = []

        # Here we build a dict containing "instructions" on how to get the
        # values for the desired coordinate values
        self._coords = {
            'x': lambda w, h: self._X(w, h),
            'y': lambda w, h: self._Y(w, h),
            'r': lambda w, h: self._R(w, h),
            't': lambda w, h: self._T(w, h),
        }

    def __str__(self):
        return "[{}, {}] x [{}, {}]".format(self._xmin, self._xmax,
                                            self._ymin, self._ymax)

    def __repr__(self):
        return "Domain(x_min={},x_max={},y_min={},y_max{})".format(self._xmin,
               self._xmax, self._ymin, self._ymax)

    def __getitem__(self, key):

        # We need to make sure we get the three things we expect from
        # the user
        try:
            coordstr, width, height = key
        except ValueError:
            message = ('Expected: \'coordstr\', i, j where\n'
                       'coordstr: a string representing the variables '
                       'you wanted e.g. \'xy\'\n'
                       'i: the width of the picture in pixels\n'
                       'j: the height of the picture in pixels')

            raise ValueError(message)

        # Next, we need to validate the coordinate string
        coordstr = ''.join(coordstr)
        fmt = re.compile('\A[' + self.coords + ']+\Z')

        if not fmt.match(coordstr):
            message = 'Coordinate string can only contain one '
            message += 'of the following: '
            message += ', '.join(self.coords)

            raise ValueError(message)

        # Next just make sure the dimensions are ok
        width_ok = isinstance(width, (int,)) and width > 0
        height_ok = isinstance(height, (int,)) and height > 0

        if not (width_ok and height_ok):
            raise ValueError('Width and Height must be specified by positive integers!')

        # Finally! We can return the coordinates asked for
        return tuple(self._coords[c](width, height) for c in coordstr)

    def __call__(self, f):
        return Drawable(domain=self, mask=f, color=None, name=f.__name__)

    def _gen_coords(self, width, height):
        # Generate the 'vanilla' grid of coordinates

        xs = np.linspace(self._xmin, self._xmax, width)
        xs = np.array([xs for _ in range(height)])

        ys = np.linspace(self._ymax, self._ymin, height)
        ys = np.array([ys for _ in range(width)])
        ys = ys.transpose()

        return (xs, ys)

    def _get_coords(self, width, height):
        # Get the grid of coordinates, modifications and all

        X, Y = self._gen_coords(width, height)

        for mod in self._mods:
            X, Y = mod(X, Y)

        return (X, Y)

    def transform(self, dx=[0, 0], r=0):

        def transformation(X, Y):
            # The following is the equivalent of doing the
            # transformation matrix multiplication 'by hand'
            Xp = X * np.cos(-r) - Y * np.sin(-r) - dx[0]
            Yp = X * np.sin(-r) + Y * np.cos(-r) - dx[1]

            return (Xp, Yp)

        self._mods.insert(0, transformation)


    def repeat(self, x_min, x_max, y_min, y_max):

        x_repeat = mk_repeater(self._xmin, self._xmax)
        y_repeat = mk_repeater(self._ymin, self._ymax)

        self._xmin = x_min
        self._xmax = x_max
        self._ymin = y_min
        self._ymax = y_max

        self._mods.insert(0, lambda x, y: (x_repeat(x), y_repeat(y)))

    @property
    def coords(self):
        return ''.join(self._coords.keys())


    @property
    def _X(self):

        def mk_xs(width, height):
            X, _ = self._get_coords(width, height)
            return X

        return mk_xs

    @property
    def _Y(self):

        def mk_ys(width, height):
            _, Y = self._get_coords(width, height)
            return Y

        return mk_ys

    @property
    def _R(self):

        X = self._X
        Y = self._Y

        def mk_rs(width, height):

            XS = X(width, height)
            YS = Y(width, height)

            return np.sqrt(XS * XS + YS * YS)

        return mk_rs

    @property
    def _T(self):

        X = self._X
        Y = self._Y

        def mk_ts(width, height):

            XS = X(width, height)
            YS = Y(width, height)

            return np.arctan2(YS, XS)

        return mk_ts


def make_sampler(name, value):
    """
    Given a name and a value return a Sampler object of that
    value
    """

    def f(x):
        return value

    return Sampler(f, num_points=25, name=name)


def make_property(name):
    """
    Given a name, construct a property object that controls
    access to an object stored under _name.
    """

    # When the value is accessed, return its value at the
    # current internal time of the Drawable
    def getter(self):
        return self.__getattribute__('_' + name)[self._current_time]

    # Do the right thing depending on the type of value given
    def setter(self, value):
        self.__setattr__('_' + name, value)

    return property(fget=getter, fset=setter)


class MetaDrawable(type):
    """
    The MetaDrawable constructs Drawables.

    Each Drawable has an internal clock which can be used when animating
    various aspects of the shape. However this clock should be nearly
    invisible to the user and the clock should be applied automatically
    when needed. Hopefully this means that this metaclass will enable the
    following use cases.

    class Pacman(Drawable):

        open = 0.5

        def mask(self, r, t):
            return r <= 0.8 and not abs(t) < self.open * 0.6

        def color():
            return (255, 255, 0)

    In the example "open" is a 'tweakable' and upon creation of the pacman
    class will be converted to a Sampler behind the scenes and stored in
    self._open. Additionally a property object will be created that will
    automatically index the Sampler object with the current internal time
    of the drawable.

    This way it allows the user to write the mask and color code as if
    it was a single value. By changing the Sampler object in the Drawable
    you can then animate as you see fit - without altering the definition!
    """
    def __new__(cls, name, base, attrs):
        """
        Here is where the magic happens! This method is called on any class
        definition that makes use of this metaclass and allows us to
        rewrite it before it is even created!

        The argument we care most about is the attrs, as this allows us to
        change out the objects for what we actually want them to be. It
        contains many things, the module the class is defined in, any methods
        and of the course the attributes we actually want to change.
        """

        # The first step is to extract all the attrbiutes that we want to
        # mess with.
        values = [(key, val) for key, val in attrs.items()
                  if not key.startswith('_') and isinstance(val, (int, float))]

        # Start building the new attrs argument, of course it should contain
        # anything we havent messed with
        new_attrs = [(key, val) for key, val in attrs.items()
                     if (key, val) not in values]

        # We also would like to give Drawables a list of all the parameters
        # that can be tweaked - this should help users figure out 3rd party
        # drawables a bit better.
        parameters = []

        # Now for each value we have collected
        for key, val in values:

            # Make note of the name
            parameters.append(key)

            # Construct a Sampler object on the default value
            sampler = make_sampler(key, val)
            new_attrs.append(('_' + key, sampler))

            # Construct the property object which acts as gatekeeper
            # and liason with these animation driver objects
            prop = make_property(key)
            new_attrs.append((key, prop))

        # Add the list of parameters to the new object
        new_attrs.append(('parameters', parameters))

        # Now that we have rewritten what we wanted to, time to
        # tell Python to go ahead and create the object.

        # I'm still not 100% clear on this next bit, but in order
        # to have this metaclass rewrite class definitions that
        # inherit from Drawable (as our users will) then we need
        # to call super().__new__ instead of type.__new__
        return super().__new__(cls, name, base, dict(new_attrs))


class Drawable(metaclass=MetaDrawable):

    def __init__(self):
        self._current_time = 0

    def __getitem__(self, key):

        if isinstance(key, (int,)) and key >= 0:
            self._current_time = key

        return self

    def domain(self):
        return Domain()

    def mask(self):
        return True

    def color(self):
        return (0, 0, 0, 255)
