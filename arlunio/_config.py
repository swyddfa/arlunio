import logging
import os
import sys

logger = logging.getLogger(__name__)


def _find_cache_dir() -> str:
    """Try and determine a suitable location to store cached data baed on platform."""

    if sys.platform == "linux" and "XDG_CACHE_HOME" in os.environ:
        return os.environ["XDG_CACHE_HOME"]

    if sys.platform == "linux":
        return os.path.join(os.environ["HOME"], ".cache")

    if sys.platform == "windows" and "APPDATA" in os.environ:
        return os.environ["APPDATA"]

    # Give up and use the current directory.
    return "."


def cache_dir() -> str:
    cache = os.path.join(_find_cache_dir(), "arlunio")

    if not os.path.isdir(cache):
        os.makedirs(cache)

    return cache
