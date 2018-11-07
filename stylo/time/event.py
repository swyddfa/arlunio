from .clock import Clock
from stylo.utils import get_parameters


class Event:
    """A representation of an event that lasts for some duration."""

    def __init__(self, duration, name=None, fps=25, timeline=None):

        self._clock = Clock(duration, fps)
        self._timeline = timeline

        self.duration = duration
        self.name = "Event" if name is None else name

    def __repr__(self):
        return "{0.name}: {0.duration}s".format(self)

    def __call__(self, f):
        """Use this to register a time dependent function with this event."""
        return TimeDependent(self._clock, f)

    @property
    def started(self):
        return self._clock.started

    @property
    def finished(self):
        return self._clock.finished

    def start(self):
        self._clock.start()
        return self

    def tick(self):
        self._clock.tick()
        return self


class TimeDependent:
    """This wraps a callable so that it is given the appropriate time value."""

    def __init__(self, clock, f):

        self._params = get_parameters(f)

        if not set(self._params) <= set("ft"):
            raise TypeError("Expected time dependent function.")

        self.f = f
        self.clock = clock

    def __repr__(self):
        return "{0}\n{1}".format(repr(self.f), repr(self.clock))

    def __call__(self):
        values = self.clock[self._params]
        return self.f(*values)
