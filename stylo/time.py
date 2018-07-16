import numpy as np
import multiprocessing as mp

from math import floor


def animate(f, start=0, stop=10, fps=25, frames=None):
    """
    Given a function `f`, with only the frame number as a
    parameter, evaluate it in parallel to quickly construct
    all frames.

    You can either specify start and stop times (in seconds)
    and the fps or just specify the number of total frames.
    """

    pool = mp.Pool()

    if frames is not None:
        num_frames = frames
    else:
        num_frames = (stop - start) * fps
        pool.map(f, range((stop - start) * fps))

    print('Animating...')
    pool.map(f, range(num_frames))

    pool.close()


class Timeline:
    """Easy time utilities."""

    def __init__(self, end, fps=25):
        self._end = end
        self._fps = fps

    def __contains__(self, t):
        return t >= 0 and t <= self.end

    def __len__(self):
        return floor(self.end * self.fps)

    def __iter__(self):
        time = np.linspace(0, self._end, self._end * self._fps)
        frames = range(len(self))

        timesteps = [(f + 1, t) for f, t in zip(frames, time)]
        return iter(timesteps)

    def __call__(self, func, multi_process=False):
        if not multi_process:
            for f, t in self:
                func(f, t)

        else:
            pool = mp.Pool()
            pool.starmap(func, self)

    @property
    def end(self):
        return self._end

    @property
    def fps(self):
        return self._fps
