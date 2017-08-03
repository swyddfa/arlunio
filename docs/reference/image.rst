Image
=====

The Image object is how you take one or more `Drawables`_ and produce an image
that can be saved as a PNG or other format.

Creation
--------

There are a number of ways you can create a new Image object, one of the most
straight forward ways is to simply specify the width and height of the image in
pixels

From Dimensions
^^^^^^^^^^^^^^^

.. doctest:: img-creation

  >>> from stylo import Image
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

.. figure:: /_static/reference/image/xAA-1-vs-xAA-4.png
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

   >>> from stylo import mk_domain
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

.. figure:: /_static/reference/image/example.png
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

.. figure:: /_static/reference/image/example-no-red.png
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

   from stylo import Image

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

Green
^^^^^

This returns a numpy array with the shape :code:`(height, width)` representing
the green colour value at each pixel in the Image. This can be used to alter
the green colour value at each pixel

.. doctest:: img-prop

   >>> img = Image(1920, 1080, background=(255, 128, 0, 255))
   >>> greens = img.green
   >>> (greens == 128).all()
   True

Blue
^^^^

This returns a numpy array with the shape :code:`(height, width)` representing
the blue colour value at each pixel in the Image. This can be used to alter the
blue colour value at each pixel.

.. doctest:: img-prop

   >>> img = Image(1920, 1080, background=(255, 128, 0, 255))
   >>> blues = img.blue
   >>> (blues == 0).all()
   True

Alpha
^^^^^

This returns a numpy array with the shape :code:`(height, width)` representing
the alpha value at each pixel in the Image. This can be used to alter the alpha
value at each pixel.

.. doctest:: img-prop

   >>> img = Image(1920, 1080, background=(255, 128, 0, 255))
   >>> alphas = img.alpha
   >>> (alphas == 255).all()
   True

xAA
^^^

This property returns the value of the anti-aliasing multiplier :code:`xAA`.

.. doctest:: img-prop

   >>> img = Image(1920, 1080)
   >>> img.xAA
   1

.. note::

    This property is read-only

Domain
^^^^^^

A domain can be associated with an image, it is a function in the :code:`width`
and :code:`height` of an image which returns a numpy meshgrid object
representing the mathematical coordinates at each point. Domains can easily be
created using the :code:`mk_domain` function

.. doctest:: img-prop

    >>> from stylo import mk_domain
    >>> img = Image(1920, 1080)
    >>> img.domain = mk_domain(0, 1, 0, 1)

This associates the domain :math:`[0, 1] \times [0, 1]` with the image
:code:`img`. The domain produced by the call to :code:`mk_domain` is
represented by a function equivalent to

.. code-block:: python

   import numpy as np

   def domain(width, height):
       xs = np.linspace(0, 1, width)
       ys = np.linspace(1, 0, height)

       return np.meshgrid(xs, ys)

.. note::

    See how the values for :code:`ys` are "backwards"? This is due to the
    differences in convention between image processing and mathematics. Images
    tend to have their origin in the upper left, wheras the origin in
    mathematics is usually in the lower left. Reversing the direction of the
    :code:`ys` makes the Image consistent with the mathematical convention.


Manipulations
-------------

There are a couple of manipulations built into Image objects

Inverting Colours
^^^^^^^^^^^^^^^^^

.. figure:: /_static/reference/image/example-inverted.png
    :width: 65%
    :align: center

    The original image with inverted colours

You can very easily invert the colours of an Image object due to the fact that
:code:`Image` objects redefine Python's negation operator


.. code-block:: python

   >>> img = Image.fromfile('example.png')
   >>> (-img).save('example-inverted.png')

"AND"-ing Images
^^^^^^^^^^^^^^^^

.. note::

    This operation will only work between images with identical dimensions!

:code:`Image` objects also overload the bitwise AND syntax in Python (the
:code:`&` operator), which can be used as a Boolean AND in certain
circumstances. For example consider the images :code:`A.png` and :code:`B.png`
below

