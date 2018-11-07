About
=====

.. list-table::
   :stub-columns: 1

   * - project
     - |license| |gitter|
   * - code
     - |travis| |coveralls| |black|
   * - pypi
     - |version| |supported-versions|

.. |travis| image:: https://travis-ci.org/alcarney/stylo.svg?branch=develop
   :target: https://travis-ci.org/alcarney/stylo

.. |coveralls| image:: https://coveralls.io/repos/github/alcarney/stylo/badge.svg?branch=develop
   :target: https://coveralls.io/github/alcarney/stylo?branch=develop

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black

.. |version| image:: https://img.shields.io/pypi/v/stylo.svg
   :alt: PyPI Package latest release
   :target: https://pypi.org/project/stylo

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/stylo.svg
   :alt: Supported versions
   :target: https://pypi.org/project/stylo

.. |license| image:: https://img.shields.io/github/license/alcarney/stylo.svg
   :alt: License

.. |gitter| image:: https://badges.gitter.im/stylo-py/Lobby.svg
   :alt: Join the chat at https://gitter.im/stylo-py/Lobby
   :target: https://gitter.im/stylo-py/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

**Stylo is in early development, while it is useable we cannot make any
stability guarantees**

Stylo is a Python library that that allows you to create images and animations
powered by your imagination and a little mathematics.  Even though maths is very
much at the core of Stylo you don't have to be a mathematician to use it!

For example here is a simple image of a boat that can be made in a few lines of
Python.

.. stylo-image:: 
   :align: center
   :img-width: 1920
   :img-height: 1080
   :include-code:
   :display-width: 75%

   from stylo.image import LayeredImage
   from stylo.color import FillColor
   from stylo.shape import Circle, Rectangle, Triangle
   from stylo.domain.transform import translate

   # Let's define some colours
   black = FillColor("000000")
   seablue = FillColor("0000ff")
   white = FillColor("ffffff")
   yellow = FillColor("ffff00")
   red = FillColor("dd2300")

   # Now for the shapes we will draw
   sun = Circle(-7, 3.4, 1.5, fill=True)
   sea = Circle(0, -55, 55, fill=True)
   sails = Triangle((0.1, 0.6), (2.5, 0.6), (0.1, 3.5)) | Triangle((-0.1, 0.6), (-1.5, 0.6), (-0.1, 3.5))
   boat = Rectangle(0, 0, 3.5, 1) | Triangle((1.75, -0.5), (1.75, 0.5), (2.25, 0.5))
   mast = Rectangle(0, 2, 0.125, 3)

   # Move some into position
   boat = boat >> translate(0, -2)
   sails = sails >> translate(0, -2)
   mast = mast >> translate(0, -2)

   # Finally let's bring it all together
   image = LayeredImage(background="99ddee", scale=8)

   image.add_layer(sun, yellow)
   image.add_layer(sea, seablue)
   image.add_layer(boat, red)
   image.add_layer(mast, black)
   image.add_layer(sails, white)

Be sure to check out `Stylo Doodles`_ - our community driven example gallery for
plenty of inspiration!

Installation
------------

Stylo is available for Python 3.5+ and can be installed using pip:

.. code-block:: sh

   $ pip install stylo

Be sure to check out the :ref:`use` (under construction) for details on how to
get started. You might also want to read the :ref:`about_docs` page for a quick
overview that aims to help you get the most out of our documentation.

Contributing
------------

Contributions are welcome! Head over to the :ref:`contribute` section to get
started.

.. note::

   If you are looking to contribute **code** to Stylo we do require that you
   have at least Python 3.6 installed due to some of our development
   dependencies requiring more recent versions of Python.


Index
^^^^^

.. toctree::
   :maxdepth: 2

   using/index
   extending/index
   contributing/index
   maths/index
   api/index
   glossary
   changes
   about


.. _Stylo Doodles: https://alcarney.github.io/stylo-doodles
