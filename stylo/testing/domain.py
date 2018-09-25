import pytest

from stylo.domain import RealDomain
from stylo.testing._factory import define_domain_test


BaseRealDomainTest = define_domain_test(RealDomain)


class BaseDomainTransformTest:
    """A base class for testing domain transform functions.

    When writing your test case for a domain transform function you declare it as
    follows.

    .. code-block:: python

       from unittest import TestCase
       from stylo.testing.domain import BaseDomainTransformTest

       class TestMyTransformFunction(TestCase, BaseDomainTransformTest):
          ...

    .. note::

       The order in which you write the classes is *very* important.

    You also need to define the :code:`setUp` method to set the following attributes

    - :code:`transform`: This is your tranformation function
    - :code:`args`: A list containing some example *args for your function.
    - :code:`kwargs` A dict containing any keyword arguments.

    .. code-block:: python

       def setUp(self):
           self.transform = my_transform_function
           self.args = [1, 2, 4]
           self.kwargs = {'invert': True}

    Then in addition to any tests you write, your domain transform function will be
    automatically tested to see if it passes the check defined below.
    """

    args = None
    kwargs = None

    def _invoke(self, argument):

        args = [] if self.args is None else self.args
        kwargs = {} if self.kwargs is None else self.kwargs

        return self.transform(argument, *args, **kwargs)

    def test_transform_with_int(self):
        """Ensure that if the transform is given some object that cannot be transformed
         such as an integer this transform raises an exception."""

        with pytest.raises(TypeError) as err:
            self._invoke(2)

        assert "Unable to perform" in str(err.value)
