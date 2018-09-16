"""This module contains functions that automate the process of writing base test classes
for :code:`Domain` objects.

"""
import pytest
import numpy as np
from hypothesis import given

from stylo.testing.strategies import dimension


DOMAIN_TEST_DOCSTRING = """
A base class to use when testing {0} implementations.

When writing your test case declare it as follows:

.. code-block:: python

   from unittest import TestCase
   from stylo.testing.domain import Base{0}Test

   class TestMyDomain(TestCase, Base{0}Test):
       ...


.. note::

   The order in which you include these classes is *very* important.

You also need to define a :code:`setUp()` method to set the :code:`domain` attribute to
be an instance of your class.

.. code-block:: python

   def setUp(self):
       self.domain = MyDomain()

If you follow these steps in addition to the test cases you write checking the
specifics of your class it will also be checked to see that it conforms to the behavior
that is expected from every {0} instance.
"""

PARAMETER_READ_ONLY_DOCSTRING = """Ensure that the :code:`{0}` property is read only."""


PARAMETER_DOCSTRING = """
Ensure that the :code:`{0}` property works as expected.

The :code:`{0}` property should:

- Return a function in width and height.
- When called it should return a numpy array.
- The array should have shape :code:`(height, width)`
"""


def parameter_read_only_check(name):
    """Given the name of a parameter to check, make sure that the corresponding
    attribute is read-only.

    :param name: The name of the parameter
    :type name: str
    """

    def check(self):
        with pytest.raises(AttributeError) as err:
            self.domain.__setattr__(name, 2)

        self.assertIn("can't set attribute", str(err.value))

    check.__doc__ = PARAMETER_READ_ONLY_DOCSTRING.format(name)
    return check


def parameter_check(name):
    """Given the name of a parameter to check, make sure that the corresponding
    attribute returns a function that works as expected.

    :param name: The name of the parameter
    :type name: str
    """
    context = given(width=dimension, height=dimension)

    def check(self, width, height):

        param = self.domain.__getattribute__(name)
        self.assertTrue(
            callable(param), "The {} property should return a function".format(name)
        )

        ps = param(width, height)
        self.assertTrue(
            isinstance(ps, (np.ndarray,)), "The function should return a numpy array"
        )

        self.assertEqual(
            (height, width),
            ps.shape,
            "The resulting array should have shape (height, width)",
        )

    check.__doc__ = PARAMETER_DOCSTRING.format(name)
    return context(check)


def define_domain_test(domain):
    """Given a domain definition, write the test class that will automatically verify
    that a given subclass follows the expected interface.
    """
    test_name = "Base" + domain.__name__ + "Test"

    attributes = {"__doc__": DOMAIN_TEST_DOCSTRING.format(domain.__name__)}

    for param in domain._parameters:
        read_only = "test_parameter_{}_read_only".format(param)
        p = "test_parameter_{}".format(param)

        attributes[read_only] = parameter_read_only_check(param)
        attributes[p] = parameter_check(param)

    return type(test_name, (), attributes)
