Primitives
==========

Stylo has a number of primitives that help you define a few of the most common
shapes and conditions.

Between
-------

.. autofunction:: stylo.prims.between

Examples
^^^^^^^^

.. table::
    :class: borderless

    +---------------------------------------------------+--------------------------------------------------------+
    | .. code-block:: python                            | .. image:: /_static/reference/primitives/x-squared.png |
    |                                                   |    :width: 95%                                         |
    |   from stylo import Image, cartesian, between     |    :align: center                                      |
    |                                                   |                                                        |
    |   @cartesian()                                    |                                                        |
    |   def shape(x, y):                                |                                                        |
    |       return between(x**2 - 0.02, y, x**2 + 0.02) |                                                        |
    |                                                   |                                                        |
    |   img = Image(512, 512)                           |                                                        |
    |   img(shape)                                      |                                                        |
    |   img.example('x-squared.png')                    |                                                        |
    +---------------------------------------------------+--------------------------------------------------------+
    | .. code-block:: python                            | .. image:: /_static/reference/primitives/x-cubed.png   |
    |                                                   |     :width: 95%                                        |
    |   from stylo import Image, cartesian, between     |     :align: center                                     |
    |                                                   |                                                        |
    |   @cartesian()                                    |                                                        |
    |   def shape(x, y):                                |                                                        |
    |       return between(-10, y, x**3)                |                                                        |
    |                                                   |                                                        |
    |   img = Image(512, 512)                           |                                                        |
    |   img(shape)                                      |                                                        |
    |   img.save('x-cubed.png')                         |                                                        |
    +---------------------------------------------------+--------------------------------------------------------+
    | .. code-block:: python                            | .. image:: /_static/reference/primitives/spindle.png   |
    |                                                   |    :width: 95%                                         |
    |   from stylo import Image, cartesian, between     |    :align: center                                      |
    |                                                   |                                                        |
    |   @cartesian()                                    |                                                        |
    |   def shape(x, y):                                |                                                        |
    |       return between(-10, abs(x), abs(y**3))      |                                                        |
    |                                                   |                                                        |
    |   img = Image(512, 512)                           |                                                        |
    |   img(shape)                                      |                                                        |
    |   img.show('spindle.png')                         |                                                        |
    +---------------------------------------------------+--------------------------------------------------------+


Circle
------

.. autofunction:: stylo.prims.circle

.. note::

    As this primitive is constructing a function it is recommened that
    you use it outside of your mask and color functions and simply reference
    the result. Calling it from within these functions will probably result in
    a significant slowdown especially at higher resolutions.

Examples
^^^^^^^^

.. table::
    :class: borderless

    +-----------------------------------------------+-----------------------------------------------------+
    | .. code-block:: python                        | .. image:: /_static/reference/primitives/circle.png |
    |                                               |     :align: center                                  |
    |   from stylo import Image, cartesian, circle  |     :width: 95%                                     |
    |                                               |                                                     |
    |   circle_shape = circle(0, 0, 0.8, pt=0.01)   |                                                     |
    |                                               |                                                     |
    |   @cartesian()                                |                                                     |
    |   def circle(x, y):                           |                                                     |
    |       return circle_shape(x, y)               |                                                     |
    |                                               |                                                     |
    |   img = Image(512, 512)                       |                                                     |
    |   img(circle)                                 |                                                     |
    |   img.save('circle.png')                      |                                                     |
    +-----------------------------------------------+-----------------------------------------------------+
    | .. code-block:: python                        | .. image:: /_static/reference/primitives/disk.png   |
    |                                               |     :align: center                                  |
    |   from stylo import Image, cartesian, circle  |     :width: 95%                                     |
    |                                               |                                                     |
    |   disk_shape = circle(0, 0, 0.8, fill=True)   |                                                     |
    |                                               |                                                     |
    |   @cartesian()                                |                                                     |
    |   def disk(x, y):                             |                                                     |
    |       return disk_shape(x, y)                 |                                                     |
    |                                               |                                                     |
    |   img = Image(512, 512)                       |                                                     |
    |   img(disk)                                   |                                                     |
    |   img.save('disk.png')                        |                                                     |
    +-----------------------------------------------+-----------------------------------------------------+


Ellipse
-------

.. autofunction:: stylo.prims.ellipse

.. note::

    If we set both :math:`a` and :math:`b` equal to 1 in the above equation
    we recover the definition of the `circle`_ as seen above

.. note::

    As this primitive is constructing a function it is recommened that
    you use it outside of your mask and color functions and simply reference
    the result. Calling it from within these functions will probably result in
    a significant slowdown especially at higher resolutions.

Examples
^^^^^^^^

