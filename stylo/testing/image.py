import base64
from hypothesis import given

from stylo.testing.strategies import dimension


class BaseImageTest:
    """A base class for writing :code:`Image` implementations.

    When writing your test case for a new :code:`Image` implementation you need to
    declare it as follows.

    .. code-block:: python

       from unittest import TestCase
       from stylo.testing.image import BaseImageTest

       class TestMyImage(TestCase, BaseImageTest):
           ...

    .. note::

       The order in which you write the classes is *very* important.

    You also need to define the :code:`setUp` method to set the :code:`image` attribute
    equal to an instance of your image implementation.

    .. code-block:: python

       def setUp(self):
           self.image = MyImage()

    Then in addition to any tests you write, your :code:`Image` implementation will be
    automatically tested to see if passes the checks defined below.
    """

    @given(width=dimension, height=dimension)
    def test_encode(self, width, height):
        """Ensure that if the :code:`encode=True` keyword argument is given then a
        base64 encoded string representing the image in PNG format is returned."""

        # Every PNG image starts with the same magic number.
        # https://en.wikipedia.org/wiki/Portable_Network_Graphics
        magic = base64.b64encode(bytes.fromhex("89504e470d0a1a0a"))

        image_bytes = self.image(width, height, encode=True)

        assert isinstance(image_bytes, (bytes,)), "Expected byte string"
        assert magic[0:11] == image_bytes[0:11]
