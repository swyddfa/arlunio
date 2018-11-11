from ._param_factory import (  # noqa: F401
    define_parameter_group,
    define_time_dependent_parameter_group,
)

Position = define_parameter_group("Position", "x, y")
Trajectory = define_time_dependent_parameter_group("Trajectory", "x, y")


class StaticPosition(Position):
    """A basic implementation of the :code:`Position` parameter group.

    It takes an x and y and returns them.
    """

    def __init__(self, x=0, y=0):
        self.x_pos = x
        self.y_pos = y
        super().__init__()

    def calculate(self):
        return {"x": self.x_pos, "y": self.y_pos}


def id_func(t):
    return t


class ParametricTrajectory(Trajectory):
    """A basic implementation of the :code:`Trajectory` time dependent parameter group.

    It takes two functions :code:`x(t)` and :code:`y(t)` and returns them.
    """

    def __init__(self, x=None, y=None):

        if x is None:
            x = id_func

        if y is None:
            y = id_func

        self.x_t = x
        self.y_t = y
        super().__init__()

    def calculate(self, t):
        return {"x": self.x_t(t), "y": self.y_t(t)}
