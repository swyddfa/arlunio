.. _stdlib_image:

Image
=====

.. currentmodule:: arlunio.image

This module wraps various parts of the :doc:`pillow:index` image library to better
integrate it with other components of :code:`arlunio` in order to help produce and
manipulate images that can be saved eventually to disk.

Creating Images
---------------

.. autofunction:: new

.. autofunction:: fromarray


Image I/O
---------

.. autofunction:: encode

.. autofunction:: decode

.. autofunction:: load

.. autofunction:: save


Manipulating Images
-------------------

.. autofunction:: colorramp

.. autofunction:: fill

.. autoclass:: Image
