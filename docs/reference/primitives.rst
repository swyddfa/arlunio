Primitives
==========

Stylo has a number of primitives that help you define a few of the most common
shapes and conditions.

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
    | .. code-block:: python                        | .. image:: /_static/reference/primitives/donut.png  |
    |                                               |     :align: center                                  |
    |   from stylo import Image, cartesian, circle  |     :width: 95%                                     |
    |                                               |                                                     |
    |   donut_shape = circle(0, 0, 0.8)             |                                                     |
    |                                               |                                                     |
    |   @cartesian()                                |                                                     |
    |   def donut(x, y):                            |                                                     |
    |       return donut_shape(x, y)                |                                                     |
    |                                               |                                                     |
    |   img = Image(512, 512)                       |                                                     |
    |   img(donut)                                  |                                                     |
    |   img.save('donut.png')                       |                                                     |
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
