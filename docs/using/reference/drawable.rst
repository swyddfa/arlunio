Drawable
========


Overview
--------

A Drawable is the abstract representation of a shape or texture that can be
mapped onto an `Image`_ and it is made up of 3 main parts:

- A Domain
- A Mask Function
- A Color Function

The **Domain** is the mathematical space upon which the shape is defined for
example the :math:`xy`-plane with :math:`x` and :math:`y` taking values between
zero and one. In this library a domain is represented by a function in the
:code:`width` and :code:`height` that returns a numpy meshgrid which associates
pixels in the Image with points in the mathematical domain. Typically domains
are constructed with the :code:`mk_domain` function:

The **Mask Function** is a function defined on the mathematical domain, taking
values :code:`(x, y)` and is responsible for determining which points in the
domain form part of the shape and returning :code:`True` when this is the case.

The **Color Function** is a function also defined on the mathematical domain,
but is only called on points that are in the shape and determines the colour
that should be assigned to each point

Creation
--------

Drawables can be created directly as you would any class in Python and you can
optionally pass in :code:`domain`, :code:`mask` and :code:`color` parameters,
or use the properties outlined below. So for example if we wanted to create a
checkerboard pattern we can do the following

.. code-block:: python

    import numpy as np
    from stylo.coords import Drawable

    def domain_func(width, height):
        xs = np.linspace(-1, 1, width)
        ys = np.linspace(1, -1, height)

        return np.meshgrid(xs, ys)

    def mask_func(x, y):
        return x * y >= 0

    def color_func():
        return (0, 0, 0, 255)

    checker = Drawable(domain=domain_func, mask=mask_func, color=color_func,
                       name="checker")

However there is also a :code:`cartesian` decorator we can use to take care of
a lot of the boilerplate for us, the following block of code produces the same
result

.. code-block:: python

    from stylo import cartesian

    @cartesian(X=[-1, 1], Y=[-1, 1])
    def checker(x, y):
        return x * y >= 0

The :code:`cartesian` decorator automatically handles the creation of the
domain function based on the values given in the :code:`X` and :code:`Y`
arguments. The mask function is the function we defined as :code:`checker` and
we are taking advantage of the fact that the default color Drawables use if no
colour is provided is black.

Due to the less verbose nature of this method it is the recommended way of
creating Drawables.


Properties
----------

Name
^^^^

The :code:`name` property allows you to assign a name to a Drawable

Domainfunc
^^^^^^^^^^

The :code:`domainfunc` property returns the current domain associated with the
Drawable. If no domain has been assigned to it, then it defaults to the domain
:math:`[-1, 1] \times [-1, 1]`. This property can also be used to change the
domain.

Drawables also have a :code:`domain` method which supports decorator syntax to
streamline the creation and assignment of new domain functions. For example if
we wanted to change the default domain, to a domain defined on
:math:`[0, 2] \times [0, 2]` we can do the following

.. code-block:: python

    from stylo.coords import Drawable
    import numpy as np

    circle = Drawable()

    @circle.domain
    def new_domain(width, height):
        xs = np.linspace(0, 2, width)
        ys = np.linspace(2, 0, height)

        return np.meshgrid(xs, ys)

Maskfunc
^^^^^^^^

The :code:`maskfunc` property returns the mask function defined for the
Drawable. If no mask function has been defined then a default function that
returns :code:`True` for any point in the domain. This property can also be
used to alter the mask function.

Drawables also have a :code:`mask` method which supports decorator syntax to
streamline the creation and assignment of a new mask function. Continuing with
the example above if we wanted to change the mask function to represent a
circle centered at the origin :math:`(0, 0)` with radius 1 then we can do the
following

.. code-block:: python

    from math import sqrt

    @circle.mask
    def new_mask(x, y):
        r = sqrt(x**2 + y**2)
        return r <= 1

Colorfunc
^^^^^^^^^

