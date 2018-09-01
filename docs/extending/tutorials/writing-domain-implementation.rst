.. _extend_tutorial_domain_implementation:

Writing a Domain Implementation
===============================

.. note::

   This tutorial is for writing a domain implementation for an existing family of domain
   objects. If you are looking to create your own family of domains please refer to this
   tutorial.

.. todo::

   Write this tutorial.

:code:`Domain` classes such as :code:`RealDomain` define an interface common to all
domain objects, by basing your class on one of these bases you do get some code for free.
However you still need to generate the data yourself and it needs to be done in a way
that the base class understands.

In this tutorial we'll outline how to implement your own domain as part of
the :code:`RealDomain` family by creating our own version of the
:class:`SquareDomain <stylo.domain.square.SquareDomain>` class which models the
following mathematical domain.

.. math::

   [a, b] \times [a, b]\, a, b \in \mathbb{R}

This tutorial assumes that you are already familiar with the basics of domains and how
a user typically interacts with them. It also assumes that you are familiar with the
`numpy`_ library. If needed you can refer to the following tutorials:

- :ref:`use_tutorial_domain_system`

.. note::

   Although this tutorial focuses on writing implementations for the :code:`RealDomain`
   family the process is very similar for other families.

You can refer to the complete implementation in the
:ref:`extend_tutorial_domain_implementation_complete` section

First Steps
-----------

The first step in implementing our domain is to import the :code:`RealDomain` class and
subclass it

.. testcode:: extend_tutorial_domain_implementation_a

   from stylo.domain import RealDomain

   class SquareDomain(RealDomain):

       def __init__(self, a, b):
           self.a = a
           self.b = b

Since :code:`RealDomain` is an abstract class with undefined methods if we tried to
create an instance of our class we would find that it would throw an error:

.. doctest:: extend_tutorial_domain_implementation_a

   >>> square = SquareDomain(0, 1)
   Traceback (most recent call last):
       ...
   TypeError: Can't instantiate abstract class SquareDomain with abstract methods _get_r, _get_t, _get_x, _get_y

The error message will tell us the methods we need to implement in order to integrate
with the code contained in the base class. In our case we need to implement a
method to return values for each of the exposed domain parameters.

If you want to be able to try out your domain as you go, then you can create dummy
implementations of each of the methods so you can at least create an instance of your
class

.. testcode:: extend_tutorial_domain_implementation_b

   from stylo.domain import RealDomain

   class SquareDomain(RealDomain):

       def __init__(self, a, b):
           self.a = a
           self.b = b

       def _get_x(self):
           pass

       def _get_y(self):
           pass

       def _get_r(self):
           pass

       def _get_t(self):
           pass

   square = SquareDomain(2, 3)

Note however that the domain doesn't return anything.

.. doctest:: extend_tutorial_domain_implementation_b

   >>> square.x
   >>>

Generating Values
-----------------

.. Note that the code below won't show up in the generated output but it's needed so
   that the doctests throughout this section will pass.

.. testsetup:: extend_tutorial_domain_implementation_c

   import numpy as np
   from stylo.domain import RealDomain

   class SquareDomain(RealDomain):

       def __init__(self, a, b):
           self.a = a
           self.b = b

       def _get_x(self):

           def mk_xs(width, height):

               row = np.linspace(self.a, self.b, width)
               xs = np.array([row for _ in range(height)])
               return xs

           return mk_xs

       def _get_y(self):

           def mk_ys(width, height):

               col = np.linspace(self.b, self.a, height)
               ys = np.array([col for _ in range(width)])
               return ys.transpose()

           return mk_ys

       def _get_r(self):

           xs = self._get_x()
           ys = self._get_y()

           def mk_rs(width, height):
               x = xs(width, height)
               y = ys(width, height)

               return np.sqrt(x*x + y*y)

           return mk_rs

       def _get_t(self):

           xs = self._get_x()
           ys = self._get_y()

           def mk_ts(width, height):
               x = xs(width, height)
               y = ys(width, height)

               return np.arctan2(y, x)

           return mk_ts


The :code:`_get_***` methods are called by the :code:`RealDomain` class behind the
scenes when a user accesses the corresponding parameter. This means that each of these
methods need to return:

- A function that takes the arguments :code:`(width, height)`
- When called this function has to return a numpy array
- The array must have the shape :code:`(height, width)`.

The above constraints mean that each of the :code:`_get_***` methods typically
have the following structure:

.. code-block:: python

   def _get_x(self):

       # Preprocessing steps can go here

       def mk_xs(width, height):
           # Construction of the domain goes here.
           return xs

       return mk_xs

