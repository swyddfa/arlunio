import numpy as np
from hypothesis import given

from stylo.testing.strategies import shape_mask


class BaseColorMapTest:
    """A base class for testing :code:`ColorMap` implementations.

    When writing your test case for a new :code:`Shape` implementation you need to
    declare it as follows.

    .. code-block:: python

       from unittest import TestCase
       from stylo.testing.color import BaseColorMapTest

       class TestMyColorMap(TestCase, BaseColorMapTest):
           ...

    .. note::

       The order in which you write the classes is *very* important.

    You also need to define a :code:`setUp` method to set the :code:`colormap` attribute
    equal to an instance of your shape implementation

    .. code-block:: python

       def setUp(self):
           self.colormap = MyColorMap()

    Then in addition to any tests your write, your :code:`ColorMap` implementation will
    be automatically tested to see if it passes the checks defined below.
    """

    @given(mask=shape_mask)
    def test_paint(self, mask):
        """Ensure that a colormap can be called with a mask produced by some shape and
        that the result is:

        - A numpy array with the same shape :code:`(height, width)` as the given mask.

        .. note::

           Since :code:`ColorMaps` need to be independent of :code:`ColorSpace` we
           cannot enforce anything about the contents of the array
        """
        colormap = self.colormap
        colorspace = colormap.colorspace
        background = colorspace.parse("ffffff")

        height, width = mask.shape
        dimensions = (height, width, len(background))

        color = np.full(dimensions, background)
        color = colormap(mask, image_data=color)

        self.assertEqual(mask.shape[0], color.shape[0])
        self.assertEqual(mask.shape[1], color.shape[1])
