import numpy as np
from math import floor


class Clock:
    """This manages all the ticking etc."""

    def __init__(self, duration, fps):
        self.duration = duration
        self.fps = fps
        self._timesteps = np.linspace(0, duration, floor(duration * fps))

        self._clock = -1

        self._started = False
        self._finished = False

        self._time = {"f": 0, "t": 0}

    def __getitem__(self, values):
        return tuple(self._time[v] for v in values if v in self._time)

    @property
    def started(self):
        return self._started

    @property
    def finished(self):
        return self._finished

    def start(self):
        self._started = True

    def tick(self):
        """This advances the clock and computes the frame number and real time value."""

        if not self._started:
            self._time["f"] = 0
            self._time["t"] = 0
            return

        if self._finished:
            self._time["f"] = self._clock
            self._time["t"] = self._timesteps[-1]
            return

        self._clock += 1

        if self._clock == len(self._timesteps) - 1:
            self._finished = True

        self._time["f"] = self._clock
        self._time["t"] = self._timesteps[self._clock]
