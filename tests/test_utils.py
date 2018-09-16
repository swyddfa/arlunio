import pytest
from hypothesis import given, assume
from unittest import TestCase

from stylo.testing.strategies import real
from stylo.utils import bounded_property


@pytest.mark.utils
class TestBoundedProperty(TestCase):
    """Tests to ensure the :code:`bounded_property` factory function produces
    properties as expected."""

    def test_checks_bounded_below_type(self):
        """Ensure that :code:`bounded_property` informs the user when using a value
        for :code:`bounded_below` with the incorrect type."""

        with pytest.raises(TypeError) as err:
            bounded_property("length", bounded_below="width")

        self.assertIn("must be a number", str(err.value))
        self.assertIn("bounded_below", str(err.value))

    def test_checks_bounded_below_by_type(self):
        """Ensure that :code:`bounded_property` informs the user when using
        a value for :code:`bounded_below_by` with the incorrect type."""

        with pytest.raises(TypeError) as err:
            bounded_property("length", bounded_below_by=2.0)

        self.assertIn("must be a string", str(err.value))
        self.assertIn("bounded_below_by", str(err.value))

    def test_checks_bounded_above_type(self):
        """Ensure that :code:`bounded_property` informs the user when using
        a value for :code:`bounded_above` with the incorrect type."""

        with pytest.raises(TypeError) as err:
            bounded_property("length", bounded_above="width")

        self.assertIn("must be a number", str(err.value))
        self.assertIn("bounded_above", str(err.value))

    def test_checks_bounded_above_by_type(self):
        """Ensure that :code:`bounded_property` informs the user when
        using a value for :code:`bounded_above_` with the incorrect type."""

        with pytest.raises(TypeError) as err:
            bounded_property("length", bounded_above_by=2.0)

        self.assertIn("must be a string", str(err.value))
        self.assertIn("bounded_above_by", str(err.value))

    def test_checks_above_arguments(self):
        """Ensure that :code:`bounded_property` informs the user that it only
        makes sense to use either :code:`bounded_above_by` or :code:`bounded_above`"""

        with pytest.raises(ValueError) as err:
            bounded_property("name", bounded_above=1, bounded_above_by="prop")

        self.assertIn("You can only use", str(err.value))

    def test_checks_below_arguments(self):
        """Ensure that :code:`bounded_below` informs the user that it only
        makes sense to use either :code:`bounded_below` or :code:`bounded_below_by`"""

        with pytest.raises(ValueError) as err:
            bounded_property("name", bounded_below=1, bounded_below_by="prop")

        self.assertIn("You can only use", str(err.value))

    @given(value=real)
    def test_uses_getter(self, value):
        """Ensure that the property constructed by :code:`bounded_property`
        returns the value it manages"""

        class MyClass:
            _length = value
            length = bounded_property("length")

        my_class = MyClass()
        self.assertEqual(value, my_class.length)

    @given(value=real)
    def test_uses_setter(self, value):
        """Ensure that the property constructed by :code:`bounded_property`
        still allows the user to set the value even if no bounds are specified."""

        class MyClass:
            length = bounded_property("length")

        my_class = MyClass()
        my_class.length = value

        self.assertEqual(value, my_class.length)

    def test_setter_checks_type(self):
        """Ensure that the property constructed by :code:`bounded_property`
        checks the type of the value provided."""

        class MyClass:
            length = bounded_property("length")

        my_class = MyClass()

        with pytest.raises(TypeError) as err:
            my_class.length = "10m"

        self.assertIn("length", str(err.value))
        self.assertIn("must be a number", str(err.value))

    @given(value=real, bound=real)
    def test_setter_checks_bounded_below(self, value, bound):
        """Ensure that when given a lower bound via :code:`bounded_below` that
        the property constructed by :code:`bounded_property` checks the value
        against that bound."""

        assume(value <= bound)

        class MyClass:
            length = bounded_property("length", bounded_below=bound)

        my_class = MyClass()

        with pytest.raises(ValueError) as err:
            my_class.length = value

        self.assertIn("must be strictly larger than", str(err.value))
        self.assertIn(str(bound), str(err.value))

        value = 1 - value
        bound = -bound

        # Now we have value > bound
        class MyOtherClass:
            length = bounded_property("length", bounded_below=bound)

        my_other_class = MyOtherClass()
        my_other_class.length = value

        self.assertEqual(value, my_other_class.length)

    @given(value=real, bound=real)
    def test_setter_checks_bounded_below_by(self, value, bound):
        """Ensure that when given an attribute to act as a lower bound via
        :code:`bounded_below_by` that the property constructed by
        :code:`bounded_property` checks the value against that bound."""

        assume(value <= bound)

        class MyClass:
            width = bound
            length = bounded_property("length", bounded_below_by="width")

        my_class = MyClass()

        with pytest.raises(ValueError) as err:
            my_class.length = value

        self.assertIn("must be strictly larger than", str(err.value))
        self.assertIn("width", str(err.value))

        value = 1 - value
        bound = -bound

        # Now we have value > bound
        class MyOtherClass:
            width = bound
            length = bounded_property("length", bounded_below_by="width")

        my_other_class = MyOtherClass()
        my_other_class.length = value

        self.assertEqual(value, my_other_class.length)

    @given(value=real, bound=real)
    def test_setter_checks_bounded_above(self, value, bound):
        """Ensure that when given an upper bound via :code:`bounded_above`
        that the property constructed by :code:`bounded_property` checks the
        value against that bound."""

        assume(value >= bound)

        class MyClass:
            length = bounded_property("length", bounded_above=bound)

        my_class = MyClass()

        with pytest.raises(ValueError) as err:
            my_class.length = value

        self.assertIn("must be strictly less than", str(err.value))
        self.assertIn(str(bound), str(err.value))

        value = -1 - value
        bound = -bound

        # We now have value < bound
        class MyOtherClass:
            length = bounded_property("length", bounded_above=bound)

        my_other_class = MyOtherClass()
        my_other_class.length = value

        self.assertEqual(value, my_other_class.length)

    @given(value=real, bound=real)
    def test_setter_checks_bounded_above_by(self, value, bound):
        """Ensure that when given an upper bound via :code:`bounded_above_by`
        that the property constructed by :code:`bounded_property` checks the
        value against the bound.
        """

        assume(value >= bound)

        class MyClass:
            width = bound
            length = bounded_property("length", bounded_above_by="width")

        my_class = MyClass()

        with pytest.raises(ValueError) as err:
            my_class.length = value

        self.assertIn("must be strictly less than", str(err.value))
        self.assertIn("width", str(err.value))

        value = -1 - value
        bound = -bound

        # Now we have value < bound
        class MyOtherClass:
            width = bound
            length = bounded_property("length", bounded_above_by="width")

        my_other_class = MyOtherClass()
        my_other_class.length = value

        self.assertEqual(value, my_other_class.length)
