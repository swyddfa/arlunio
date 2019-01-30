import inspect
import networkx as nx
import matplotlib.pyplot as plt


class Source:
    """A source object can hold and manage a collection of named sources."""

    def __init__(self, *args):
        self._sources = {}
        self._args = list(args)

    def __repr__(self):
        return "{}: {}".format(self.name, repr(self._sources))

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
        """Return an evaluation order that takes into account the dependencies between the variables."""
        dep_graph = self._build_dep_graph(selection)
        return list(nx.topological_sort(dep_graph))

    def new(self, f):
        """Declare a new source."""
        tweaked = Tweakable(f)
        self[f.__name__] = tweaked

        return tweaked

    def plot(self, figsize=12, selection=None):
        """Return a matplotlib plot visualising the dependencies between the sources."""
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
        self._func = f
        self._defaults = {} if f.__kwdefaults__ is None else f.__kwdefaults__

    def __repr__(self):
        params = ["{}={}".format(k, v) for k, v in self._defaults.items()]
        return "{}({})".format(self._func.__name__, ", ".join(params))

    def __call__(self, *args, **kwargs):

        params = dict(self._defaults)

        for name, val in kwargs.items():
            if name in params:
                params[name] = val

        return self._func(*args, **params)

    @property
    def tweaks(self):
        return list(self._defaults.keys())

    @property
    def args(self):
        params = inspect.signature(self._func).parameters
        return [k for k in params.keys() if k not in self.tweaks]
