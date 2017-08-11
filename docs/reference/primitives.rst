Primitives
==========

Stylo has a number of primitives that help you define a few of the most common
shapes and conditions.

Circle
------

.. autofunction:: stylo.prims.circle

Mathematically a circle with centre at :math:`(x_0, y_0)` and radius :math:`r`
is defined as all points :math:`(x, y)` which satisfy

.. math::

    (x - x_0)^2 + (y - y_0)^2 = r^2

The :code:`circle` primitive takes the following arguments:

- :code:`x0`: The x-coordinate of the centre of the circle
- :code:`y0`: The y-coordinate of the centre of the circle
- :code:`r`: The radius of the circle

it returns a function in :code:`(x, y)` that returns :code:`True` if the point
:math:`(x, y)` lies on the circle as defined above. There are also a couple of
optional arguments which control how the circle looks.

- :code:`pt`: This is a float which  controls the thickness of the line used to
  draw the circle. Default: :code:`0.2`
- :code:`fill`: A boolean, if :code:`True` will fill the circle rather than
  draw the outline. This option if set overrides the behavior of the :code:`pt`
  argument. Default: :code:`False`

.. note::

    Since the mask and color functions of drawables are called for every pixel
    in the Image it is being applied to, it is a good idea to use this
    primitive outside of these functions and reference the result. This is so
    your code isn't constantly redefining the same function at each pixel which
    would slow down execution.

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

Mathematically an ellipse can be defined as the set of all points :math:`(x, y)`
which satisfy the following

.. math::

    \frac{(x - x_0)^2}{a^2} + \frac{(y - y_0)^2}{b^2} = r^2

where :math:`(x_0, y_0)` is the center of the ellipse, :math:`a` is known as
the semi major axis and :math:`b` is known as the semi minor axis. Together
they control the proportions of the ellipse and :math:`r` controls the overall
size of the ellipse.

.. note::

    If we set both :math:`a` and :math:`b` equal to 1 in the above equation
    we recover the definition of the `circle`_ as seen above

The :code:`ellipse` primitive takes the following arguments

- :code:`x0`: The x-coordinate of the center of the ellipse
- :code:`y0`: The y-coordinate of the center of the ellipse
- :code:`a`: The value of the semi major axis - larger values make the
  ellipse more elongated in the x-direction
- :code:`b`: The value of the semi minor axis - larger values make the ellipse
  more elongated in the y-direction
- :code:`r`: The "radius" of the ellipse, larger values makes the ellipse
  larger overall

