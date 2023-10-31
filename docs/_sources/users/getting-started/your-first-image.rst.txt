.. _users_getting_started_first_image:

Your First Image
================

.. nbtutorial::

Drawing an image with :code:`arlunio` can be as simple as a few lines of
code::

   import arlunio as ar
   from arlunio.lib import Circle

   circle = Circle()
   ar.fill(circle(width=1920, height=1080), color="red")

.. only:: html

   .. arlunio-image::

      from arlunio.lib.mask import Circle
      from arlunio.lib.image import fill

      circle = Circle()
      image = fill(circle(width=1920, height=1080), color="red")
