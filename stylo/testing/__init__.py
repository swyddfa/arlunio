from .strategies import (  # noqa: F401
    real,
    angle,
    dimension,
    small_dimension,
    image_size,
    domain_values,
    shape_mask,
)
from .color import BaseColorMapTest  # noqa: F401
from .design import (  # noqa: F401
    define_parameter_group_test,
    define_time_dependent_parameter_group_test,
    BasePositionTest,
    BaseTrajectoryTest,
)
from .domain import define_domain_test, BaseRealDomainTest  # noqa: F401
from .image import BaseImageTest  # noqa: F401
from .shape import BaseShapeTest  # noqa: F401
