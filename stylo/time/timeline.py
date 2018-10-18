import numpy as np

from math import floor

from .clock import Clock
from .event import Event, TimeDependent


class Timeline:
    """All time begins here."""

    def __init__(self, duration, fps=25):

        self.duration = duration
        self._clock = Clock(duration, fps)
        self._triggers = {}
        self._tickers = []
        self._main = None

    def __repr__(self):
        return "Timeline: {}s".format(self.duration)

    def _tick(self):

        # Do we need to start any more events?
        realtime, = self._clock["t"]

        for trigger, events in self._triggers.items():

            started = events[0].started

            if trigger <= realtime and not started:
                for event in events:
                    event.start()
                    self._tickers.append(event)

        # Advance all the clocks
        self._clock.tick()
        for event in self._tickers:
            event.tick()

    def _start_at(self, start_time, event):
        """Given an event, start it at the given time."""

        if start_time not in self._triggers:
            self._triggers[start_time] = [event]
            return

        self._triggers[start_time].append(event)

    def main(self, f):
        self._main = TimeDependent(self._clock, f)
        return self._main

    def event(self, duration, start=None, name=None):
        """Place a new event on the timeline."""

        event = Event(duration, name=name, fps=self._clock.fps, timeline=self)

        if start is None:
            start = 0

        self._start_at(start, event)
        return event

    def render(self):

        self._clock.start()

        while not self._clock.finished:
            self._tick()
            self._main()
