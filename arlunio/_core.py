from typing import Any, Dict

import attr


class Key:
    """This class is used to represent x.y.z keys in a collection.

    It's only a thin wrapper around a tuple that should make the implementation of
    collections easier to reason about. A key can be created from a number of strings

    >>> from arlunio._shapes import Key
    >>> Key('a', 'b', 'c')
    k'a.b.c'

    Alternatively from a single string with each part delimited with a dot.

    >>> Key.fromstring('a.b.c')
    k'a.b.c'

    Keys have a length which is equal to the number of components that makes up the
    key.

    >>> k = Key('a', 'b', 'c')
    >>> len(k)
    3

    They can be checked to see if they are equal against other keys, or their string
    representation

    >>> k == Key.fromstring('a.b.c')
    True

    >>> k == "a.b.c"
    True

    Keys can be indexed

    >>> k[0]
    'a'

    But not mutated

    >>> k[1] = 'd'
    Traceback (most recent call last):
        ...
    TypeError: 'Key' object does not support item assignment
    """

    __slots__ = "_key"

    def __init__(self, *args):
        self._key = args

    def __repr__(self):
        return f"k'{str(self)}'"

    def __str__(self):
        return ".".join(self._key)

    def __hash__(self):
        return hash(self._key)

    def __eq__(self, other):

        if isinstance(other, Key):
            return self._key == other._key

        if isinstance(other, str):
            return str(self) == other

        return False

    def __len__(self):
        return len(self._key)

    def __getitem__(self, index):
        return self._key[index]

    def __add__(self, other):
        return Key.fromstring(str(self) + "." + str(other))

    @classmethod
    def fromstring(cls, string):
        return cls(*string.split("."))


@attr.s(auto_attribs=True)
class Collection:
    """A group of related items, indexed by keys."""

    _items: Dict[Key, Any] = attr.Factory(dict)

    def __str__(self):
        sep = "\n|  "
        name = self.__class__.__name__
        header = f"{name}: {len(self)} items{sep}"
        items = sep.join(str(k) for k in self._items.keys())

        return header + items

    def __len__(self):
        return len(self._items)

    def __getitem__(self, key):

        if isinstance(key, int):
            return list(self._items.values())[key]

        raise KeyError(key)

    def __getattr__(self, name):
        candidates = self.find(name)
        cls = self.__class__

        if len(candidates) == 0:
            items = {k: v for k, v in self._items.items() if k[0] == name}

            if len(items) == 0:
                raise AttributeError(f"No item with name: {name}")

            return cls(items=items)

        if len(candidates) == 1:
            return candidates[0]

        raise AttributeError(f"Ambiguous reference: {name}")

    def find(self, name: str):
        """Return a collection of all the items that have the given name."""

        items = {k: v for k, v in self._items.items() if k[-1] == name}
        return Collection(items=items)

    def merge(self, prefix: str, collection) -> None:
        """Given a collection and a prefix, merge its items into the collection."""

        prefix = Key.fromstring(prefix)

        for k, item in collection._items.items():
            self._items[prefix + k] = item
