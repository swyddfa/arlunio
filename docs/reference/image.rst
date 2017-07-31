Image
=====

The Image object is how you take one or more Drawables and produce an image
that can be saved as a PNG or other format.

Creation
--------

There are a number of ways you can create a new Image object, one of the most
straight forward ways is to simply specify the width and height of the image in
pixels

From Dimensions
^^^^^^^^^^^^^^^

.. doctest:: img-creation

  >>> from mage import Image
  >>> Image(1920, 1080)
  1920x1080 Image

This simply creates a new Image object with the specified dimensions and the
default fill colour of white. You can choose a different colour by passing in
an optional :code:`background` argument to the constructor, for example to
change the background to black you would do the following

.. doctest:: img-creation

  >>> Image(1920, 1080, background=(0, 0, 0))
  1920x1080 Image

**Note:** Colours are specified by tuples of length 3, or 4 representing RGB or
RGBA colour formats respectively. Individual entries are integers taking values
between 0 and 255 inclusively.

From a File
^^^^^^^^^^^

You can also create an Image object from an existing image using the
:code:`fromfile` class method as such

.. code-block:: python

  >>> Image.fromfile('example.png')
  640x480 Image

From an Array
^^^^^^^^^^^^^

Internally, Images are represented using numpy arrays with the shape
:code:`(height, width, 4)` and :code:`dtype` given by :code:`np.uint8`. If you
have such an array you can make an Image object out of it using the
:code:`fromarray` class method

.. doctest:: img-creation

   >>> import numpy as np
   >>> px = np.full((768, 1024, 4), (255, 0, 0, 0), dtype=np.uint8)
   >>> Image.fromarray(px)
   1024x768 Image

Additional Options
^^^^^^^^^^^^^^^^^^

Anti-Aliasing
"""""""""""""

Currently the only form of anti-aliasing available is the naive and
computationally intensive method of simply generating an image larger than
required and scaling it down to the required size. So at creation time you can
pass in an optional :code:`xAA` which acts as a multiplier and controls the
level of anti-aliasing. The default value of this parameter is :code:`1` which
is equivalent to no anti-aliasing.

.. figure:: /_static/xAA-1-vs-xAA-4.png
    :width: 75%
    :align: center

    Two 128x128 images with :code:`xAA=1` (left) and :code:`xAA=4` (right)

.. note::

    - The :code:`xAA` parameter must be an :code:`int` and :code:`>= 1`
    - The :code:`xAA` parameter can only be set when an Image object is first
      created!


Domain
""""""

Certain operations require that a mathematical domain be associated with an
Image, this can be done in a number of places including the construction of a
new Image using the :code:`domain` parameter. For example to associate the
domain :math:`[0, 1] \times [0, 1]` with an Image we can do the following

.. doctest:: img-creation

   >>> from mage import mk_domain
   >>> Image(512, 512, domain=mk_domain(0, 1, 0, 1))
   512x512 Image


Indexing
--------

By Pixel
^^^^^^^^

Image objects, being built on numpy arrays expose the powerful `indexing`_
syntax for accessing individual pixel values or subsections of an image. This
makes a number of image manipulation tasks easier. For example consider the
following example image

.. figure:: /_static/example.png
    :width: 65%
    :align: center

    The original image: example.png

In just a few short steps we can remove the red color channel from the image

.. code-block:: python

  >>> img = Image.fromfile('example.png')
  >>> img[:, :, 0] = (0,)
  >>> img.save('example-no-red.png')

So if we take a closer look at the second line, the first two indices
:code:`:, :` simply say all the pixels in the image. Then the :code:`0` index
says the first colour channel - which in this case is red which we set to
:code:`0`. We write the zero as :code:`(0,)` simply because numpy is expecting
an iterable when assigning a range.

.. figure:: /_static/example-no-red.png
    :width: 65%
    :align: center

    The original image without the red colour channel

By Coordinate
^^^^^^^^^^^^^

Image objects also support indexing the image based on the mathematical domain
which has been mapped onto it. This allows you to select regions of an image
independently on the actual resolution of the underlying image. This is done by
using floats instead of integers when indexing. For example we can create a
simple checkerboard pattern as follows

.. code-block:: python

    >>> img = Image(512, 512, domain=mk_domain(-1, 1, -1, 1)
    >>> img[:0.0, 0.0:1.0] = (0, 0, 0, 255)
    >>> img[0.0:, :0.0] = (0, 0, 0, 255)

Properties
----------

.. testsetup:: img-prop

   from mage import Image

Image objects have a number of properties that allow you to query or adjust
certain aspects of an Image object

Width
^^^^^

This returns the width of an Image in pixels

.. doctest:: img-prop

   >>> img = Image(1920, 1080)
   >>> img.width
   1920

.. note::

    This property is read-only


Height
^^^^^^

This returns the height of the Image in pixels

.. doctest:: img-prop

   >>> img = Image(1920, 1080)
   >>> img.height
   1080

.. note::

    This property is read-only

Color
^^^^^

This returns a numpy array with the shape :code:`(height, width, 3)`
representing the RGB color values of each pixel. This can be used to alter the
color of each pixel in the Image

.. doctest:: img-prop

    >>> img = Image(1920, 1080, background=(255, 128, 0, 255))
    >>> color = img.color
    >>> color.shape
    (1080, 1920, 3)

Red
^^^

This returns a numpy array with the shape :code:`(height, width)` representing
the red color value at each pixel in the Image. This can be used to alter the
red color value at each pixel.

.. doctest:: img-prop

   >>> img = Image(1920, 1080, background=(255, 128, 0, 255))
   >>> reds = img.red
   >>> (reds == 255).all()
   True

.. _indexing: https://docs.scipy.org/doc/numpy/user/basics.indexing.html
