from math import floor

from .motion import Driver, driver


def make_driver(name, value):
    """
    Given a name and a default value, construct and return
    a Driver with a single keyframe
    """

    @driver()
    def default():
        return [(0.0, value)]

    default.name = name
    return default


def make_property(name):
    """
    Given the name of the property, construct and return a property
    object which points to '_name' and performs appropriate validation
    on the value given to the setter
    """

    def getter(self):
        return self.__getattribute__('_' + name)

    def setter(self, value):

        if not isinstance(value, (Driver,)):
            raise TypeError("%s must be an instance of Driver!" % name)

        # To ensure consistency across the Puppet, set the driver's FPS
        # to match that of the puppet
        value.FPS = self._FPS

        self.__setattr__('_' + name, value)

    return property(fget=getter, fset=setter)


class PuppetMaster(type):
    """
    The PuppetMaster builds puppets.

    This is my first MetaClass, so there's bound to be some problems with
    this eventually but here goes...

    The whole point of creating a MetaClass is to allow for the following
    usage of a class inheriting from Puppet

    class Pacman(Puppet):

        mouth = 0.5
        direction = 0.0    # Angle in radians

        def draw(self, frame, time):

            @cartesian()
            @translate(r=self.direction[frame])
            @polar
            def pacman(x, y, r, t):

                return r <= 0.8 and not\
                      between(-0.6*self.mouth[frame], t, 0.6*self.mouth[frame])

            @pacman.colormap
            def color():
                return (255, 255, 0)

            return pacman

    Note how in the draw() method we used the mouth and direction attributes
    as if they supported indexing? This is precisely what I want the MetaClass
    for. Behind the scenes when Pacman is created using the PuppetMaster class
    which takes the default values and creates a Driver object and hides it
    behind a property object.

    This allows you to write your 'Puppets' exactly as you would if you were
    animating them but you can give them a default pose, and simply plug in
    the animation later hopefully making them much easier to use and re-use.
    """
    def __new__(cls, name, bases, attrs):
        """
        Here is where we do the dirty work, this is called on any
        class definition which uses this as its MetaClass and let's
        us effectively rewrite it before any objects are actually
        produced.

        The main argment of interest to us is the attrs argument
        it's a dictionary of attributes-to-be names and their associated
        values. It contains everything from the module the class is defined
        in, to any __init__ methods and the attributes we are actaully
        interested in.
        """

        # Extract all the attributes we want to be interpreted as
        # drivers. I expect this might cause issue eventually - selecting
        # items which are not meant to be drivers...
        defaults = [(key, val) for key, val in attrs.items()
                    if not key.startswith('_') and
                           isinstance(val, (int, float))]

        # Start rebuilding the attrs argument, starting with everything
        # we don't need to mess with
        new_attrs = [(key, val) for key, val in attrs.items()
                     if (key, val) not in defaults]

        # For certain tasks, it is useful to maintain a list of drivers
        drivers = []

        # Now for each default value
        for key, val in defaults:

            # Record the driver name
            drivers.append('_' + key)

            # Turn the default value into a driver and put it in
            # self._key
            default = make_driver(key, val)
            new_attrs.append(('_' + key, default))

            # Now make a property object to access this 'hidden' driver
            # as well perfrom some sanity checking on any user provided
            # replacements. Store it in self.key
            prop = make_property(key)
            new_attrs.append((key, prop))

        # Add the list of drivers to the list of attributes
        new_attrs.append(('_drivers', drivers))

        # Now that we've rewritten everything we wanted to, tell Python
        # to go ahead and construct the object.

        # I'm not 100% clear on the specifics of this bit, but in order
        # to support inheriting from Puppet, and still have this MetaClass
        # process the definition we need to call super().__new__ rather
        # than type.__new__()
        return super().__new__(cls, name, bases, dict(new_attrs))


class Puppet(metaclass=PuppetMaster):
    """
    A Puppet allows you to easily define time dependent Drawables
    which are one of the building blocks of many animations.

    **Note:** You should NOT use this class directly, but instead
    create your own class and inherit from this one.
    """

    def __init__(self, FPS=25):
        self._FPS = FPS

    def __getitem__(self, key):

        if isinstance(key, (int,)):
            frame = key
            time = key / self._FPS
        elif isinstance(key, (float,)):
            time = key
            frame = floor(key * self._FPS)
        else:
            raise TypeError('Index must be a single timestamp or '
                            'frame number')

        return self.draw(frame, time)

    @property
    def FPS(self):
        return self._FPS

    @FPS.setter
    def FPS(self, value):

        if not isinstance(value, (int,)):
            raise TypeError('FPS must be an integer!')

        if value <= 0:
            raise ValueError('FPS must be positive!')

        self._FPS = value

        # Ensure that the change in FPS is propogated down
        # to the appropriate drivers
        for d in self._drivers:
            self.__getattribute__(d).FPS = value

    def draw(self, frame, time):
        """
        Users, should provide their own implementation of this method
        """
        raise NotImplementedError('Puppets must have a draw method!!')