The :code:`colorfunc` property returns the color function defined for the
Drawable. If no color function has been defined then a default function that
returns black for every point is returned. This property can also be used to
alter the color function.

Drawables also have a :code:`colormap` method that supports decorator syntax to
streamline the creation and assignment of a new color function. Carrying on
with the earlier example if we wanted the inner half of the circle to be
coloured red and the outer half to be coloured green then we can do the
following

.. code-block:: python

    @circle.colormap
    def new_color(x, y):
        r = sqrt(x**2 + y**2)

        if r <= 0:
            return np.array([255, 0, 0, 255])
        else:
            return np.array([0, 255, 0, 255])

Now there is a trick that can be done to optimize the color function. If you
are going to colour the shape with a single colour - i.e. the colour doesn't
depend on the values of :code:`x` and :code:`y` then if you define the color
function with no arguments then the Drawable can optimize things behind the
scenes and speed up your code. For example, say instead we wanted to colour the
entire circle blue the we can do the following

.. code-block:: python

    @circle.colormap
    def new_color():
        return (0, 0, 255, 255)

Decorators
----------

Along with the :code:`cartesian` decorator mentioned above, there are a few
other decorators that allow you to modify the mask function in a number of ways

Extend Periodically
^^^^^^^^^^^^^^^^^^^

This is useful for defining repeating patterns - like a checker board. If we
look at the checkerboard we defined above

.. table::
    :class: borderless

    +----------------------------------------------------------+-----------------------------------------------------+
    | .. code-block:: python                                   | .. image:: /_static/reference/drawable/checker.png  |
    |                                                          |      :width: 95%                                    |
    |   from stylo import Image, cartesian                     |      :align: center                                 |
    |                                                          |                                                     |
    |   @cartesian()                                           |                                                     |
    |   def checker(x, y):                                     |                                                     |
    |       return x * y >=0                                   |                                                     |
    |                                                          |                                                     |
    |   img = Image(512, 512, background=(128, 128, 128, 255)) |                                                     |
    |   img(checker)                                           |                                                     |
    |   img.save('checker.png')                                |                                                     |
    +----------------------------------------------------------+-----------------------------------------------------+

Now if we wanted this pattern to repeat, we could try and mess with the
definition above or we could simply ask the pattern we've already defined to
repeat. This is where the :code:`extend_periodically` decorator comes in. We
can define the drawable over a larger domain :math:`[-4, 4] \times [-4, 4]`
and telling the :code:`extend_periodically` that the pattern is defined over
:math:`[-1, 1] \times [-1, 1]` it will repeat the pattern for us

.. table::
    :class: borderless

    +-----------------------------------------------------------+--------------------------------------------------------------+
    | .. code-block:: python                                    |  .. image:: /_static/reference/drawable/checker-extended.png |
    |                                                           |      :width: 95%                                             |
    |   from stylo import Image, cartesian, extend_periodically |      :align: center                                          |
    |                                                           |                                                              |
    |   @cartesian(X=[-4, 4], Y=[-4, 4])                        |                                                              |
    |   @extend_periodically(X=[-1, 1], Y=[-1, 1])              |                                                              |
    |   def checker(x, y):                                      |                                                              |
    |       return x * y >= 0                                   |                                                              |
    |                                                           |                                                              |
    |   img = Image(512, 512, background=(128, 128, 128, 255))  |                                                              |
    |   img(checker)                                            |                                                              |
    |   img.save('checker-extended.png')                        |                                                              |
    +-----------------------------------------------------------+--------------------------------------------------------------+

Translate
^^^^^^^^^

Sometimes you want to move or rotate your shapes there are a number of ways to
do this, one of them is the :code:`translate` decorator. It takes two
arguments:

- :code:`X`: A list of two elements :code:`[dx, dy]` - how far you want to move
  in the :math:`x` and :math:`y` directions respectively
