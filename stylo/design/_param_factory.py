"""A :code:`ParameterGroup` is used to help define and manage a related set of
parameters. For example a "Position" parameter group could contain values for the
:code:`x` and :code:`y` position of an object. Another "Stickman" property group could
contain all the values required to define a stickman with a particular size and shape.

This module much like the :code:`stylo.domain._factory` module defines a number of
functions for declaring new parameter groups of various types. By writing the base
classes using code, we can ensure that all property groups follow the same interface.

Currently the following functions are defined

- :code:`define_parameter_group`: This defines a base, static parameter group.
- :code:`define_time_dependent_parameter_group`: This defines a time-dependent parameter
  group, that can take some time :code:`t` and vary in time. It also provides some
  utilities for visualising these changes over time.
"""
from abc import ABC, abstractmethod
import numpy as np

from stylo.error import MissingDependencyError

try:
    import matplotlib.pyplot as plt

    MATPLOTLIB = True

except ImportError:
    MATPLOTLIB = False


def pgroup_keys(params):
    """Provide the implementation of the :code:`keys` method for this parameter group

    One of the key features of a parameter group is the ability to use the dictionary
    unpacking syntax (:code:`**params`) to conveniently pass all the values into a
    function as a single unit. This syntax is enabled by implementing two methods
    :code:`keys` and :code:`__getitem__`, this function provides the implementation
    of the former.

    :param list params: The list of strings containing the names of the parameters.
    """

    def keys(self):
        return params

    return keys


def pgroup_parameters_prop():
    """Provide the implementation of the :code:`parameters` property.

    The :code:`parameters` property returns a list of all the parameter names in the
    group.
    """

    @property
    def parameters(self):
        return self.keys()

    return parameters


def pgroup_getitem():
    """Provide the implementation of the :code:`__getitem__` method.

    One of the key features of a parameter group is the ability to use the dictionary
    unpacking syntax (:code:`**params`) to conveniently pass all the values into a
    function as a single unit. This syntax is enabled by implementing two methods
    :code:`keys` and :code:`__getitem__`, this function provides the implementation
    of the latter.
    """

    def __getitem__(self, key):
        return self._values[key]

    return __getitem__


def pgroup_init():
    """Provide the implementation of the :code:`__init__` method."""

    def __init__(self):
        self._values = self.calculate()

    return __init__


def pgroup_parameter_prop(param):
    """Provide the implementation of the property getter for the given parameter name.

    This enables the :code:`group.param` syntax.

    :param str param: The parameter name.
    """

    @property
    def parameter(self):
        return self._values[param]

    return parameter


def pgroup_calculate():
    """Define an abstract method for the user to implement.

    The user must define this method to return the values dictionary containing each
    of the parameters in the group,.
    """

    @abstractmethod
    def calculate(self):
        pass

    return calculate


def pgroup_repr(name, params):
    """Provide the implementation of the :code:`__repr__` method.

    :param str name: The name of the parameter group.
    :param: list params: The list of parameter names.
    """

    offset = max([len(p) for p in params]) + 10

    def __repr__(self):

        cls_name = self.__class__.__name__

        values = [
            p + ":" + str(val).rjust(offset - len(p)) for p, val in self._values.items()
        ]

        ps = "\n  ".join(values)
        return "{}: {}\n  {}".format(cls_name, name, ps)

    return __repr__


def define_base_attributes(name, params):
    """Define the attributes, methods and properties that are common to every type of
    parameter group.

    :param str name: The name of the parameter group
    :param list params: The list of strings containing the parameter names.
    """

    attributes = {
        "__doc__": "TODO: Make this docstring useful.",
        "__getitem__": pgroup_getitem(),
        "__repr__": pgroup_repr(name, params),
        "keys": pgroup_keys(params),
        "parameters": pgroup_parameters_prop(),
        "_parameters": params,
    }

    for p in params:
        attributes[p] = pgroup_parameter_prop(p)

    return attributes


def get_parameter_names(parameters):
    """Convert the parameter string supplied by the user into a list of parameter names.

    :param list parameters: The comma separated string of parameter names
    """
    return parameters.replace(" ", "").split(",")


def define_parameter_group(name, parameters):
    """Define a new parameter group.

    :param str name: The name of the parameter group.
    :param list parameters: A list of strings containing the parameter
                            names for the group.
    """

    params = get_parameter_names(parameters)

    attributes = define_base_attributes(name, params)
    attributes["__init__"] = pgroup_init()
    attributes["calculate"] = pgroup_calculate()

    return type(name, (ABC,), attributes)


def tdpgroup_calculate():
    """Define an abstract :code:`calculate` method for users to implement.

    This method will serve the same role as the calculate method in a standard parameter
    group, but this one is dependent on time :code:`t`.
    """

    @abstractmethod
    def calculate(self, t):
        pass

    return calculate


def tdpgroup_init():
    """Provide the implementation of the :code:`__init__` method."""

    def __init__(self):
        self()

    return __init__


def tdpgroup_call():
    """Provide the implementation of the :code:`__call__` method.

    This enables the :code:`**params(t)` functionality and use the parameter group as a
    time dependent function.
    """

    def __call__(self, t=0):
        self._values = self.calculate(t)
        return self

    return __call__


def tdpgroup_plot():
    """Provide the implementation of the :code:`plot` method.

    This enables users to plot the values as they change over time.
    """

    def plot(self, start=0, stop=1, N=128, plot_size=8):

        if not MATPLOTLIB:
            message = (
                "Unable to plot parameter group. Run `pip install stylo[jupyter]`"
                " to install the required dependencies."
            )
            raise MissingDependencyError(message)

        cls = self.__class__
        name = cls.__name__
        base_name = cls.__base__.__name__

        ts = np.linspace(start, stop, N)
        values = self.calculate(ts)

        fig, ax = plt.subplots(1, figsize=(plot_size, plot_size))

        for pname, vals in values.items():
            ax.plot(ts, vals, label=pname)

        # Include a legend, title and label the time axis.
        ax.legend()
        ax.set_title("{}: {}".format(name, base_name))
        ax.set_xlabel("Time (seconds)")

        return ax

    return plot


def define_time_dependent_parameter_group(name, parameters):
    """Define a new time dependent parameter group.

    :param str name: The name of the parameter group
    :param list parameters: A list of strings containing the parameter names for the
                            group.
    """
    params = get_parameter_names(parameters)
    attributes = define_base_attributes(name, params)

    attributes["__call__"] = tdpgroup_call()
    attributes["__init__"] = tdpgroup_init()
    attributes["calculate"] = tdpgroup_calculate()
    attributes["plot"] = tdpgroup_plot()

    return type(name, (ABC,), attributes)
