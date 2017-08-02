import multiprocessing as mp


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
