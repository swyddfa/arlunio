from stylo.domain import Domain
from .interpolate import Sampler


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
        return self.__getattribute__("_" + name)[self._current_time]

    # Do the right thing depending on the type of value given
    def setter(self, value):

        if isinstance(value, (int, float)):
            value = make_sampler(name, value)

        self.__setattr__("_" + name, value)

    return property(fget=getter, fset=setter)


class MetaDrawable(type):
    """
    The :code:`MetaDrawable` constructs :code:`Drawables`.

    Each Drawable has an internal clock which can be used when animating
    various aspects of the shape. However this clock should be nearly
    invisible to the user and the clock should be applied automatically
    when needed. Hopefully this means that this metaclass will enable the
    following use case.

    .. code-block:: python

        class Pacman(Drawable):
            open = 0.5

            def mask(self, r, t):
                return r <= 0.8 and not abs(t) < self.open * 0.6

            def color():
                return (255, 255, 0)

    In the example :code:`open` is a 'tweakable' and upon creation of the
    pacman class will be converted to a Sampler behind the scenes and stored in
    self._open. Additionally a property object will be created that will
    automatically index the Sampler object with the current internal time of
    the drawable.

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
        values = [
            (key, val)
            for key, val in attrs.items()
            if not key.startswith("_") and isinstance(val, (int, float))
        ]

        # Start building the new attrs argument, of course it should contain
        # anything we havent messed with
        new_attrs = [
            (key, val) for key, val in attrs.items() if (key, val) not in values
        ]

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
            new_attrs.append(("_" + key, sampler))

            # Construct the property object which acts as gatekeeper
            # and liason with these animation driver objects
            prop = make_property(key)
            new_attrs.append((key, prop))

        # Add the list of parameters to the new object
        new_attrs.append(("parameters", parameters))

        # Now that we have rewritten what we wanted to, time to
        # tell Python to go ahead and create the object.

        # I'm still not 100% clear on this next bit, but in order
        # to have this metaclass rewrite class definitions that
        # inherit from Drawable (as our users will) then we need
        # to call super().__new__ instead of type.__new__
        return super().__new__(cls, name, base, dict(new_attrs))


class Drawable(metaclass=MetaDrawable):
    def __init__(self, domain=None):
        self._current_time = 0
        self._domain = Domain() if domain is None else domain
        self.calculate()

    def __getitem__(self, key):

        if isinstance(key, (int,)) and key >= 0:
            self._current_time = key
            self.calculate()

        return self

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, value):

        if not isinstance(value, (Domain,)):
            raise TypeError(
                "The domain property can only be set to an "
                "instance of a Domain object!"
            )

        self._domain = value

    def calculate(self):
        return

    def mask(self):
        return True

    def color(self):
        return (0, 0, 0, 255)
