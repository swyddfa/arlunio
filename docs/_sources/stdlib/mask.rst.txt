.. _stdlib_mask:

Mask
====

.. currentmodule:: arlunio.mask

Masks are 2D boolean numpy arrays which are primarily used to represent selections for
example some region of an image. Masks are typically given to functions like
:func:`arlunio.image.fill` to indicate which regions of an image a particular operation
should affect. This module provides a :class:`Mask` class that builds on a standard
numpy array as well as a number of functions and definitions for manipulating it.

Creating Masks
--------------

.. autofunction:: all_

.. autofunction:: any_

.. autoclass:: Mask

Definitions
-----------

This module also contains a number of definitions that either produce or manipulate
masks in some way

.. list-table:: Summary
   :align: center
   :widths: 10 30

   - * :class:`Empty`
     * Return an empty mask with the given dimensions
   - * :class:`Full`
     * Return a full mask with the given dimensions
   - * :class:`Map`
     * Construct a mask from smaller, simpler masks
   - * :class:`Repeat`
     * Construct a mask by replicating an existing one.
   - * :class:`Pixelize`
     * Enlarge an existing mask, creating a pixelised effect.


Empty
^^^^^

.. autoclass:: Empty

Full
^^^^

.. autoclass:: Full

Map
^^^

.. autoclass:: Map

Repeat
^^^^^^

.. autoclass:: Repeat

Pixelize
^^^^^^^^

.. autoclass:: Pixelize
