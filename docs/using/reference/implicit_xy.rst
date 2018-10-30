.. _use_ref_shape_implicit_xy:

Implicit XY  
===========

Introduction
------------

.. todo::

   Move this exposition into the mathematics section when it has been fleshed out.

Rather than draw a single shape the :code:`ImplicitXY` shape allows you to draw an 
entire familiy of curves. Those that can be defined using the following relation.

.. math::

   f(x, y) = 0

where :math:`x` and :math:`y` are the standard :code:`x, y` coordinates.

A few examples of such shapes include

**A Circle**

.. math::

   f(x, y) = x^2 + y^2 - r^2

**A Straight Line**

.. math::

   f(x, y) = mx + c - y

**A Parabola**

.. math::

   f(x, y) = x^2 - y

The list goes on. However if we were to use the condition :math:`f(x,y) = 0` to
define our curves we would never see them as curves have no area. Instead we
artificially give our curves some area so that we can draw them with stylo.

We do this by changing the condtion to sat that as long as a point is within
a certain distance of the curve we will color it. Mathematically we choose
some number :math:`e > 0` and pick the points that satisfy the following

.. math::

   |f(x, y)| < e

Basic Usage
-----------

To get started with the :code:`ImplicitXY` shape all we need to do is provide it 
with an :code:`f`. Since we already have :ref:`use_ref_shape_circle` and
:ref:`use_ref_shape_line` shapes built into stylo we will use the parabola from
above as an example

.. stylo-image::
   :align: center
   :img-width: 1920
   :img-height: 1080
   :include-code:
   :display-width: 75%

   from stylo.color import FillColor
   from stylo.shape import ImplicitXY
   from stylo.image import SimpleImage

   def f(x, y):
       return x*x - y

   color = FillColor()
   parabola = ImplicitXY(f)
   image = SimpleImage(parabola, color)


Drawing Options
---------------

You can control how the curve is drawn by using the following arguments

- :code:`pt`: This controls the thickness of the curve. (The value of this
  argument is used as the value of :math:`e` we defined in the introduction)
- :code:`above`: This shades in the area "above" the curve
- :code:`below` This shades in the area "below" the curve

.. note::

   :code:`above` and :code:`below` might not behave in the way you would
   expect depending on the shape of your curve. If you don't see the result
   you expected, try using the other argument

.. stylo-image::
   :align: center
   :img-width: 1920
   :img-height: 1080
   :include-code:
   :display-width: 75%

   from stylo.color import FillColor
   from stylo.shape import ImplicitXY
   from stylo.image import LayeredImage

   def f1(x, y):
       return 2*x*x + 0.6 - y

   def f2(x, y):
       return x*x - y

   def f3(x, y):
       return x*x/2 - 0.6 - y 

   color = FillColor()

   above = ImplicitXY(f1, above=True)
   curve = ImplicitXY(f2, pt=0.2)
   below = ImplicitXY(f3, below=True)

   image = LayeredImage()
   image.add_layer(above, color)
   image.add_layer(curve, color)
   image.add_layer(below, color)