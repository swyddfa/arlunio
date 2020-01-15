.. _using_tutorial_getstarted_part1:

Shapes and Images
=================

.. nbtutorial::

In this tutorial we start you off by introducing you to the two main types of
object you will find in :code:`stylo` as well as how to use them to create your
first image. The first of these objects are the :code:`Shapes`.

:code:`Shapes` define the rules that are used to contruct our second kind of
object :code:`Images`. An :code:`Image` contains the raw image data that we can
manipulate before saving it as a file. :code:`Images` are typically constructed
using one or more shapes.

Let's show you what I mean, first import the Shapes collection and create an
instance of the :code:`Circle` shape.

.. doctest::

   >>> from arlunio import Shapes as S
   >>> circle = S.Circle()
   >>> circle
   Circle(x0=0, y0=0, r=0.8, pt=None)

As you can see each shape can carry its own set of properties that can be
tweaked to change how it looks when it is drawn. For now don't worry about them
too much as we will get to look at those in more detail later. Instead let's
focus on making our first image!

Every shape instance can be called as a function and will return an image
contiaing itself, all we need to do is tell it how large we want the image to
be!

.. doctest::

   >>> circle(4, 4)  # doctest: +SKIP


.. only:: html

   .. arlunio-image::

      from arlunio import Shapes as S

      circle = S.Circle()
      image = circle(4, 4)