- :code:`r`: A float, representing the angle you wish to rotate the shape by -
  measured in `radians`_

It might be best to give a few examples so consider the following parabolic
shapes and the code to generate them

.. table::
    :class: borderless

    +--------------------------------------------------+----------------------------------------------------------+
    | .. code-block:: python                           | .. image:: /_static/reference/drawable/parabola.png      |
    |                                                  |       :width: 95%                                        |
    |   from stylo import Image, cartesian             |       :align: center                                     |
    |                                                  |                                                          |
    |   @cartesian()                                   |                                                          |
    |   def shape(x, y):                               |                                                          |
    |       return y < x**2 + 0.05 and y > x**2 - 0.05 |                                                          |
    |                                                  |                                                          |
    |   img = Image(512, 512)                          |                                                          |
    |   img(shape)                                     |                                                          |
    |   img.save('parabola.png')                       |                                                          |
    |                                                  |                                                          |
    | **Original**                                     |                                                          |
    +--------------------------------------------------+----------------------------------------------------------+
    | .. code-block:: python                           | .. image:: /_static/reference/drawable/parabola-dx.png   |
    |                                                  |       :width: 95%                                        |
    |   from stylo import Image, cartesian, translate  |       :align: center                                     |
    |                                                  |                                                          |
    |   @cartesian()                                   |                                                          |
    |   @translate(X=[1, 0])                           |                                                          |
    |   def shape(x, y):                               |                                                          |
    |       return y < x**2 + 0.05 and y > x**2 - 0.05 |                                                          |
    |                                                  |                                                          |
    |   img = Image(512, 512)                          |                                                          |
    |   img(shape)                                     |                                                          |
    |   img.save('parabola-dx.png')                    |                                                          |
    |                                                  |                                                          |
    | **Translation along x-axis**                     |                                                          |
    +--------------------------------------------------+----------------------------------------------------------+
    | .. code-block:: python                           | .. image:: /_static/reference/drawable/parabola-dy.png   |
    |                                                  |       :width: 95%                                        |
    |   from stylo import Image, cartesian, translate  |       :align: center                                     |
    |                                                  |                                                          |
    |   @cartesian()                                   |                                                          |
    |   @translate(X=[0, 1])                           |                                                          |
    |   def shape(x, y):                               |                                                          |
    |       return y < x**2 + 0.05 and y > x**2 - 0.05 |                                                          |
    |                                                  |                                                          |
    |   img = Image(512, 512)                          |                                                          |
    |   img(shape)                                     |                                                          |
    |   img.save('parabola-dx.png')                    |                                                          |
    |                                                  |                                                          |
    | **Translation along y-axis**                     |                                                          |
    +--------------------------------------------------+----------------------------------------------------------+
    | .. code-block:: python                           | .. image:: /_static/reference/drawable/parabola-r.png    |
    |                                                  |       :width: 95%                                        |
    |   from stylo import Image, cartesian, translate  |       :align: center                                     |
    |   from math import pi                            |                                                          |
    |                                                  |                                                          |
    |   @cartesian()                                   |                                                          |
    |   @translate(r=pi/4)                             |                                                          |
    |   def shape(x, y):                               |                                                          |
    |       return y < x**2 + 0.05 and y > x**2 - 0.05 |                                                          |
    |                                                  |                                                          |
    |   img = Image(512, 512)                          |                                                          |
    |   img(shape)                                     |                                                          |
    |   img.save('parabola-r.png')                     |                                                          |
    |                                                  |                                                          |
    | **Rotated by** :math:`\pi/4` **(45 degrees)**    |                                                          |
    +--------------------------------------------------+----------------------------------------------------------+
    | .. code-block:: python                           | .. image:: /_static/reference/drawable/parabola-dX-r.png |
    |                                                  |       :width: 95%                                        |
    |   from stylo import Image, cartesian, translate  |       :align: center                                     |
    |   from math import pi                            |                                                          |
    |                                                  |                                                          |
    |   @cartesian()                                   |                                                          |
    |   @translate(X=[1, 1], r=pi/4)                   |                                                          |
    |   def shape(x, y):                               |                                                          |
    |       return y < x**2 + 0.05 and y > x**2 - 0.05 |                                                          |
    |                                                  |                                                          |
    |   img = Image(512, 512)                          |                                                          |
    |   img(shape)                                     |                                                          |
    |   img.save('parabola-dX-r.png')                  |                                                          |
    |                                                  |                                                          |
    | **Translation and Rotation**                     |                                                          |
    +--------------------------------------------------+----------------------------------------------------------+
    | .. code-block:: python                           | .. image:: /_static/reference/drawable/parabola-r-dX.png |
    |                                                  |       :width: 95%                                        |
    |   from stylo import Image, cartesian, translate  |       :align: center                                     |
    |   from math import pi                            |                                                          |
    |                                                  |                                                          |
    |   @cartesian()                                   |                                                          |
    |   @translate(X=[1, 1])                           |                                                          |
    |   @translate(r=pi/4)                             |                                                          |
    |   def shape(x, y):                               |                                                          |
    |       return y < x**2 + 0.05 and y > x**2 - 0.05 |                                                          |
    |                                                  |                                                          |
    |   img = Image(512, 512)                          |                                                          |
    |   img(shape)                                     |                                                          |
    |   img.save('parabola-r-dX.png')                  |                                                          |
    |                                                  |                                                          |
    | **Rotation then Translation**                    |                                                          |
    +--------------------------------------------------+----------------------------------------------------------+

