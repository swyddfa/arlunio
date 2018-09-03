.. _extend_tutorial_cartesian_conversion:

Using the CartesianConversion Helper
====================================

Here is a list of tutorials and resources that this tutorial assumes you are already
familiar with.

- :ref:`math_polar_coordinates`
- :ref:`math_cartesian_coordinates`
- :ref:`extend_tutorial_domain_implementation`

There are occasions when writing a :code:`RealDomain` implementation, say a
:code:`Rotation` transform where all the "interesting" code is contained within the
:code:`_get_r` and :code:`_get_t` methods and all you need is a conversion from polar
to cartesian coordinates.

This is where the :class:`CartesianConversion <stylo.domain.helpers.CartesianConversion>`
helper class comes in, it provides implementations of the :code:`_get_x` and
:code:`_get_y` methods to convert them from the :code:`_get_r` and :code:`_get_t`
methods that you provide.

This tutorial walks you through the process of using this helper to implement an example
rotation domain transformation.

Setup
-----

As with any other domain transformation it starts with us creating a class and
subclassing :code:`RealDomainTransform`. However in this case we also include
:class:`CartesianConversion <stylo.domain.helpers.CartesianConversion>` in our list of
base classes

.. testcode:: extend_tutorial_cartesian_conversion_a

   from stylo.domain.transform import RealDomainTransform
   from stylo.domain.helpers import CartesianConversion


   class Rotation(CartesianConversion, RealDomainTransform):
       pass

.. important::

   The order in which these classes are included is *very* important.
   :code:`CartesianConversion` must come before the :code:`RealDomainTransform`

If we were to try and create an instance of our class now we will get an error (as is
expected since :code:`RealDomainTransform` is an abstract class).

.. doctest:: extend_tutorial_cartesian_conversion_a

   >>> rotate = Rotation()
   Traceback (most recent call last):
      ...
   TypeError: Can't instantiate abstract class Rotation with abstract methods  _get_r, _get_t, _repr

But notice that :code:`_get_x` and :code:`_get_y` don't appear in the error message, this
is due to them being implemented by the :code:`CartesianConversion` helper.

Implementation
--------------

If you've implemented a domain transform before, the rest should be familiar to you,
it's just a case of implementing the remaining methods:

- :code:`__init__`: We need to take an angle as input from the user
- :code:`_repr`: We need a textual representation of the object, this is used by the
  :code:`__repr__` method in the :code:`RealDomainTransform` base class
- :code:`_get_r`: A method to generate the :math:`r` values
- :code:`_get_t`: A method to generate the :math:`\theta` values and here is where the
  actual rotation will be implemented

__init__
^^^^^^^^

The :code:`__init__` method is pretty straightforward it's just a matter of taking a
value from the user to represent an angle. Just don't forget to call the
:code:`__init__` method on the base class!

.. code-block:: python

   def __init__(self, domain, angle):
       super().__init__(domain)

       self.angle = angle

_repr
^^^^^

Again nothing too groundbreaking here, just a case of returning some meaningful string
to represent our rotation to the user.

.. code-block:: python

   def _repr(self):
       return "Rotation: {:.2f}rad".format(self.angle)

The reason domain transforms like :code:`RealDomainTransform` ask you to implement
:code:`_repr` and not :code:`__repr__` is that the base class implements
:code:`__repr__` in a way that also displays the domain that the transformation is
acting upon.

_get_r
^^^^^^

The :math:`r` values don't change when rotated so all we need to do is return the
:math:`r` values from the base domain.

.. code-block:: python

   def _get_r(self):
       return self.domain.r

_get_t
^^^^^^

Here is the only non trivial method on this class. We need to get the base domain to
generate its :math:`\theta` values for us which we then *take away* the user's angle
which implements the rotation

.. code-block:: python

   def _get_t(self):

       ts = self.domain.t

       def mk_ts(width, height):
           return ts(width, height) - self.angle

       return mk_ts


Bringing It All Together
------------------------

Here is the complete class definition

.. testcode:: extend_tutorial_cartesian_conversion_b

   from math import pi

   from stylo.domain import UnitSquare
   from stylo.domain.helpers import CartesianConversion
   from stylo.domain.transform import RealDomainTransform


   class Rotation(CartesianConversion, RealDomainTransform):

       def __init__(self, domain, angle):
           super().__init__(domain)

           self.angle = angle

       def _repr(self):
           return "Rotation: {:.2f}rad".format(self.angle)

       def _get_r(self):
           return self.domain.r

       def _get_t(self):

           ts = self.domain.t

           def mk_ts(width, height):
               return ts(width, height) - self.angle

           return mk_ts

Which we can now use to apply a rotation to some domain

.. doctest:: extend_tutorial_cartesian_conversion_b

   >>> rotated = Rotation(UnitSquare(), pi/4)
   >>> rotated
   Rotation: 0.79rad
     UnitSquare: [0, 1] x [0, 1]

   >>> rotated.x(4, 4)
   array([[0.70710678, 0.94280904, 1.1785113 , 1.41421356],
          [0.47140452, 0.70710678, 0.94280904, 1.1785113 ],
          [0.23570226, 0.47140452, 0.70710678, 0.94280904],
          [0.        , 0.23570226, 0.47140452, 0.70710678]])
