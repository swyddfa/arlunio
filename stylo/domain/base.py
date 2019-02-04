import inspect
import networkx as nx

from stylo.error import MissingDependencyError

try:
    import matplotlib.pyplot as plt

    MATPLOTLIB = True
except ImportError:
    MATPLOTLIB = False


class Source:
    """A source object can hold and manage a collection of named sources."""

    def __init__(self, *args, name=None):
        self._sources = {}
        self.name = "Source" if name is None else name
        self._args = list(args)

    def __repr__(self):
        sources = "\n\t".join(repr(s) for s in self._sources.values())
        return "{}: \n\t{}".format(self.name, sources)

    def __getitem__(self, key):
        return self._sources[key]

    def __setitem__(self, key, value):

        if not isinstance(value, Tweakable):
            raise TypeError("Expected Tweakable.")

        if key in self._sources:
            raise NameError("Variable '{}' is already defined.".format(key))

        # Look to see if this source can satisfy the requirements.
        available = self.args + self.sources
        required = value.args
        missing = []

        for arg in required:
            if arg not in available:
                missing.append(arg)

        if len(missing) > 0:
            message = "Source is unable to provide the following arguments: {}"
            raise TypeError(message.format(", ".join(missing)))

        self._sources[key] = value

    def __call__(self, names, *args, **kwargs):

        missing = [name for name in names if name not in self.sources]

        if len(missing) > 0:
            message = "Source is unable to provide the following arguments: {}"
            raise TypeError(message.format(", ".format(missing)))

        values = {}

        for name in names:
            values[name] = self._sources[name](*args, **kwargs)

        return values

    def _build_dep_graph(self, selection=None):
        edges = []
        sources = self.sources if selection is None else selection

        for source in sources:
            for dep in [arg for arg in self[source].args if arg not in self.args]:
                edges.append((source, dep))

        graph = nx.DiGraph()
        graph.add_edges_from(edges)
        graph.add_nodes_from(sources)

        return graph

    def _sort(self, selection=None):
        """Return an evaluation order that takes into account the dependencies between
        the variables."""
        dep_graph = self._build_dep_graph(selection)
        return list(nx.topological_sort(dep_graph))

    def new(self, f):
        """Declare a new source."""
        tweaked = Tweakable(f)
        self[f.__name__] = tweaked

        return tweaked

    def plot(self, figsize=12, selection=None):
        """Return a matplotlib plot visualising the dependencies between the sources."""

        if not MATPLOTLIB:
            raise MissingDependencyError("jupyter")

        dep_graph = self._build_dep_graph(selection)

        fig, ax = plt.subplots(1, figsize=(figsize, figsize))
        nx.draw(dep_graph, ax=ax, with_labels=True)

        return ax

    @property
    def args(self):
        return self._args

    @property
    def sources(self):
        return list(self._sources.keys())


class Tweakable:
    """A tweakable is a function that can be tweaked :)"""

    def __init__(self, f):
        super().__setattr__("_func", f)

        defaults = {} if f.__kwdefaults__ is None else f.__kwdefaults__
        super().__setattr__("_defaults", defaults)

    def __repr__(self):
        args = list(self.args)
        args += ["{}={}".format(k, v) for k, v in self._defaults.items()]
        return "{}({})".format(self._func.__name__, ", ".join(args))

    def __call__(self, *args, **kwargs):

        params = dict(self._defaults)

        for name, val in kwargs.items():
            if name in params:
                params[name] = val

        return self._func(*args, **params)

    def __getattr__(self, name):

        try:

            return self._defaults[name]
        except KeyError:
            message = "{} has no attribute {}"
            raise AttributeError(message.format(self.__class__.__name__, name))

    def __setattr__(self, name, value):

        if name in self._defaults:
            self._defaults[name] = value
            return

        object.__setattr__(self, name, value)

    @property
    def defaults(self):
        """Return a dictionary containing the default values for the tweakable
        parameters."""
        return self._defaults

    @property
    def tweaks(self):
        """Return the list of tweakable parameter names.

        These correspond with the keyword only arguments of the function
        and as their name suggests can be tweaked.
        """
        return list(self._defaults.keys())

    @property
    def args(self):
        """Return the list of argument names.

        These correspond to the positional arguments of the function and cannot
        be tweaked.
        """
        params = inspect.signature(self._func).parameters
        return [k for k in params.keys() if k not in self.tweaks]


def tweakable(f):
    """Decorator to convert a normal Python function into a tweakable."""
    return Tweakable(f)
