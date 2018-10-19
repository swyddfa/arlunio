from math import floor
from tqdm import tqdm
from .clock import Clock


class Timeline:
    """All time begins here."""

    def __init__(self, duration, fps=25):
        self._clock = Clock(fps)
        self.duration = duration
        self.framecount = floor(duration * fps)

    def main(self, f):
        self._clock.on_tick(f)
        return f

    def render(self):

        with tqdm(total=self.framecount) as pbar:

            while self._clock.time <= self.duration:
                self._clock()
                pbar.update(1)
