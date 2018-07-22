Stylo
-----

.. list-table::
   :stub-columns: 1

   * - docs
     - |docs|
   * - code
     - |travis| |coveralls| |black|
   * - pypi
     - |version| |supported-versions|

.. |travis| image:: https://travis-ci.org/alcarney/stylo.svg?branch=develop
    :target: https://travis-ci.org/alcarney/stylo

.. |docs| image:: https://readthedocs.org/projects/stylo/badge/?version=develop
    :target: http://stylo.readthedocs.io/en/develop/?badge=develop
    :alt: Documentation Status

.. |coveralls| image:: https://coveralls.io/repos/github/alcarney/stylo/badge.svg?branch=develop
    :target: https://coveralls.io/github/alcarney/stylo?branch=develop

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

.. |version| image:: https://img.shields.io/pypi/v/stylo.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/stylo

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/stylo.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/stylo

**DISCLAIMER!: Stylo is still in its very early stages, many of the core
concepts are yet to be decided on. The interface can change without warning or
features be added and removed entirely!**

Stylo is a library that attempts to allow users to easily describe the
contents of an image using a blend of Python and Mathematics. It also provides
tools that allow for easy parameterisation of the contents of an image opening
up the possibilities for the creation of animations.

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