The actual values to be returned are free for us to decide. We'll take our time
and implement :code:`_get_x` first, then move through each of the others a bit
quicker.

_get_x
^^^^^^

The :math:`x` values change as we move from left to right across the image with the
leftmost pixel taking the user's start value (:math:`a`). Similarly the rightmost pixel
will take the user's end value (:math:`b`). There are a number of ways we could
interpolate between these values but it probably makes sense to do so linearly - although
other schemes might give us some interesting results!

Thankfully there is a numpy function :func:`np.linspace <numpy.linspace>` that does this
for us, so constructing a row of pixels is quite straightforward:

.. code-block:: python

   row = np.linspace(self.a, self.b, width)

Since :math:`x` values don't change as we move up and down an image we only need to
duplicate the row :code:`height` times and package it up into a numpy array.

.. code-block:: python

   xs = np.array([row for _ in range(height)])

Which when combined with the general structure outlined above we get the complete
definition for :code:`_get_x`:

.. code-block:: python

   def _get_x(self):

       def mk_xs(width, height):

           row = np.linspace(self.a, self.b, width)
           xs = np.array([row for _ in range(height)])
           return xs

       return mk_xs

Now if we try our class out we'll see that it returns the :math:`x` values as expected.

.. doctest:: extend_tutorial_domain_implementation_c

   >>> square = SquareDomain(2, 3)
   >>> square.x(4, 4)
   array([[2.        , 2.33333333, 2.66666667, 3.        ],
          [2.        , 2.33333333, 2.66666667, 3.        ],
          [2.        , 2.33333333, 2.66666667, 3.        ],
          [2.        , 2.33333333, 2.66666667, 3.        ]])

_get_y
^^^^^^

The implementation for the :math:`y` values is almost identical to the :math:`x` values,
except this time the values change as we move up and down the image so the roles of
:code:`height` and :code:`width` from the previous example switch. We also need to
:term:`transpose` the resulting array so that the values we've called :code:`col`
actually appear as a column in the final array.

.. code-block:: python

   def _get_y(self):

       def mk_ys(width, height):

           col = np.linspace(self.b, self.a, height)
           ys = np.array([col for _ in range(width)])
           return ys.transpose()

       return mk_ys

.. important::

   So that the image doesn't appear upside down, the :math:`y` values need to start at
   the final value (:math:`b`) and end with the inital value (:math:`a`).

If you are following along you should now see that the :code:`y` parameter now also
returns values:

.. doctest:: extend_tutorial_domain_implementation_c

   >>> square = SquareDomain(0, 1)
   >>> square.y(4, 4)
   array([[1.        , 1.        , 1.        , 1.        ],
          [0.66666667, 0.66666667, 0.66666667, 0.66666667],
          [0.33333333, 0.33333333, 0.33333333, 0.33333333],
          [0.        , 0.        , 0.        , 0.        ]])

_get_r
^^^^^^
The next two methods may be a little unfamiliar to you if you haven't come across
:term:`polar coordinates` before. It's an alternate system for representing a point in
space based on the distance a point is from the origin and the angle it makes with the
:math:`x`-axis. For more details check out the :ref:`math_polar_coordinates` page.

Since we have already implemented functions for generating :math:`x` and :math:`y`
values and we know how to convert between the different coordinate systems it makes
sense to use the following formula:

.. math::

   r = \sqrt{x^2 + y^2}

By using numpy's :py:data:`np.sqrt <numpy.sqrt>` function, calculating the square
root of every value in an array is both fast and easy and we get the following
implementation.

.. code-block:: python

   def _get_r(self):

       xs = self._get_x()
       ys = self._get_y()

       def mk_rs(width, height):
           x = xs(width, height)
           y = ys(width, height)

           return np.sqrt(x*x + y*y)

       return mk_rs

And we can see that our domain now supports the :code:`r` property

.. doctest:: extend_tutorial_domain_implementation_c

   >>> square = SquareDomain(-1, 1)
   >>> square.r(4, 4)
   array([[1.41421356, 1.05409255, 1.05409255, 1.41421356],
          [1.05409255, 0.47140452, 0.47140452, 1.05409255],
          [1.05409255, 0.47140452, 0.47140452, 1.05409255],
          [1.41421356, 1.05409255, 1.05409255, 1.41421356]])

_get_t
^^^^^^

Last but not least, this method corresponds to the :math:`\theta` variable from
:term:`polar coordinates`. As with the previous method, since we already have the means
of generating :math:`x` and :math:`y` values that satisfy the user's input it makes sense
to use the conversion formula to generate values of :math:`\theta`

