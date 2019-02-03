.. _extend_source:

Sources
=======

|Source| objects are primarily used by Image objects to generate the data that
is used to draw an image with. In the case of the standard images in stylo this
is coordinate data that shapes such as circles are defined against.

A :code:`Source` is a collection of variables that are represented by
|Tweakables|.  These variables are defined either with respect to some common
arguments (like :code:`width` and :code:`height`) or some existing variables.

Perhaps the best way to explain how :code:`Source` objects are used is to walk
through the process of defining and using one. As an example we will build up a
:code:`Source` object similar to the one that is built into the standard images
that come with stylo.

.. _extend_source_create:

Creating a Source
-----------------

When creating a new :code:`Source` object you must specify the names of the
arguments that you expect users of the source to provide when using it. For
example in the case of the standard source these arguments are the
:code:`width` and :code:`height` of the image::

   >>> import stylo as st
   >>> source = st.Source('width', 'height', name="Variables")



