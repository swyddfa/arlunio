from stylo.domain import RealDomain
from stylo.domain._factory import define_domain_transform

RealDomainTransform = define_domain_transform(RealDomain)

from .rotation import rotate  # noqa: F401
from .shear import horizontal_shear, vertical_shear  # noqa: F401
from .translation import translate  # noqa: F401
