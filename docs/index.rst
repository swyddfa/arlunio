
.. The code below won't show up on the page, but it will be run as part of the doctests
   to ensure that is works.

.. testsetup:: readme-eye

   from stylo.image import LayeredImage
   from stylo.color import FillColor
   from stylo.shape import Circle

   outer_eye = Circle(0, 0.5, 1) & Circle(0, -0.5, 1)
   inner_eye = Circle(0, 0.5, .9) & Circle(0, -0.5, 0.9)
   eye = outer_eye & ~inner_eye

   iris = Circle(0, 0, 0.4)
   pupil = Circle(0, 0, 0.15)

   blue = FillColor("0000ff")
   black = FillColor("000000")

   image = LayeredImage(scale=1.5)

   image.add_layer(iris, blue)
   image.add_layer(pupil, black)
   image.add_layer(eye, black)

   image(1920, 1080, filename="docs/_static/examples/readme-eye.png")

.. include:: ../README.rst

Be sure to check out the :ref:`about_docs` page for a guide on how to get the most of
the documentation!


Contents
^^^^^^^^

.. toctree::
   :maxdepth: 2

   using/index
   extending/index
   contributing/index
   maths/index
   api/index
   glossary
   changes
   about