.. table::
   :class: borderless

   +-------------------------------------------------------+-----------------------------------------------------------+
   | .. code-block:: python                                | .. image:: /_static/reference/primitives/ellipse.png      |
   |                                                       |     :width: 95%                                           |
   |   from stylo import Image, cartesian, ellipse         |     :align: center                                        |
   |                                                       |                                                           |
   |   ellipse_shape = ellipse(0, 0, 2, 1, 0.8)            |                                                           |
   |                                                       |                                                           |
   |   @cartesian()                                        |                                                           |
   |   def ellipse(x, y):                                  |                                                           |
   |       return ellipse_shape(x, y)                      |                                                           |
   |                                                       |                                                           |
   |   img = Image(512, 512)                               |                                                           |
   |   img(ellipse)                                        |                                                           |
   |   img.save('ellipse.png')                             |                                                           |
   +-------------------------------------------------------+-----------------------------------------------------------+
   | .. code-block:: python                                | .. image:: /_static/reference/primitives/ellipse-fill.png |
   |                                                       |     :width: 95%                                           |
   |   from stylo import Image, cartesian, ellipse         |     :align: center                                        |
   |                                                       |                                                           |
   |   ellipse_shape = ellipse(0, 0, 2, 1, 0.8, fill=True) |                                                           |
   |                                                       |                                                           |
   |   @cartesian()                                        |                                                           |
   |   def ellipse(x, y):                                  |                                                           |
   |       return ellipse_shape(x, y)                      |                                                           |
   |                                                       |                                                           |
   |   img = Image(512, 512)                               |                                                           |
   |   img(ellipse)                                        |                                                           |
   |   img.save('ellipse-fill.png')                        |                                                           |
   +-------------------------------------------------------+-----------------------------------------------------------+

Rectangle
---------

.. autofunction:: stylo.prims.rectangle

.. note::

    As this primitive is constructing a function it is recommened that
    you use it outside of your mask and color functions and simply reference
    the result. Calling it from within these functions will probably result in
    a significant slowdown especially at higher resolutions.

Examples
^^^^^^^^

.. table::
    :class: borderless

    +------------------------------------------------------+-------------------------------------------------------------+
    | .. code-block:: python                               | .. image:: /_static/reference/primitives/rectangle.png      |
    |                                                      |    :width: 95%                                              |
    |  from stylo import Image, cartesian, rectangle       |    :align: center                                           |
    |                                                      |                                                             |
    |  rect_shape = rectangle(0, 0, 1.25, 0.75, pt=0.02)   |                                                             |
    |                                                      |                                                             |
    |  @cartesian()                                        |                                                             |
    |  def rectangle(x, y):                                |                                                             |
    |      return rectangle_shape(x, y)                    |                                                             |
    |                                                      |                                                             |
    |  img = Image(512, 512)                               |                                                             |
    |  img(rectangle)                                      |                                                             |
    |  img.save("rectangle.png")                           |                                                             |
    +------------------------------------------------------+-------------------------------------------------------------+
    | .. code-block:: python                               | .. image:: /_static/reference/primitives/rectangle-fill.png |
    |                                                      |    :width: 95%                                              |
    |  from stylo import Image, cartesian, rectangle       |    :align: center                                           |
    |                                                      |                                                             |
    |  rect_shape = rectangle(0, 0, 1.25, 0.75, fill=True) |                                                             |
    |                                                      |                                                             |
    |  @cartesian()                                        |                                                             |
    |  def rectangle(x, y):                                |                                                             |
    |      return rectangle_shape(x, y)                    |                                                             |
    |                                                      |                                                             |
    |  img = Image(512, 512)                               |                                                             |
    |  img(rectangle)                                      |                                                             |
    |  img.save("rectangle-fill.png")                      |                                                             |
    +------------------------------------------------------+-------------------------------------------------------------+


Square
------

.. autofunction:: stylo.prims.square

.. note::

    As this primitive is constructing a function it is recommened that
    you use it outside of your mask and color functions and simply reference
    the result. Calling it from within these functions will probably result in
    a significant slowdown especially at higher resolutions.

Examples
^^^^^^^^

.. table::
    :class: borderless

    +-----------------------------------------------+----------------------------------------------------------+
    | .. code-block:: python                        | .. image:: /_static/reference/primitives/square.png      |
    |                                               |     :width: 95%                                          |
    |  from stylo import Image, cartesian, square   |     :align: center                                       |
    |                                               |                                                          |
    |  square_shape = square(0, 0, 1.25, pt=0.02)   |                                                          |
    |                                               |                                                          |
    |  @cartesian()                                 |                                                          |
    |  def square(x, y):                            |                                                          |
    |      return square_shape(x, y)                |                                                          |
    |                                               |                                                          |
    |      img = Image(512, 512)                    |                                                          |
    |      img(square)                              |                                                          |
    |      img.save('square.png')                   |                                                          |
    +-----------------------------------------------+----------------------------------------------------------+
    | .. code-block:: python                        | .. image:: /_static/reference/primitives/square-fill.png |
    |                                               |     :width: 95%                                          |
    |  from stylo import Image, cartesian, square   |     :align: center                                       |
    |                                               |                                                          |
    |  square_shape = square(0, 0, 1.25, fill=True) |                                                          |
    |                                               |                                                          |
    |  @cartesian()                                 |                                                          |
    |  def square(x, y):                            |                                                          |
    |      return square_shape(x, y)                |                                                          |
    |                                               |                                                          |
    |      img = Image(512, 512)                    |                                                          |
    |      img(square)                              |                                                          |
    |      img.save('square-fill.png')              |                                                          |
    +-----------------------------------------------+----------------------------------------------------------+
