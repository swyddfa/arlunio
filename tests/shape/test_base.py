import pytest

from stylo.shapes import shape
from stylo.shapes.base import SHAPE_DOCSTRING, _normalise_name


@pytest.mark.shape
class TestShape:
    """Tests for the :code:`shape` decorator and for the :code:`Shape` class it
    produces."""

    def test_shape_sets_name(self):
        """Ensure that the class returned from the :code:`shape` decorator inherits
        the name of the decorated function."""

        @shape
        def Example():
            pass

        assert Example.__name__ == "Example"

    def test_shape_sets_docstring_when_none(self):
        """Ensure that the class returned from the :code:`shape` decorator is given
        the standard docstring."""

        @shape
        def Example():
            pass

        assert Example.__doc__ == SHAPE_DOCSTRING

    def test_shape_sets_docstring(self):
        """Ensure that the class returned from the :code:`shape` decorator has included
        the function's docstring along with the standard docstring."""

        @shape
        def Example():
            """With a docstring"""
            pass

        assert Example.__doc__ == SHAPE_DOCSTRING + "\n" + "With a docstring"

    def test_shape_checks_parameters(self):
        """Ensure that if a parameter is given that is unexpected that the
        :code:`__init__` method on the generated shape throws a :code:`TypeError`
        just like a regular class."""

        @shape
        def Example(a, *, c=1):
            pass

        with pytest.raises(TypeError) as err:
            Example(b=1)

        assert "unexpected keyword argument 'b'" in str(err.value)

    def test_shape_default_parameters(self):
        """Ensure that if no kwargs are given the shape instance uses the default
        values in the decoratorated function."""

        @shape
        def Example(a, *, b=1, c=-3):
            pass

        example = Example()
        actual = {_normalise_name(k): v for k, v in example._params.items()}

        assert actual == {"b": 1, "c": -3}

    def test_shape_accepts_parameters(self):
        """Ensure that if any valid kwargs are given to the Shape's constructor then
        they are used over the defaults."""

        @shape
        def Example(a, *, b=1, c=2):
            pass

        example = Example(b=0)
        actual = {_normalise_name(k): v for k, v in example._params.items()}

        assert actual == {"b": 0, "c": 2}

    def test_shape_repr(self):
        """Ensure that the generated :code:`Shape` class has a useful :code:`repr`"""

        @shape
        def Example(a, *, b=1, c=0):
            pass

        example = Example()

        assert repr(example) == "Example(b=1, c=0)"

    def test_shape_args(self):
        """Ensure that the :code:`args` property on the generated :code:`Shape` class
        returns the list of domain arguments for the shape."""

        @shape
        def Example(x, y, *, x0=1, y0=2):
            pass

        example = Example()

        assert example.args == ["x", "y"]

    def test_shape_parameters(self):
        """Ensure that the :code:`parameters` property on the generated :code:`Shape`
        class returns the list of parameters for the shape."""

        @shape
        def Example(x, y, *, x0=1, y0=2):
            pass

        example = Example()

        assert example.parameters == ["x0", "y0"]

    def test_call_passes_parameters(self):
        """Ensure that when the class instance is called, is passes the parameters to
        the wrapped function."""

        @shape
        def Example(x, *, x0=1):
            return x - x0

        example = Example()
        assert example(1) == 0

        example = Example(x0=0)
        assert example(1) == 1

    def test_call_args(self):
        """Ensure that the class instance can accept the args as positional
        arguments"""

        @shape
        def Example(x, y):
            return x - y

        example = Example()
        assert example(1, 0) == 1

    def test_call_kwargs(self):
        """Ensure that the class instance can accept the args as keyword arguments."""

        @shape
        def Example(x, y):
            return x - y

        example = Example()
        assert example(y=1, x=0) == -1
