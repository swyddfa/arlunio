import functools
import logging

import numpy as np

logger = logging.getLogger(__name__)


def any(*args):
    result = functools.reduce(np.logical_or, args)
    logger.debug(f"any( {', '.join(str(a.shape) for a in args)} ) -> {result.shape}")

    return result


def all(*args):
    return functools.reduce(np.logical_and, args)


def invert(x):
    return np.logical_not(x)