Reflect
^^^^^^^

The :code:`reflect` decorator allows you to reflect a design across either the
:math:`x`-axis, the :math:`y`-axis or both.

.. table::
    :class: borderless

    +-----------------------------------------------+------------------------------------------------------+
    | .. code-block:: python                        | .. image:: /_static/reference/drawable/circle.png    |
    |                                               |    :width: 95%                                       |
    |   from math import sqrt                       |    :align: center                                    |
    |   from stylo import Image, cartesian, reflect |                                                      |
    |                                               |                                                      |
    |   @cartesian()                                |                                                      |
    |   def shape(x, y):                            |                                                      |
    |       r = sqrt((x - 0.5)**2 + (y - 0.5)**2)   |                                                      |
    |       return r <= 0.4                         |                                                      |
    |                                               |                                                      |
    |   img = Image(512, 512)                       |                                                      |
    |   img(shape)                                  |                                                      |
    |   img.save('circle.png')                      |                                                      |
    |                                               |                                                      |
    | **Original Design**                           |                                                      |
    +-----------------------------------------------+------------------------------------------------------+
    | .. code-block:: python                        | .. image:: /_static/reference/drawable/circle-X.png  |
    |                                               |    :width: 95%                                       |
    |   from math import sqrt                       |    :align: center                                    |
    |   from stylo import Image, cartesian, reflect |                                                      |
    |                                               |                                                      |
    |   @cartesian()                                |                                                      |
    |   @reflect(X=True)                            |                                                      |
    |   def shape(x, y):                            |                                                      |
    |       r = sqrt((x - 0.5)**2 + (y - 0.5)**2)   |                                                      |
    |       return r <= 0.4                         |                                                      |
    |                                               |                                                      |
    |   img = Image(512, 512)                       |                                                      |
    |   img(shape)                                  |                                                      |
    |   img.save('circle-X.png')                    |                                                      |
    |                                               |                                                      |
    | **Reflected about the** :math:`x` **axis**    |                                                      |
    +-----------------------------------------------+------------------------------------------------------+
    | .. code-block:: python                        | .. image:: /_static/reference/drawable/circle-Y.png  |
    |                                               |    :width: 95%                                       |
    |   from math import sqrt                       |    :align: center                                    |
    |   from stylo import Image, cartesian, reflect |                                                      |
    |                                               |                                                      |
    |   @cartesian()                                |                                                      |
    |   @reflect(Y=True)                            |                                                      |
    |   def shape(x, y):                            |                                                      |
    |       r = sqrt((x - 0.5)**2 + (y - 0.5)**2)   |                                                      |
    |       return r <= 0.4                         |                                                      |
    |                                               |                                                      |
    |   img = Image(512, 512)                       |                                                      |
    |   img(shape)                                  |                                                      |
    |   img.save('circle-Y.png')                    |                                                      |
    |                                               |                                                      |
    | **Reflected about the** :math:`y` **axis**    |                                                      |
    +-----------------------------------------------+------------------------------------------------------+
    | .. code-block:: python                        | .. image:: /_static/reference/drawable/circle-XY.png |
    |                                               |    :width: 95%                                       |
    |   from math import sqrt                       |    :align: center                                    |
    |   from stylo import Image, cartesian, reflect |                                                      |
    |                                               |                                                      |
    |   @cartesian()                                |                                                      |
    |   @reflect(X=True, Y=True)                    |                                                      |
    |   def shape(x, y):                            |                                                      |
    |       r = sqrt((x - 0.5)**2 + (y - 0.5)**2)   |                                                      |
    |       return r <= 0.4                         |                                                      |
    |                                               |                                                      |
    |   img = Image(512, 512)                       |                                                      |
    |   img(shape)                                  |                                                      |
    |   img.save('circle-XY.png')                   |                                                      |
    |                                               |                                                      |
    | **Reflected about both axes**                 |                                                      |
    +-----------------------------------------------+------------------------------------------------------+

