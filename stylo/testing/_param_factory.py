"""This module contains functions that automate the process of writing base test classes
for :code:`ParameterGroup` objects.
"""
import pytest
import numpy as np

from stylo.error import MissingDependencyError

try:
    from hypothesis import given
    from stylo.testing.strategies import real

except ImportError as err:
    raise MissingDependencyError(
        "The testing package requires additional dependencies."
        " Run `pip install stylo[testing]` to install them."
    ) from err


PARAM_TEST_DOCSTRING = """
A base class to use when testing {0} implementations.

When writing your test case, declare it as follows:

.. code-block:: python

   from unittest import TestCase
   from stylo.testing.design import Base{0}Test

   class TestMyGroup(TestCase, Base{0}Test):
      ...

.. note::

   The order in which you include these classes is *very* important.

You also need to define a :code:`setUp()` method to set the :code:`params` attribute
to be an instance of your class.

.. code-block:: python

   def setUp(self):
       self.params = MyParams()

If you follow these steps in addition to the test cases you write your class will be
automatically checked to see that it conforms to the behavior expected from every {0}.
"""


def keys_check(expected_keys):
    """Parameter groups should define a :code:`keys()` method that returns the name of
    each of the parameters in the group.
    """

    def check(self):
        assert self.params.keys() == expected_keys

    return check


def getitem_check(keys):
    """Parameter groups should define :code:`__getitem__` and return a value for each
    parameter in the group."""

    def check(self):

        for key in keys:
            self.params[key]

    return check


def mapping_check(expected_keys):
    """Parameter groups should support the dictionary unpacking syntax :code:`**params`.
    """

    def check(self):
        def map_func(**kwargs):
            assert set(kwargs.keys()) == set(expected_keys)

        map_func(**self.params)

    return check


def parameters_check(expected_params):
    """Parameter groups should define a :code:`parameters` property that returns a list
    of the parameter names."""

    def check(self):
        assert self.params.parameters == expected_params

    return check


def parameters_check_read_only():
    """The :code:`parameters` property should be read only."""

    def check(self):
        with pytest.raises(AttributeError) as err:
            self.params.parameters = "2"

        assert "can't set attribute" in str(err.value)

    return check


def parameter_check(parameter):
    """Parameter groups should define a property for each parameter name."""

    def check(self):
        self.params.__getattribute__(parameter)

    return check


def parameter_check_read_only(parameter):
    """The declared parameter should be read only."""

    def check(self):

        with pytest.raises(AttributeError) as err:
            self.params.__setattr__(parameter, 2)

        assert "can't set attribute" in str(err.value)

    return check


def define_base_tests(pgroup):
    """Define the test cases that are common to every type of parameter group.

    :param list pgroup: The parameter group to define test cases for.
    """

    params = pgroup._parameters
    attributes = {
        "__doc__": PARAM_TEST_DOCSTRING.format(pgroup.__name__),
        "test_getitem": getitem_check(params),
        "test_keys": keys_check(params),
        "test_parameters": parameters_check(params),
        "test_parameters_read_only": parameters_check_read_only(),
        "test_mapping": mapping_check(params),
    }

    for pname in params:
        property_check = "test_{}_property".format(pname)
        read_only_check = "test_{}_property_read_only".format(pname)

        attributes[property_check] = parameter_check(pname)
        attributes[read_only_check] = parameter_check_read_only(pname)

    return attributes


def define_parameter_group_test(pgroup):
    """Given a parameter group, write the test class that will automatically verify that
    a given subclass follows the expected interface.
    """

    test_name = "Base" + pgroup.__name__ + "Test"
    attributes = define_base_tests(pgroup)

    return type(test_name, (), attributes)


def call_check(expected_keys):
    """Time dependent parameter groups should be able to be called as a function, taking
    the time :code:`t` as an argument."""

    context = given(t=real)

    def check(self, t):
        def map_check(**kwargs):
            assert set(kwargs.keys()) == set(expected_keys)

        result = self.params(t)

        # The parameter group should return itself.
        assert result is self.params
        map_check(**self.params(t))

    return context(check)


def call_check_numpy():
    """Time dependent parameter groups should be able to take numpy arrays as an
    argument."""

    ts = np.linspace(0, 1, 128)

    def check(self):
        self.params(ts)

    return check


def define_time_dependent_parameter_group_test(pgroup):
    """Given a time dependent parameter group, write the test calss that will
    automatically verify that a given subclass follows the expected interface."""

    test_name = "Base" + pgroup.__name__ + "Test"
    params = pgroup._parameters

    attributes = define_base_tests(pgroup)
    attributes["test_call"] = call_check(params)
    attributes["test_call_numpy"] = call_check_numpy()

    return type(test_name, (), attributes)
