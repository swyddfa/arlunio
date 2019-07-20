import unittest.mock as mock

import pkg_resources

import py.test
from stylo.loaders import Collection


@py.test.mark.core
class TestCollection:
    """Tests for the :code:`Collection` class."""

    @py.test.fixture()
    def collection(self):
        items = {"one": 1, "two": 2, "three": 3}
        return Collection("Numbers", items)

    def test_getitem(self, collection):
        """Ensure that we can use indexing syntax to get items from a
        collection."""
        assert collection["one"] == 1

    def test_getitem_entry_point(self):
        """Ensure that if an item comes from an entry point, it is loaded before
        being returned."""

        entry_point = pkg_resources.EntryPoint("five", "stylo.numbers")
        entry_point.load = mock.Mock(return_value=5)

        items = {"five": entry_point}
        collection = Collection("Numbers", items)

        assert collection["five"] == 5
        assert collection["five"] == 5

        # The result should be cached after the first time it's accessed.
        entry_point.load.assert_called_once()

    def test_getitem_bad_key(self, collection):
        """Ensure that a collection raises a :code:`KeyError` when a non
        existent key is asked for."""

        with py.test.raises(KeyError) as err:
            collection["four"]

        assert "four" in str(err.value)

    def test_getattr(self, collection):
        """Ensure that we can use regular a.b syntax to get items from a
        collection."""
        assert collection.one == 1

    def test_getattr_entry_point(self):
        """Ensure that is an item comes from an entry point, it is loaded before
        being returned."""

        entry_point = pkg_resources.EntryPoint("five", "stylo.numbers")
        entry_point.load = mock.Mock(return_value=5)

        items = {"five": entry_point}
        collection = Collection("Numbers", items)

        assert collection.five == 5
        assert collection.five == 5

        # The result should be cached after the first time it's accessed.
        entry_point.load.assert_called_once()

    def test_getattr_bad_name(self, collection):
        """Ensure that a Collection raises an :code:`AttributeError` when a non
        existent item is asked for."""

        with py.test.raises(AttributeError) as err:
            collection.four

        assert "four" in str(err.value)
