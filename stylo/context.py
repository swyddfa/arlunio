import logging
import os
import sys
import tempfile

logger = logging.getLogger(__name__)


def ensure_directory(dirname):
    """Ensure that the given directory exists, create it otherwise."""

    if os.path.isfile(dirname):
        raise FileExistsError(f"Expected directory: {dirname}")

    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    return dirname


def find_linux_cache():
    """Try and find a suitable cache dir on linux systems."""

    base = os.path.join(os.environ["HOME"], ".cache")

    if "XDG_CACHE_HOME" in os.environ:
        base = os.environ["XDG_CACHE_HOME"]

    dirname = os.path.join(base, "stylo")
    logger.debug(f"--> Platform is {sys.platform}, using {dirname}")

    return dirname


def find_windows_cache():
    """Try and find a suitable cache dir on windows systems."""

    base = "."

    if "APPDATA" in os.environ:
        base = os.environ["APPDATA"]

    dirname = os.path.join(base, "stylo", "cache")
    logger.debug(f"--> Platform is {sys.platform}, using {dirname}")

    return dirname


def find_cache_dir():
    """Try and find a suitable location to store cache data in based on the
    platform we find ourselves on."""
    platform = sys.platform
    logger.debug("Looking for suitable cache location.")

    if platform == "linux":
        return find_linux_cache()

    if platform == "windows":
        return find_windows_cache()

    logger.debug(f"--> Unknown platform {platform}, using fallback")
    return os.path.join(".", ".stylo")


class Context:
    """The :code:`Context` carries information and abstracts away platform
    specific details."""

    def __init__(self, *, cache_dir=None, tmp_dir=None):
        self.cache_dir = cache_dir
        self.tmp_dir = tmp_dir

    def __del__(self):
        if self._tmp_dir is not None:
            self._tmp_dir.cleanup()

    @property
    def tmp_dir(self):

        if self._tmp_dir is not None:
            return self._tmp_dir.name

    @tmp_dir.setter
    def tmp_dir(self, value):
        self._tmp_dir = value

    @classmethod
    def create(cls):
        """Create a default context."""
        cache_dir = ensure_directory(find_cache_dir())
        tmp_dir = tempfile.TemporaryDirectory()

        return cls(cache_dir=cache_dir, tmp_dir=tmp_dir)
