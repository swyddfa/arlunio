import logging

import pkg_resources

logger = logging.getLogger(__name__)
_LOAD_CACHE = {}


class Collection:
    """A collection of items, populate from an entry point."""

    def __init__(self, name, items):
        self.name = name
        self.items = items

    def __repr__(self):
        return f"Collection<{self.name}, {len(self.items)} items>"

    def _get(self, name):
        """Get an item, return None if none exists."""
        if name not in self.items:
            logger.debug(f"Item {name} does not exist in collection {self.name}")
            return None

        item = self.items[name]

        if isinstance(item, pkg_resources.EntryPoint):
            logger.debug(f"Item {name} is an entry point reference, loading...")

            real_item = item.load()
            self.items[name] = real_item

            return real_item

        return item

    def __getitem__(self, name):
        item = self._get(name)

        if item is None:
            raise KeyError(name)

        return item

    def __getattr__(self, name):
        item = self._get(name)

        if item is None:
            raise AttributeError(name)

        return item

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

    logger.debug(f"Loading {name}")
    items = {}

    for item in pkg_resources.iter_entry_points(entry_point):
        logger.debug(f"--> {item.module_name}.{item.name}")
        items[item.name] = item

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

    return _load_collection("Parameter", "arlunio.parameters", docstring)
