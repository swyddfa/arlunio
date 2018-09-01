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
:code:`SquareDomain` class which models the following mathematical domain.

.. math::

   [a, b] \times [a, b]\, a, b \in \mathbb{R}

This tutorial assumes that you are already familiar with the basics of domains and how
a user typically interacts with them. It also assumes that you are familiar with the
numpy library. If needed you can refer to the following tutorials:

- :ref:`use_tutorial_domain_system`

.. todo::

   Once the API reference is in place link to the actual :code:`RealDomain` object that
   contains the blurb on what each of the parameters mean.

.. note::

   Although this tutorial focuses on writing implementations for the :code:`RealDomain`
   family the process is very similar for other families.

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

.. Note that the code below won't show up in the generated output but it's needed so
   that the doctest at the end of this section will pass.

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
           pass

       def _get_r(self):
           pass

       def _get_t(self):
           pass

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

.. Again, this is included so that the doctest at the end of the section will pass.

.. testsetup:: extend_tutorial_domain_implementation_d

   import numpy as np
   from stylo.domain import RealDomain

   class SquareDomain(RealDomain):

       def __init__(self, a, b):
           self.a = a
           self.b = b

       def _get_y(self):

           def mk_ys(width, height):

               col = np.linspace(self.b, self.a, height)
               ys = np.array([col for _ in range(width)])
               return ys.transpose()

           return mk_ys

       def _get_x(self):
           pass

       def _get_r(self):
           pass

       def _get_t(self):
           pass

In the case of :math:`y` values, it's almost identical to the :math:`x` values, except
this time the values change as we move up and down the image so the roles of
:code:`height` and :code:`width` from the previous example switch roles. We also need to
transpose the resulting array so that the values we've called :code:`col` actually appear
as a column in the final array.

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

.. doctest:: extend_tutorial_domain_implementation_d

   >>> square = SquareDomain(0, 1)
   >>> square.y(4, 4)
   array([[1.        , 1.        , 1.        , 1.        ],
          [0.66666667, 0.66666667, 0.66666667, 0.66666667],
          [0.33333333, 0.33333333, 0.33333333, 0.33333333],
          [0.        , 0.        , 0.        , 0.        ]])

_get_r
^^^^^^

_get_t
^^^^^^

Further Resources
-----------------

That's it! You now know the bare minimum required to go off and write your own domain
implementations however :code:`stylo` comes with a few more tools and helpers that you
can use to avoid doing a lot of the boilerplate work yourself. We'll wrap up by briefly
outlining what these helpers are and where you can go to find out more about them.

Conversion Tools
^^^^^^^^^^^^^^^^

.. todo::

   Link to the tutorials outlining the usage of the various conversion helpers

Testing Tools
^^^^^^^^^^^^^

.. todo::

   Link to the tutorial outlining how to use the :code:`BaseDomainHelper`
