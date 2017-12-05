from inspect import signature


def get_parameters(f):
    """
    Given a function f, return a tuple of all its
    parameters
    """

    return tuple(signature(f).parameters.keys())