Polar
^^^^^

The :code:`polar` decorator allows you to define your shape with respect to
`Polar Coordinates`_ which is useful when working with shapes that are not
easily defined on a rectangular grid. For example to define a disk centered at
:math:`(0, 0)` with radius :math:`1` using standard `Cartesian Coordinates`_
you need to find points :math:`(x, y)` such that

.. math::

    \sqrt{x^2 + y^2} \leq 1

Whereas the same disk in polar coordinates is as simple as all points
:math:`(r, t)` such that

.. math::

    r \leq 1

To use the polar decorator you just have to define your mask function to take 4
arguments :code:`(x, y, r, t)` where :code:`x, y` are the standard cartesian
coordinates, :code:`r` is the distance from the origin and :code:`t` is the
angle in radians around from the line :math:`y = 0, x \geq 0`

For example if we wanted to draw Pacman, this becomes quite straight forward
when using this decorator

.. table::
    :class: borderless

    +--------------------------------------------------------+---------------------------------------------------+
    | .. code-block:: python                                 | .. image:: /_static/reference/drawable/pacman.png |
    |                                                        |    :width: 95%                                    |
    |   from stylo import Image, cartesian, polar            |    :align: center                                 |
    |                                                        |                                                   |
    |   @cartesian()                                         |                                                   |
    |   @polar()                                             |                                                   |
    |   def pacman(x, y, r, t):                              |                                                   |
    |       return r <= 0.8 and not (t >= -0.6 and t <= 0.6) |                                                   |
    |                                                        |                                                   |
    |   @pacman.colormap                                     |                                                   |
    |   def color():                                         |                                                   |
    |       return (255, 255, 0)                             |                                                   |
    |                                                        |                                                   |
    |   img = Image(512, 512)                                |                                                   |
    |   img(pacman)                                          |                                                   |
    |   img.save('pacman.png')                               |                                                   |
    +--------------------------------------------------------+---------------------------------------------------+

.. _Cartesian Coordinates: https://en.wikipedia.org/wiki/Cartesian_coordinate_system
.. _Image: ./image.html
.. _Polar Coordinates: https://en.wikipedia.org/wiki/Polar_coordinate_system
.. _radians: https://en.wikipedia.org/wiki/Radian
