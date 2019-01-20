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

        parameters = inspect.signature(func).parameters
        domain_args = [
            k for k, v in parameters.items() if v.kind != inspect.Parameter.KEYWORD_ONLY
        ]

        args = {arg: StyName(arg) for arg in domain_args + list(default_params.keys())}
        expr = func(**args)

        class Shape:
            def __init__(self, **kwargs):
                self._params = _set_params(default_params, kwargs)
                self._expr = expr
                self._args = domain_args

            def __repr__(self):
                args = ["{}={}".format(k, v) for k, v in self._params.items()]
                arg_string = ", ".join(args)

                return "{}({})".format(name, arg_string)

            def __call__(self, *args, **kwargs):

                posargs = {name: value for value, name in zip(args, self.args)}

                arguments = dict(self._params)
                arguments.update(kwargs)
                arguments.update(posargs)

                return self._expr.eval(arguments)

            @property
            def args(self):
                """Return a list of variable names that correspond to the domain
                arguments to the shape."""
                return self._args

            @property
            def parameters(self):
                """Return a list of variable names that correspond to the shape's
                parameters."""
                return list(self._params.keys())

            @property
            def expr(self):
                """Return a :code:`StyExpr` representation of the shape."""
                return self._expr

        if func.__doc__ is not None:
            docstring += "\n" + func.__doc__

        Shape.__name__ = name
        Shape.__doc__ = docstring

        return Shape

    return wrapper
