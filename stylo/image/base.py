import inspect
from stylo.color import FillColor
from stylo.domain import Source


def _define_variable(f):

    name = f.__name__
    defaults = {} if f.__kwdefaults__ is None else f.__kwdefaults__
    params = inspect.signature(f).parameters

    parameters = [key for key in params.keys() if key in defaults]
    args = [key for key in params.keys() if key not in defaults]

    class Variable:
        def __init__(self):
            self._params = defaults
            self._func = f

        def __repr__(self):
            params = ["{}={}".format(k, v) for k, v in self._params.items()]
            return "{}({})".format(name, ", ".join(params))

        def __call__(self, *args, **kwargs):

            params = dict(self._params)

            for pname, pval in kwargs.items():
                if pname in params:
                    params[pname] = pval

            return self._func(*args, **params)

        @property
        def parameters(self):
            return parameters

        @property
        def args(self):
            return args

    Variable.__name__ = name
    return Variable


class Image:
    def __init__(self, *, domain=None, renderer=None, writers=None):
        self._domain = domain
        self.renderer = renderer
        self._writers = writers
        self._layers = []

    def __call__(self, width, height, *args, **kwargs):
        image_data = self.renderer(width, height, self)

        return image_data

    def add_layer(self, shape, color):

        if isinstance(color, str):
            color = FillColor(color)

        self._layers.append((shape, color))

    def variable(self, f):
        """Define a new variable."""

        Variable = _define_variable(f)
        var = Variable()

        self._domain[Variable.__name__] = var
        return var


class ImageFactory:
    """A class for building new image types."""

    def __init__(self):
        self.variables = []
        self.writers = {}
        self.renderer = None

    def variable(self, f):
        """Define a new variable for the image domain."""
        Variable = _define_variable(f)
        self.variables.append(Variable)

        return Variable()

    def render(self, f):
        """Define a new renderer for the image."""
        self.renderer = f
        return f

    def writer(self, f):
        """Define a new output writer for image data."""

        name = f.__name__
        self.writers[name] = f

        return f

    def construct(self):
        """Take everything defined so far and convert it into an image."""

        if self.renderer is None:
            raise TypeError("Missing renderer definition.")

        def new_image(*args, **kwargs):

            domain = Source()

            for var in self.variables:
                domain[var.__name__] = var()

            return Image(domain=domain, writers=self.writers, renderer=self.renderer)

        return new_image
