import arlunio as ar
import arlunio.mask as mask
import arlunio.math as math


@ar.definition
def Checker(x: math.X, y: math.Y) -> mask.Mask:
    """
    .. arlunio-image:: Checker
       :align: center

       ::

          from arlunio.pattern import Checker
          from arlunio.image import fill

          checker = Checker()
          image = fill(checker(width=256, height=256))

    A simple checker pattern
    """
    return x * y > 0
