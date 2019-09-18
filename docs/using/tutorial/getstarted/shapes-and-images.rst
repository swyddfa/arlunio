.. _using_tutorial_getstarted_part1:

Shapes and Images
=================

.. nbtutorial::

.. arlunio-image::

   import arlunio as ar

   dice = ar.S.SuperEllipse(n=5, color="#dd0000") + ar.S.SuperEllipse(n=5, pt=0.05)
   dice += ar.S.Circle(r=0.45, color="#ffffff")
   dice += ar.S.Circle(r=0.45, color="#ffffff", x0=0.5, y0=-0.5)
   dice += ar.S.Circle(r=0.45, color="#ffffff", x0=-0.5, y0=0.5)

   image = dice(1920, 1080)

In this tutorial we introduce the two main types of object you will find in
arlunio, :code:`Shapes` and :code:`Images` and how they can be used to create
your first image.

A :code:`Shape` represents something that can be drawn and provides a number of
options that control how it appears. Once drawn, a shape, or collection of
shapes produce an :code:`Image` which holds the raw pixel data that we will
eventually save to a file.

To get started let's create an instance of a :code:`Circle` and draw it by
giving it the dimensions we want the resulting image to have.

.. doctest:: shapes-and-images

   >>> import arlunio as ar
   >>> circle = ar.S.Circle()
   >>> circle(4, 4)  # doctest: +SKIP

.. only:: html

   .. arlunio-image::

      import arlunio as ar

      circle = ar.S.Circle()
      image = circle(4, 4)

Hmm that doesn't look much like a circle... ah yes almost forgot! Image sizes in
:code:`arlunio` are given in pixels. Try it yourself, create a high definition
version of our circle. *Hint high definition is 1920x1080 pixels*

.. nbsolution::

   .. doctest:: shapes-and-images

      >>> circle(1920, 1080)  # doctest: +SKIP

   .. only:: html

      .. arlunio-image::

         import arlunio as ar

         circle = ar.S.Circle()
         image = circle(1920, 1080)


As mentioned above a shape provides a number of options called properties that
can be changed to control how it looks when it is drawn. Let's take a closer
look at that circle object we just created.

.. doctest:: shapes-and-images

   >>> circle
   Circle(x0=0, y0=0, r=0.8, pt=None)

You can see each of the
