import numpy as np


class LogicalAnd:
    """Represents a logical AND between N values.

    Yes, there is currently no reason to use a class but where I want to
    take this in the near future will require a class.
    """

    def __init__(self, values):
        self.values = values

    def __call__(self):

        result = True

        for v in self.values:
            result = np.logical_and(result, v)

        return result


def anded(*args):
    logical_and = LogicalAnd(args)
    return logical_and()
