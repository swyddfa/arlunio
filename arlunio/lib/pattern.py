import logging

import arlunio as ar
import numpy as np

logger = logging.getLogger(__name__)


@ar.definition
def Grid(width, height, *, nx=4, ny=4, shape=None):
    """Repeatedly draw the given shape in a grid.

    :param nx: The number of times to repeat the shape in the x-direction
    :param ny: The number of times to repeat the shape in the y-direction
    :param shape: The shape instance to draw.
    """
    bg = np.full((height, width), False)

    logger.debug(f"Grid size: {ny} x {nx}")
    logger.debug(f"Background size: {height} x {width}")

    # Draw the shape at a size determined by the size of the grid
    s_height, s_width = height // ny, width // nx
    mask = shape(s_width, s_height)

    logger.debug(f"Shape size: {s_height} x {s_width}")

    # Let numpy handle the repeating of the shape across the image.
    pattern = np.tile(mask, (ny, nx))

    # Apply the pattern to the background, depending on the grid size and
    # image dimensions align, the generated grid may not perfectly fill the
    # image.
    p_height, p_width = pattern.shape
    logger.debug(f"Pattern size: {p_height} x {p_width}")

    bg[:p_height, :p_width] = pattern

    return bg


@ar.definition
def Map(width, height, *, layout=None, legend=None):
    """For more complex layouts."""

    nx, ny = len(layout), len(layout[0])
    size = (height // ny, width // nx)  # TODO: Handle divisions with rounding errors

    # Build a new dict with the values being the shapes drawn at the appropriate res
    # to ensure we only draw them once.
    items = {k: v(*size) for k, v in legend.items()}
    return np.block([[items[key] for key in row] for row in layout])


@ar.definition
def Pixelize(width, height, *, pixels=None, shape=None, nx=None, ny=None):
    """Draw a pixelated version of a shape."""

    if shape is None and pixels is None:
        raise ValueError("You must either provide a shape or a pixel pattern.")

    if shape is not None:

        if nx is None or ny is None:
            raise ValueError("You must also provide the `nx` and `ny` size parameters")

        pixels = shape(nx, ny)

    nx, ny = len(pixels), len(pixels[0])
    size = (height // ny, width // nx)  # TODO: Handle divisions with rounding errors

    fill = np.full(size, True)
    empty = np.full(size, False)

    return np.block([[fill if col else empty for col in row] for row in pixels])
