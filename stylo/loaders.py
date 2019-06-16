import logging

import pkg_resources

logger = logging.getLogger(__name__)
_LOAD_CACHE = {}


class Collection:
    """A collection of items."""

    def __init__(self, name, items):
        self.name = name
        self.items = items

    def __repr__(self):
        return f"Collection<{self.name}, {len(self.items)} items>"

    def __getitem__(self, name):
        return self.items[name]

    def __getattr__(self, name):

        try:
            return self.items[name]
        except KeyError:
            raise AttributeError(name)

    def list(self):
        """List all of the available items in the collection."""
        return sorted(list(self.items.keys()))


def _load_collection(name, entry_point, docstring=None):
    """This method builds an enum containing all the items defined in the named
    entry point.

    :param name: The name to give the constructed enum
    :param entry_point: The name of the entry point to load
    :param docstring: If given the constructed enum will be given the docstring
    """

    if name in _LOAD_CACHE:
        return _LOAD_CACHE[name]

    logger.debug(f"Building {name}")
    items = {}

    for item in pkg_resources.iter_entry_points(entry_point):
        logger.debug(f"--> Loading {item.name}")
        items[item.name] = item.load()

    collection = Collection(name, items)

    if docstring is not None:
        collection.__doc__ = docstring

    _LOAD_CACHE[name] = collection
    return collection


def load_parameters():
    """Load all of the available parameters."""

    docstring = """\
    All of the available parameters.
    """

    return _load_collection("Parameter", "stylo.parameters", docstring)


def load_shapes():
    """Load all of the available shapes."""

    docstring = """\
    All of the available shapes.
    """

    return _load_collection("Shapes", "stylo.shapes", docstring)