def ellipse(x0, y0, a, b, r, pt=0.2, fill=False):
    """
    An ellipse can be defined in the following manner:

        1/a(x - x0)^2 + 1/b(y - y0)^2 = r^2

    This function returns a function in (x, y) and will
    return true if the given point is in the ellipse

    Arguments:
    ----------

    x0 : float
        Represents the x coordinate of the ellipse's center
    y0 : float
        Represents the y coordinate of the ellipse's center
    a : float
        This controls how elongated the ellipse is in the x
        direction
    b : float
        This controls how elongated the ellipse is in the y
        direction
    r : float
        This represents the radius of the ellipse
    pt : float, optional
        Represents the thickness of the lines of the ellipse.
        Default: 0.2
    fill : bool, optional
        Fill the ellipse rather than outline it
        Default: False
        **Note:** If fill is true, this function will ignore the value
        of pt
    """

    lhs = lambda x, y: 1/a*(x - x0)**2 + 1/b*(y - y0)**2

    if fill:

        def ell(x, y):

            if lhs(x, y) <= r**2:
                return True

            return False

        return ell

    else:

        def ipse(x, y):

            val = lhs(x, y)

            if val <= (r + pt)**2 and val >= (r - pt)**2:
                return True

            return False
        return ipse


def circle(x0, y0, r, *args, **kwargs):
    """
    A circle can be defined in the following manner:

        (x - x0)^2 + (y - y0)^2 = r^2

    This function returns a function in (x, y) and
    will return true if the point is in the circle

    Arugments:
    ----------

    x0 : float
        This is the x coordinate of the circle's center
    y0 : float
        This is the y coordinate of the circle's center
    r : float
        This represents the radius of the ellipse
    pt : float, optional
        Represents the thickness of the lines of the circle.
        Default: 0.2
    fill : bool, optional
        Fill the circle rather than outline it
        Default: False
        **Note:** If fill is true, this function will ignore the value
        of pt
    """

    return ellipse(x0, y0, 1, 1, r, *args, **kwargs)


def thicken(f, pt):
    """
    Mathematical paths are all well and good but in order
    to see them they have to have some amount of thickness.

    Given some function which describes a path and a thickness
    this function construct and returns a function which determines
    if some given y is in the neighbourhood of the given function
    at x

    Arguments:
    ----------

    f: callable
        The function you want 'thickened'
    pt: float
        Determines the size of the neighbourhood to test
        in
    """

    def test_func(x, y):

        if y >= f(x) - pt and y <= f(x) + pt:
            return True
        else:
            return False

    return test_func


def between(lower, value, upper):
    return lower <= value and value <= upper


def rectangle(x0, y0, width, height, pt=0.2, fill=False):
    """
    Returns a function in (x, y) which returns true
    when the given point in in/on the rectangle defined by the
    arguments.

    Arguments:
    ----------

    x0 : float
        Represents the x-coordinate of the rectangle's center
    y0 : float
        Represents the y-coordinate of the rectangle's center
    width : float
        Represents the width of the rectangle
    height : float
        Represents the height of the rectangle
    pt : float, optional
        Represents the thickness of the lines of the rectangle.
        Default: 0.2
    fill : bool, optional
        Fill the rectangle rather than outline it
        Default: False
        **Note:** If fill is true, this function will ignore the value
        of pt
    """
    left = x0 - (width / 2)
    right = x0 + (width / 2)
    top = y0 + (height / 2)
    bottom = y0 - (height / 2)

    def rect(x, y):

        if x >= left and x <= right and\
           y >= bottom and y <= top:
            return True

        return False

    if fill:
        return rect

    def small(x, y):

        if x >= left + pt and x <= right - pt and\
           y >= bottom + pt and y <= top - pt:
            return True

        return False

    def test(x, y):

        if rect(x, y) and not small(x, y):
            return True

        return False

    return test


def square(x0, y0, size, *args, **kwargs):
    """
    Returns a function in (x, y) which returns true
    when the given point in in/on the square defined by the
    arguments.

    Arguments:
    ----------

    x0 : float
        Represents the x-coordinate of the rectangle's center
    y0 : float
        Represents the y-coordinate of the rectangle's center
    size : float
        Represents the size of the rectangle
    pt : float, optional
        Represents the thickness of the lines of the rectangle.
        Default: 0.2
    fill : bool, optional
        Fill the rectangle rather than outline it
        Default: False
        **Note:** If fill is true, this function will ignore the value
        of pt

    """
    return rectangle(x0, y0, size, size, *args, **kwargs)
