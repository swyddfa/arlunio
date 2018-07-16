Stylo
---------

.. list-table::
   :stub-columns: 1

   * - docs
     - |docs|
   * - code
     - |travis| |coveralls| |black|

.. |travis| image:: https://travis-ci.org/alcarney/stylo.svg?branch=develop
    :target: https://travis-ci.org/alcarney/stylo

.. |docs| image:: https://readthedocs.org/projects/stylo/badge/?version=develop
    :target: http://stylo.readthedocs.io/en/develop/?badge=develop
    :alt: Documentation Status

.. |coveralls| image:: https://coveralls.io/repos/github/alcarney/stylo/badge.svg?branch=develop
    :target: https://coveralls.io/github/alcarney/stylo?branch=develop

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

**DISCLAIMER!: Stylo is still in its very early stages, many of the core
concepts are yet to be decided on. The interface can change without warning or
features be added and removed entirely!**

Stylo is a library that attempts to allow users to easily describe the
contents of an image using a blend of Python and Mathematics. It also provides
tools that allow for easy parameterisation of the contents of an image opening
up the possibilities for the creation of animations.

One of the design goals is to minimise the amount of code needed from the user
to achieve the desired result.

Requirements
------------

This framework is Python 3 only, and has the following dependencies:

- Numpy
- Scipy
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
