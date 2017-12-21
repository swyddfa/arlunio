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

    +-----------------------------------------------------------------------+----------------------------------------------------+
    | .. testcode:: between-1                                               | .. image:: /_static/using/reference/x-squared.png  |
    |                                                                       |    :width: 95%                                     |
    |   from stylo import Image, Drawable, between                          |    :align: center                                  |
    |                                                                       |                                                    |
    |   class Shape(Drawable):                                              |                                                    |
    |       def mask(self, x, y):                                           |                                                    |
    |           return between(x**2 - 0.02, y, x**2 + 0.02)                 |                                                    |
    |                                                                       |                                                    |
    |   shape = Shape()                                                     |                                                    |
    |   img = Image(512, 512)                                               |                                                    |
    |   img(shape)                                                          |                                                    |
    |   img.save('x-squared.png')                                           |                                                    |
    +-----------------------------------------------------------------------+----------------------------------------------------+
    | .. testcode:: between-2                                               | .. image:: /_static/using/reference/loop.png       |
    |                                                                       |     :width: 95%                                    |
    |   from stylo import Image, Drawable, between                          |     :align: center                                 |
    |   from math import sin                                                |                                                    |
    |                                                                       |                                                    |
    |   class Shape(Drawable):                                              |                                                    |
    |       def mask(self, r, t):                                           |                                                    |
    |           return between(0.8*sin(2*t) - 0.04, r, 0.8*sin(2*t) + 0.04) |                                                    |
    |                                                                       |                                                    |
    |   shape = Shape()                                                     |                                                    |
    |   img = Image(512, 512)                                               |                                                    |
    |   img(shape)                                                          |                                                    |
    |   img.save('loop.png')                                                |                                                    |
    +-----------------------------------------------------------------------+----------------------------------------------------+


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

    +---------------------------------------------+------------------------------------------------+
    | .. testcode:: circle-1                      | .. image:: /_static/using/reference/circle.png |
    |                                             |     :align: center                             |
    |   from stylo import Image, Drawable, circle |     :width: 95%                                |
    |                                             |                                                |
    |   circle_shape = circle(0, 0, 0.8, pt=0.01) |                                                |
    |                                             |                                                |
    |   class Circle(Drawable):                   |                                                |
    |       def mask(self, x, y):                 |                                                |
    |           return circle_shape(x, y)         |                                                |
    |                                             |                                                |
    |   circle = Circle()                         |                                                |
    |   img = Image(512, 512)                     |                                                |
    |   img(circle)                               |                                                |
    |   img.save('circle.png')                    |                                                |
    +---------------------------------------------+------------------------------------------------+
    | .. testcode:: circle-2                      | .. image:: /_static/using/reference/disk.png   |
    |                                             |     :align: center                             |
    |   from stylo import Image, Drawable, circle |     :width: 95%                                |
    |                                             |                                                |
    |   disk_shape = circle(0, 0, 0.8, fill=True) |                                                |
    |                                             |                                                |
    |   class Disk(Drawable):                     |                                                |
    |       def mask(self, x, y):                 |                                                |
    |           return disk_shape(x, y)           |                                                |
    |                                             |                                                |
    |   disk = Disk()                             |                                                |
    |   img = Image(512, 512)                     |                                                |
    |   img(disk)                                 |                                                |
    |   img.save('disk.png')                      |                                                |
    +---------------------------------------------+------------------------------------------------+


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

   +-------------------------------------------------------+------------------------------------------------------+
   | .. testcode:: ellipse-1                               | .. image:: /_static/using/reference/ellipse.png      |
   |                                                       |     :width: 95%                                      |
   |   from stylo import Image, Drawable, ellipse          |     :align: center                                   |
   |                                                       |                                                      |
   |   ellipse_shape = ellipse(0, 0, 2, 1, 0.8)            |                                                      |
   |                                                       |                                                      |
   |   class Ellipse(Drawable):                            |                                                      |
   |       def mask(self, x, y):                           |                                                      |
   |           return ellipse_shape(x, y)                  |                                                      |
   |                                                       |                                                      |
   |   ellipse = Ellipse()                                 |                                                      |
   |   img = Image(512, 512)                               |                                                      |
   |   img(ellipse)                                        |                                                      |
   |   img.save('ellipse.png')                             |                                                      |
   +-------------------------------------------------------+------------------------------------------------------+
   | .. testcode:: ellipse-2                               | .. image:: /_static/using/reference/ellipse-fill.png |
   |                                                       |     :width: 95%                                      |
   |   from stylo import Image, Drawable, ellipse          |     :align: center                                   |
   |                                                       |                                                      |
   |   ellipse_shape = ellipse(0, 0, 2, 1, 0.8, fill=True) |                                                      |
   |                                                       |                                                      |
   |   class Ellipse(Drawable):                            |                                                      |
   |       def ellipse(self, x, y):                        |                                                      |
   |           return ellipse_shape(x, y)                  |                                                      |
   |                                                       |                                                      |
   |   ellipse = Ellipse()                                 |                                                      |
   |   img = Image(512, 512)                               |                                                      |
   |   img(ellipse)                                        |                                                      |
   |   img.save('ellipse-fill.png')                        |                                                      |
   +-------------------------------------------------------+------------------------------------------------------+

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

    +------------------------------------------------------+--------------------------------------------------------+
    | .. testcode:: rectangle-1                            | .. image:: /_static/using/reference/rectangle.png      |
    |                                                      |    :width: 95%                                         |
    |  from stylo import Image, Drawable, rectangle        |    :align: center                                      |
    |                                                      |                                                        |
    |  rect_shape = rectangle(0, 0, 1.25, 0.75, pt=0.02)   |                                                        |
    |                                                      |                                                        |
    |  class Rectangle(Drawable):                          |                                                        |
    |      def mask(self, x, y):                           |                                                        |
    |          return rect_shape(x, y)                     |                                                        |
    |                                                      |                                                        |
    |  rectangle = Rectangle()                             |                                                        |
    |  img = Image(512, 512)                               |                                                        |
    |  img(rectangle)                                      |                                                        |
    |  img.save("rectangle.png")                           |                                                        |
    +------------------------------------------------------+--------------------------------------------------------+
    | .. testcode:: rectangle-2                            | .. image:: /_static/using/reference/rectangle-fill.png |
    |                                                      |    :width: 95%                                         |
    |  from stylo import Image, Drawable, rectangle        |    :align: center                                      |
    |                                                      |                                                        |
    |  rect_shape = rectangle(0, 0, 1.25, 0.75, fill=True) |                                                        |
    |                                                      |                                                        |
    |  class Rectangle(Drawable):                          |                                                        |
    |      def mask(self, x, y):                           |                                                        |
    |          return rect_shape(x, y)                     |                                                        |
    |                                                      |                                                        |
    |  rectangle = Rectangle()                             |                                                        |
    |  img = Image(512, 512)                               |                                                        |
    |  img(rectangle)                                      |                                                        |
    |  img.save("rectangle-fill.png")                      |                                                        |
    +------------------------------------------------------+--------------------------------------------------------+


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

    +-----------------------------------------------+-----------------------------------------------------+
    | .. testcode:: square-1                        | .. image:: /_static/using/reference/square.png      |
    |                                               |     :width: 95%                                     |
    |  from stylo import Image, Drawable, square    |     :align: center                                  |
    |                                               |                                                     |
    |  square_shape = square(0, 0, 1.25, pt=0.02)   |                                                     |
    |                                               |                                                     |
    |  class Square(Drawable):                      |                                                     |
    |      def mask(self, x, y):                    |                                                     |
    |          return square_shape(x, y)            |                                                     |
    |                                               |                                                     |
    |  square = Square()                            |                                                     |
    |  img = Image(512, 512)                        |                                                     |
    |  img(square)                                  |                                                     |
    |  img.save('square.png')                       |                                                     |
    +-----------------------------------------------+-----------------------------------------------------+
    | .. testcode:: square-2                        | .. image:: /_static/using/reference/square-fill.png |
    |                                               |     :width: 95%                                     |
    |  from stylo import Image, Drawable, square    |     :align: center                                  |
    |                                               |                                                     |
    |  square_shape = square(0, 0, 1.25, fill=True) |                                                     |
    |                                               |                                                     |
    |  class Square(Drawable):                      |                                                     |
    |      def mask(self, x, y):                    |                                                     |
    |          return square_shape(x, y)            |                                                     |
    |                                               |                                                     |
    |  square = Square()                            |                                                     |
    |  img = Image(512, 512)                        |                                                     |
    |  img(square)                                  |                                                     |
    |  img.save('square-fill.png')                  |                                                     |
    +-----------------------------------------------+-----------------------------------------------------+
