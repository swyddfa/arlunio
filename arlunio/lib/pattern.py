import logging

import arlunio as ar
import numpy as np

logger = logging.getLogger(__name__)
pattern = ar.ShapeCollection()


@pattern.shape
def Grid(x, *, nx=4, ny=4, shape=None):
    """Repeatedly draw the given shape in a grid.

    :param nx: The number of times to repeat the shape in the x-direction
    :param ny: The number of times to repeat the shape in the y-direction
    :param shape: The shape instance to draw.
    """

    # Use a parameter to get the dimensions of the image we are drawing.
    # Remember! Parameters return an array of (height, width)
    height, width = x.shape
    bg = np.full((height, width), False)

    logger.debug(f"Grid size: {ny} x {nx}")
    logger.debug(f"Background size: {height} x {width}")

    # Draw the shape at a size determined by the size of the grid
    s_height, s_width = height // ny, width // nx
    mask = shape.mask(s_width, s_height)

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
