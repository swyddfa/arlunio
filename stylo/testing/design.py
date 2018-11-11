from stylo.design import Position, Trajectory
from ._param_factory import (
    define_parameter_group_test,
    define_time_dependent_parameter_group_test,
)

BasePositionTest = define_parameter_group_test(Position)
BaseTrajectoryTest = define_time_dependent_parameter_group_test(Trajectory)
