from math import floor
from pathlib import Path

from tqdm import tqdm
from .clock import Clock


class Timeline:
    """All time begins here."""

    def __init__(self, seconds=None, minutes=None, hours=None, fps=25):
        self._filename = None
        self._clock = Clock(fps)
        duration = 0

        if hours is not None:
            duration += hours * 60 * 60

        if minutes is not None:
            duration += minutes * 60

        if seconds is not None:
            duration += seconds

        self.fps = fps
        self.framecount = floor(duration * fps)
        self.duration = duration

    def _build_filename(self, filename):
        path = Path(filename)

        pad = "-{{:0{}d}}".format(len(str(self.framecount)))
        fname = path.stem + pad + path.suffix

        fmt_string = str(path.parent.joinpath(fname))
        self._filename = fmt_string

    @property
    def filename(self):
        if self._filename is not None:
            return self._filename.format(self._clock.tick)

    def main(self, f):
        self._clock.on_tick(f)
        return f

    def render(self, filename=None):

        if filename is not None:
            self._build_filename(filename)

        with tqdm(total=self.framecount) as pbar:

            while self._clock.tick < self.framecount:
                self._clock()
                pbar.update(1)
