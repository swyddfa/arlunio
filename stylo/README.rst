Stylo
---------

Stylo is a framework that attempts to allow users to easily describe the
contents of an image using a blend of Python and Mathematics. It also provides
tools that allow for easy parameterisation of the contents of an image opening
up the possibilities for the creation of animations.

One of the design goals is to minimise the amount of code needed from the user
to achieve the desired result.

Requirements
------------

This framework is Python 3 only, and has the following dependencies:

- Numpy
- Pillow
- Matplotlib


Installation
------------

Stylo is available on PyPi and can easily be installed using Pip:

.. code::

    $ pip install stylo

Alternatively you can grab the latest source code using Git:

.. code::

    $ git clone https://github.com/alcarney/stylo


Getting Started
---------------

Once installed it's relatively straightforward to get started - provided you
are familiar with a few concepts from mathematics such as Cartesian and Polar
coordinates.

Here is a 'Hello World' example where we draw Pacman::

.. code::

    from stylo import Image, cartesian, polar, between

    @cartesian()
    @polar()
    def pacman(x, y, r, t):
        return r <= 0.8 and not between(-0.6, t, 0.6)

    @pacman.colormap
    def color():
    return (255, 255, 0)

    img = Image(512, 512)
    img(pacman)
    img.save('pacman.png')

<Insert nice explanation here>
