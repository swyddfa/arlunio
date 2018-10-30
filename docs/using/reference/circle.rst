.. _use_ref_shape_circle:

Circle 
======

Default Behavior
----------------

By default drawing a :code:`Circle` without any arguments will only draw the outline of
the circle.

.. stylo-image::
   :align: center
   :img-width: 1920
   :img-height: 1080
   :include-code:
   :display-width: 75%

   from stylo.color import FillColor
   from stylo.shape import Circle
   from stylo.image import SimpleImage

   color = FillColor()
   circle = Circle()

   image = SimpleImage(circle, color)

Circle Properties
-----------------

You can control the size and position of the circle by making use of the
:code:`(x, y, r)` arguments

.. stylo-image::
   :align: center
   :img-width: 1920
   :img-height: 1080
   :include-code:
   :display-width: 75%

   from stylo.color import FillColor
   from stylo.shape import Circle
   from stylo.image import LayeredImage

   color = FillColor()
   left_circle = Circle(x=-0.5, y=-0.25, r=0.25)
   right_circle = Circle(x=0.5, y=0.2, r=0.75)

   image = LayeredImage()
   image.add_layer(left_circle, color)
   image.add_layer(right_circle, color)

Drawing Options
---------------

You can also control how the circle is drawn by using the :code:`pt` and :code:`fill`
arguments

- :code:`pt` controls the thickness of the line used to draw the circle
- :code:`fill` switches the circle from being drawn with a line to being a
  shaded area.

.. stylo-image::
   :align: center
   :img-width: 1920
   :img-height: 1080
   :include-code:
   :display-width: 75%

   from stylo.color import FillColor
   from stylo.shape import Circle
   from stylo.image import LayeredImage

   color = FillColor()
   inner_circle = Circle(r=0.25, fill=True)
   outer_circle = Circle(r=0.75, pt=0.2)

   image = LayeredImage()
   image.add_layer(inner_circle, color)
   image.add_layer(outer_circle, color)