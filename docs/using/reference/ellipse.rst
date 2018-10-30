.. _use_ref_shape_ellipse:

Ellipse
=======

Default Behavior
----------------

By default drawing an :code:`Ellipse` without any arguments will only
draw the outline of the ellipse.

.. stylo-image:: 
   :align: center
   :img-width: 1920
   :img-height: 1080
   :include-code:
   :display-width: 75%

   from stylo.color import FillColor
   from stylo.shape import Ellipse
   from stylo.image import SimpleImage

   color = FillColor()
   ellipse = Ellipse()

   image = SimpleImage(ellipse, color)

Ellipse Properties
------------------

You can control various aspects of the ellipse using the following arguments

- :code:`x, y` will control the position of the ellipse
- :code:`a, b` can be used to control the ellipse's proportions
- :code:`r` controls the overall size of the ellipse

.. stylo-image::
   :align: center
   :img-width: 1920
   :img-height: 1080
   :include-code:
   :display-width: 75%

   from stylo.color import FillColor
   from stylo.shape import Ellipse
   from stylo.image import LayeredImage

   color = FillColor()

   left_ellipse = Ellipse(x=-1, y=0.3, a=1, b=1, r=0.4)
   middle_ellipse = Ellipse(x=-0.4, y=-0.25, a=1, b=2, r=0.2)
   right_ellipse = Ellipse(x=0.6, y=0.4, a=2, b=1, r=0.5)

   image = LayeredImage()
   image.add_layer(left_ellipse, color)
   image.add_layer(middle_ellipse, color)
   image.add_layer(right_ellipse, color)

The above image should give you an idea about the relationship between the prarmeters
:code:`a` and :code:`b`.

- When :code:`a = b` we get a circle
- When :code:`a > b` the ellipse is wider and shorter
- When :code:`a < b` the ellipse is narrower and taller

Drawing Options
---------------

You can also control how the ellipse is drawn using the :code:`pt` and :code:`fill`
arguments

- :code:`pt` controls the thickness of the line used to draw the ellipse
- :code:`fill` switches the ellipse from being drawn with a line to a shaded area

.. stylo-image::
   :align: center
   :img-width: 1920
   :img-height: 1080
   :include-code:
   :display-width: 75%

   from stylo.color import FillColor
   from stylo.shape import Ellipse
   from stylo.image import LayeredImage

   color = FillColor()
   inner_ellipse = Ellipse(a=1, b=2, r=0.2, fill=True)
   outer_ellipse = Ellipse(a=2, b=1, r=0.6, pt=0.2)

   image = LayeredImage()
   image.add_layer(inner_ellipse, color)
   image.add_layer(outer_ellipse, color)