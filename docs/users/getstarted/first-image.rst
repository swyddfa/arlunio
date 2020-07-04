Your First Image
================

.. arlunio-image:: Sunny Day
   :align: center
   :gallery: examples

   A nice sunny day::

      import arlunio.image as image
      import arlunio.shape as shape

      width, height = 1920, 1080
      img = image.new(width, height, color="lightskyblue")

      sun = shape.Circle(xc=-1.2, yc=0.8, r=0.6)
      img += image.fill(sun(width=width, height=height), foreground="yellow")

      hill = shape.Circle(xc=-1, yc=-2.1, r=1.5)
      img += image.fill(hill(width=width, height=height), foreground="limegreen")

      hill = shape.Circle(xc=1, yc=-1.8, r=1.3)
      img += image.fill(hill(width=width, height=height), foreground="lawngreen")


In this tutorial we will be drawing the image you see above. Along the way
you'll learn some of ways you can create simple images and combine them into a
final composition. Given the visual nature of this library it's recommended
that you follow along using a Jupyter Notebook so that you can see the results
of each step incrementally.

We start off by importing the modules we need.

.. code-block:: python

   import arlunio.image as image
   import arlunio.shape as shape

Next we decide on a resolution at which we want to render our final image at
and create an image containing the background color representing the sky.

.. code-block:: python

   width, height = 1920, 1080
   background = image.new(width, height, color="lightskyblue")

Now we'll create a circle to represent the sun and position it over and up to
the left. To produce an image we can use the :code:`fill` function to color in
the circle with a yellow color.

.. code-block:: python

   sun_shape = shape.Circle(xc=-1.2, yc=0.8, r=0.6)
   sun = image.fill(sun_shape(width=width, height=height), foreground="yellow")

Adding our :code:`background` and :code:`sun` images together we can start
building up our final image - order matters!

.. code-block:: python

   final_image = background + sun

Then following a similar process we can create the two hills and add them onto
the final image.

.. code-block:: python

   hill = shape.Circle(xc=-1, yc=-2.1, r=1.5)
   final_image += image.fill(hill(width=width, height=height), foreground="limegreen")

   hill = shape.Circle(xc=1, yc=-1.8, r=1.3)
   final_image += image.fill(hill(width=width, height=height), foreground="lawngreen")

Congratulations! You've just drawn your first image with :code:`arlunio`! Don't
forget to save it as a PNG so you can share it with all your friends 😃

.. code-block:: python

   final_image.save("sunny-day.png")

Test Your Skills
----------------

As with anything practice makes perfect so we've included a few exercises for
you to try, can you use what you have learned so far to recreate the examples
below?

We have included a solution for each example if you get stuck but keep in mind
that there is no "correct answer". Quite often there are multiple ways to
achieve the same result!

.. arlunio-image:: Sunset
   :gallery: examples
   :include-code: solution

   Sunset::

      import arlunio.image as image
      import arlunio.shape as shape

      w, h = 1920, 1080
      img = image.new(w, h, color="darkorange")

      sun = shape.Circle(xc=-1.2, yc=0, r=0.6)
      img += image.fill(sun(width=w, height=h), foreground="yellow")

      hill = shape.Circle(xc=-1, yc=-2.1, r=1.5)
      img += image.fill(hill(width=w, height=h), foreground="forestgreen")

      hill = shape.Circle(xc=1, yc=-1.8, r=1.3)
      img += image.fill(hill(width=w, height=h), foreground="green")