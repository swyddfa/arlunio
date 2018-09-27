.. _use_tutorial_basics_1:

An Introduction To Stylo - Part 1
=================================

Stylo is a package that enables you to create images through the use of
mathematical functions and basic shapes. This is done via a two step process:

        - Define a shape
        - Set a colour

But how?

Defining Our Shape
------------------

We now need to define the shape we intend to draw. We will need to import the
Rectangle shape from the shape library. We then create our rectangle at
coordinates (0,0) and with width=1, height=1.

.. doctest:: use_tutorial_basics

  >>> from stylo.shape import Rectangle
  >>> shape = Rectangle(0, 0, 1, 1)

Defining Our Colour
-------------------

Finally, we need to define the colour that we wish our shape to be. We import
color from the color library, and use the default fill colour, which will be
black.

.. doctest:: use_tutorial_basics

   >>> from stylo.color import FillColor
   >>> color = FillColor()

Creating Our Image
------------------

To display our image, we import the SimpleImage from the image library, and
pass it our two parameters.

.. doctest:: use_tutorial_basics

   >>> from stylo.image import SimpleImage
   >>> image = SimpleImage( shape, color)

Saving Our Image
----------------

The following saves our image with size 1024x1024px in the current directory as
myImage.png.

.. code-block:: python

   >>> image(1024, 1024, filename="myImage.png")

Congratulations, you have created your first image in stylo!
