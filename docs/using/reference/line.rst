.. _use_ref_shape_line:

Line
====

Default Behavior
----------------

By default drawing a :code:`Line` without any arguments will draw a line segment
connecting the points :math:`(0, 0)` and :math:`(0, 1)`

.. stylo-image::
   :align: center
   :img-width: 1920
   :img-height: 1080
   :include-code:
   :display-width: 75%

   from stylo.color import FillColor
   from stylo.shape import Line
   from stylo.image import SimpleImage

   color = FillColor()
   line = Line()

   image = SimpleImage(line, color)

Line Properties
---------------

You can control various aspects of the line using the following arguments

- :code:`p1, p2` control the points that the line is drawn between
- :code:`extend` this can be used to extend the line drawn off to infinity

.. stylo-image::
   :align: center
   :img-width: 1920
   :img-height: 1080
   :include-code:
   :display-width: 75%

   from stylo.color import FillColor
   from stylo.shape import Line
   from stylo.image import LayeredImage

   color = FillColor()

   flat_line = Line(p1=(0,0), p2=(1, 0), extend=True)
   shallow_line = Line(p1=(-0.5, -0.4), p2=(0.5, -0.2))
   steep_line = Line(p1=(0.1, 0.1), p2=(0.2, 0.9))

   image = LayeredImage()
   image.add_layer(flat_line, color)
   image.add_layer(shallow_line, color)
   image.add_layer(steep_line, color)

.. note::

   As you can see in the image above there is currently a limitation with the
   :code:`Line` shape where the steeper the line, the thinner it gets. It is
   also impossible to draw vertical lines.

   There is however a workaround where you can draw a flat line and use the
   :code:`rotate` transform to angle it to the desired slope.

.. stylo-image::
   :align: center
   :img-width: 1920
   :img-height: 1080
   :include-code:
   :display-width: 75%

   import numpy as np 
   from math import pi 

   from stylo.domain.transform import rotate
   from stylo.color import FillColor
   from stylo.shape import Line
   from stylo.image import LayeredImage

   color = FillColor()
   image = LayeredImage()

   for angle in np.linspace(0, 2*pi, 12, endpoint=False):
       line = Line(p1=(0.2, 0), p2=(0.6, 0)) >> rotate(angle)
       image.add_layer(line, color)

Drawing Options
---------------

You can also control how the line is drawn using the following options.

- :code:`pt` will control the thickness of the line
- :code:`above` will shade in the area above the line
- :code:`below` will shade in the area below the line

.. stylo-image::
   :align: center
   :img-width: 1920
   :img-height: 1080
   :include-code:
   :display-width: 75%

   from stylo.color import FillColor
   from stylo.shape import Line
   from stylo.image import LayeredImage

   color = FillColor()

   line = Line(p1=(0,0), p2=(1,-1), extend=True, pt=0.2)
   left_area = Line(p1=(-0.75, 0), p2=(0.25, -1), extend=True, below=True)
   right_area = Line(p1=(0.75, 0), p2=(1.75, -1), extend=True, above=True)

   image = LayeredImage()
   image.add_layer(line, color)
   image.add_layer(left_area, color)
   image.add_layer(right_area, color)