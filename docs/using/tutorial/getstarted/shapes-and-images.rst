.. _using_tutorial_getstarted_part1:

Shapes and Images
=================

.. nbtutorial::

In this tutorial we introduce the two main types of object you will find in
arlunio, :code:`Shapes` and :code:`Images` and how they can be used to create
your first image.

A :code:`Shape` represents a shape that can be drawn and provides a number of
options that control how it is drawn. Once drawn a shape, or collection of
shapes produce an :code:`Image` which holds the raw pixel data that we will
eventually save to a file.

To get started let's create an instance of a :code:`Circle`.

.. doctest:: shapes-and-images

   >>> import arlunio as ar
   >>> circle = ar.S.Circle()
   >>> circle
   Circle(x0=0, y0=0, r=0.8, pt=None)

As mentioned above a shape provides a number of options called properties that
can be changed to control how it looks when it is drawn. We will leave these as
they are for now and let's focus on turning our shape into an image

Every shape in arlunio can be called like a function and will return an image
representing itself, all we need to do is tell it how large we want the image to
be

.. doctest:: shapes-and-images

   >>> circle(4, 4)  # doctest: +SKIP


.. only:: html

   .. arlunio-image::

      import arlunio as ar

      circle = ar.S.Circle()
      image = circle(4, 4)

Ah yes almost forgot, image sizes are given in pixels. Try it yourself, create a
high definition version of the image above. *Hint high definition is 1920x1080
pixels*

.. nbsolution::

   .. doctest:: shapes-and-images

      >>> circle(1920, 1080)  # doctest: +SKIP


Talking 'bout other stuff