.. table::
    :class: borderless

    +-------------------------------------------+-------------------------------------------+
    | .. image:: /_static/reference/image/A.png | .. image:: /_static/reference/image/B.png |
    |     :width: 95%                           |     :width: 95%                           |
    |     :align: center                        |     :align: center                        |
    |                                           |                                           |
    | :code:`A.png`                             | :code:`B.png`                             |
    +-------------------------------------------+-------------------------------------------+

Taking the Boolean AND of the two images as follows

.. code-block:: python

   >>> A = Image.fromfile('A.png')
   >>> B = Image.fromfile('B.png')
   >>> (A & B).save('A_and_B.png')

.. figure:: /_static/reference/image/A_and_B.png
    :width: 55%
    :align: center

    The resulting image

.. note::

    It's important to note that for this to work as expected the areas where
    there is nothing have to have zero alpha value - so the colour is
    :code:`(0, 0, 0, 0)` otherwise due to the implementation you might
    encounter some unexpected results.

In other circumstances it can be used to apply masks, for example consider the
images below

.. table::
    :class: borderless

    +-------------------------------------------------+--------------------------------------------------+
    | .. image:: /_static/reference/image/example.png | .. image:: /_static/reference/image/vignette.png |
    |     :width: 95%                                 |     :width: 95%                                  |
    |     :align: center                              |     :align: center                               |
    |                                                 |                                                  |
    | :code:`example.png`                             | :code:`mask.png`                                 |
    +-------------------------------------------------+--------------------------------------------------+

Together along with the :code:`&` operator we can apply a vignette (albeit
quite extreme in this case) to the image as such

.. code-block:: python

    >>> img = Image.fromfile('example.png')
    >>> mask = Image.fromfile('mask.png')
    >>> (img & mask).save('example-vignette.png')

.. figure:: /_static/reference/image/example-vignette.png
    :width: 65%
    :align: center

    The final result.

Mapping Drawables
-----------------

Drawables are the mathematical/abstract description of a shape/texture. They
must be "mapped" onto an Image object in order to be seen, thankfully the
syntax for this is very straightforward

.. code-block:: python

    from mage import Image, cartesian, circle

    dot = circle(0, 0, 0.8, fill=True)

    @cartesian()
    def blackspot(x, y):
        return dot(x, y)

    img = Image(512, 512)
    img(blackspot)
    img.save('blackspot.png')

In this example we create a Drawable called :code:`blackspot` and to map it
onto an Image all we have to do is call the Image object like we would a normal
function :code:`img(blackspot)`.

.. figure:: /_static/reference/image/blackspot.png
    :width: 45%
    :align: center

    :code:`blackspot.png`

.. note::

    For full details on what Drawables are and how they are created please see
    the page on `Drawables`_

The default behavior of this mapping is to then overwrite the domain associated
with the Image (if there is one) with the domain of the newly mapped Drawable.
This can be overridden by passing in the :code:`overwrite_domain=False` option
along with the Drawable.

Alternatively if the Image does have a domain associated with it then you can
optionally ignore the domain that comes with the Drawable object and use the
Image's domain instead this is done by passing the :code:`use_host_domain=True`.
option along with the drawable

Interactive Editing
-------------------

If you are working interactively in a Jupyter Notebook you can easily preview
Image objects using the built-in :code:`show()` method. Be sure to also run the
:code:`%matplotlib inline` magic method when importing the library.

For example, to preview the :code:`example.png` image in a Jupyter Notebook
simply run the following

.. code-block:: python

   from stylo import Image
   %matplotlib inline

   img = Image.fromfile('example.png')
   img.show()

.. note::

    Keep in mind that this is only a preview, and some details - especially at
    higher resolutions will be lost. So the only way currently to get a true
    impression of your Image is to save it and open it in your favourite Image
    viewer

.. _Drawables: ./drawable.html
.. _indexing: https://docs.scipy.org/doc/numpy/user/basics.indexing.html
