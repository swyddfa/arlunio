import inspect

from stylo.math import StyName


SHAPE_DOCSTRING = """\
I am a shape :)
"""


def _set_params(default, override):
    """Return a dictionary based on the given default dictionary, but with
    particular overrides."""

    params = dict(default)

    for key, value in override.items():

        if key not in default:
            raise TypeError("Unexpected keyword argument '{}'".format(key))

        params[key] = value

    return params


def shape():
    """This decorator is used to define a new shape.

    This will convert your function into a class definition.

    """

    def wrapper(func):

        name = func.__name__.capitalize()
        default_params = {} if func.__kwdefaults__ is None else func.__kwdefaults__
        docstring = SHAPE_DOCSTRING

        class Shape:
            def __init__(self, **kwargs):
                self._params = _set_params(default_params, kwargs)
                self.definition = func

            def __repr__(self):
                args = ["{}={}".format(k, v) for k, v in self._params.items()]
                arg_string = ", ".join(args)

                return "{}({})".format(name, arg_string)

            def __call__(self, *args, **kwargs):
                return self.definition(*args, **self._params)

            @property
            def args(self):
                """Return a list of variable names that correspond to the domain arguments
                to the shape."""

                parameters = inspect.signature(self.definition).parameters

                return [
                    k
                    for k, v in parameters.items()
                    if v.kind != inspect.Parameter.KEYWORD_ONLY
                ]

            @property
            def parameters(self):
                """Return a list of variable names that correspond to the shape's parameters."""

                parameters = inspect.signature(self.definition).parameters

                return [
                    k
                    for k, v in parameters.items()
                    if v.kind == inspect.Parameter.KEYWORD_ONLY
                ]

            def expr(self):
                """Return a :code:`StyExpr` representation of the shape."""
                args = [StyName(arg) for arg in self.args]
                return self.definition(*args, **self._params)

        if func.__doc__ is not None:
            docstring += "\n" + func.__doc__

        Shape.__name__ = name
        Shape.__doc__ = docstring

        return Shape

    return wrapper