.. math::

   \theta = \tan^{-1}{\left(\frac{y}{x}\right)}

Numpy has a function :py:data:`np.arctan2 <numpy.arctan2>` which implements the
:math:`\tan^{-1}` function taking into account the quadrant the point :math:`(x, y)`
is a part of ensuring that the sign of :math:`\theta` is as expected.

.. code-block:: python

   def _get_t(self):

       xs = self._get_x()
       ys = self._get_y()

       def mk_ts(width, height):
           x = xs(width, height)
           y = ys(width, height)

           return np.arctan2(y, x)

       return mk_ts

Which finally enables the :code:`t` property on the domain.

.. doctest:: extend_tutorial_domain_implementation_c

   >>> square = SquareDomain(-1, 1)
   >>> square.t(4, 4)
   array([[ 2.35619449,  1.89254688,  1.24904577,  0.78539816],
          [ 2.8198421 ,  2.35619449,  0.78539816,  0.32175055],
          [-2.8198421 , -2.35619449, -0.78539816, -0.32175055],
          [-2.35619449, -1.89254688, -1.24904577, -0.78539816]])

Further Resources
-----------------

That's it! You now know the bare minimum required to go off and write your own domain
implementations, however :code:`stylo` comes with a few more tools and helpers that you
can use to avoid doing a lot of the legwork work yourself. We'll wrap up by briefly
outlining what these helpers are and where you can go to find out more about them.

Conversion Tools
^^^^^^^^^^^^^^^^

When working through the sections for the :code:`_get_t` and :code:`_get_r` functions
you might have thought that implementing a number of different domains might get
laborious especially if these methods are always based off the :math:`x` and :math:`y`
values. Similarly you might be working a lot with the :math:`r` and :math:`\theta`
methods leaving you to implement a number of repetitive :code:`_get_x` and
:code:`_get_y` methods.

In an effort to reduce the amount of duplicated code :code:`stylo` comes with a few
helper classes that you can use as a base for your class. These classes will provide
default implementations for one or more of the methods required by your domain family
letting you focus on just the interesting bits.

For example, for the :code:`RealDomain` family we have the
:class:`CartesianConversion <stylo.domain.helpers.CartesianConversion>` and
:class:`PolarConversion <stylo.domain.helpers.PolarConversion>` classes that provide
implementations of methods that convert one coordinate system to another.

Below are some links to tutorials introducing some of these classes.

- :ref:`extend_tutorial_cartesian_conversion`
- polar

.. todo::

   Link to the tutorials outlining the usage of the various conversion helpers

Testing Tools
^^^^^^^^^^^^^

By basing your domain off a class such as :code:`RealDomain` and implementing all of the
abstract methods you know that the base class knows how to talk to your implementation
but how do you know if your class integrates with :code:`stylo`'s other systems?

This is where testing comes in, but you don't want to have to keep your tests up to date
with the expectations of the core library. So each domain family also has its own base
test class in the :code:`stylo.testing` namespace.

If you base your tests off one of these base classes such as
:class:`BaseRealDomainTest <stylo.testing.BaseRealDomainTest>` then your implementation
will be automatically tested that it conforms with the expectations of the rest of the
library. If they change, then tests on the base class will be updated to enforce them.

Below are links to tutorials that show you how to get started testing your newly
implemented domain.

.. todo::

   Link to the tutorial outlining how to use the :class:`BaseDomainTest`

.. _extend_tutorial_domain_implementation_complete:

Bringing It All Together
------------------------

Here is the complete definition of our :code:`SquareDomain` class.

.. code-block:: python
   :linenos:

   import numpy as np
   from stylo.domain import RealDomain

   class SquareDomain(RealDomain):

       def __init__(self, a, b):
           self.a = a
           self.b = b

       def _get_x(self):

           def mk_xs(width, height):

               row = np.linspace(self.a, self.b, width)
               xs = np.array([row for _ in range(height)])
               return xs

           return mk_xs

       def _get_y(self):

           def mk_ys(width, height):

               col = np.linspace(self.b, self.a, height)
               ys = np.array([col for _ in range(width)])
               return ys.transpose()

           return mk_ys

       def _get_r(self):

           xs = self._get_x()
           ys = self._get_y()

           def mk_rs(width, height):
               x = xs(width, height)
               y = ys(width, height)

               return np.sqrt(x*x + y*y)

           return mk_rs

       def _get_t(self):

           xs = self._get_x()
           ys = self._get_y()

           def mk_ts(width, height):
               x = xs(width, height)
               y = ys(width, height)

               return np.arctan2(y, x)

           return mk_ts

.. _numpy: https://www.numpy.org
