Sampler
=======

The :code:`Sampler` object allows you to easily take a mathematical function
:math:`f` defined on the interval :math:`[0, 1]` and discretise it. It is the
key component behind interpolation and the :code:`Driver` object.

Creation
--------

There are a number of methods for constructing a :code:`Sampler` object
depending on your circumstances

Manually
^^^^^^^^

Creating a :code:`Sampler` object can be as simple as just calling the
constructor with no arguments

.. doctest:: sampler-creation

   >>> from stylo.interpolate import Sampler
   >>> Sampler()
   Sampled function:
   Num Points: 25

As you can see the :code:`Sampler` object defaults to sampling 25 points in the
domain.  If no function is given then the :code:`Sampler` object will default
to the identity function :math:`f(x) = x`. You can however specify the function
up front along with the number of points, useful if you want to sample a
pre-existing function

.. doctest:: sampler-creation

   >>> from math import sin
   >>> Sampler(sin, num_points=250)
   Sampled function:
   Num Points: 250

Finally you can optionally provide a name to help you identify your samplers -
particularly useful for interactive sessions

.. doctest:: sampler-creation

   >>> Sampler(sin, num_points=100, name='Sine')
   Sine
   Num Points: 100


Using the Decorator
^^^^^^^^^^^^^^^^^^^

If you are defining your own function that you want sampled then you might want
to use the :code:`sampled` decorator

.. doctest:: sampler-creation

   >>> from stylo.interpolate import sampled
   >>> @sampled()
   ... def squared(x):
   ...     return x * x
   >>> squared
   squared
   Num Points: 25

You can also pass the number of points you want sampled to the decorator itself

.. doctest:: sampler-creation

   >>> from stylo.interpolate import sampled
   >>> @sampled(num_points=250)
   ... def squared(x):
   ...     return x * x
   >>> squared
   squared
   Num Points: 250


Using a Factory Function
------------------------

If you have a certain class of functions that you will want to sample often you
can use a factory function to both construct the function and return a sampled
version of it. For example if you wanted to sample many different quadratic
polynomials of the form :math:`p(x) = ax^2 + bx + c` you might use the
following factory function

.. doctest:: sampler-creation

   >>> def quadratic(a, b, c):
   ...     def p(x):
   ...         return a*x**2 + b*x + c
   ...     name = "{:+}x^2 {:+}x {:+}".format(a, b, c)
   ...     return Sampler(p, name=name)

Which could then be used as follows

.. doctest:: sampler-creation

   >>> quadratic(4, -2, 1.5)
   +4x^2 -2x +1.5
   Num Points: 25

Stylo itself comes with a number of such factory functions geared towards
interpolating between values while following certain curves which model certain
types of easing, see `Interpolators`_ for full details on those included.


Usage
-----

.. testsetup:: sampler-usage

   from stylo.interpolate import Sampler
   from math import sin, pi

Since :code:`Sampler` data is just a :code:`numpy` array you can access the
values using numpy's array `indexing`_ syntax

.. doctest:: sampler-usage

   >>> f = lambda x: sin(pi*x)
   >>> sin_sampled = Sampler(f)
   >>> sin_sampled[0]
   0.0
   >>> sin_sampled[sin_sampled[:] < 0.5]
   array([  0.00000000e+00,   1.30526192e-01,   2.58819045e-01,
            3.82683432e-01,   5.00000000e-01,   3.82683432e-01,
            2.58819045e-01,   1.30526192e-01,   1.22464680e-16])

However if you need an "exact" value for a point you can call the sampled
object just as you would a normal function

.. doctest:: sampler-usage

   >>> sin_sampled(pi / 4)
   0.6242...

Properties
----------

.. testsetup:: sampler-prop

   from stylo.interpolate import Sampler
   from math import sin, cos

Each of the arguments in the constructor are also available as a property,
allowing you to modify the :code:`Sampler` object after its creation

F
^^

This returns the function that is being sampled, however as you can call the
underlying function from the sample object itself this property is more useful
if you wish to change the underlying function

.. doctest:: sampler-prop

   >>> sin_sampled = Sampler(sin, name="sin(x)")
   >>> sin_sampled[0]
   0.0
   >>> sin_sampled.f = cos
   >>> sin_sampled[0]
   1.0

.. note::

    Changing this property immediately triggers a recalculation of the
    underlying data

Num Points
^^^^^^^^^^

This returns the number of points that have been sampled, it can also be used
to adjust the resolution of the sampling

.. doctest:: sampler-prop

   >>> sin_sampled.num_points
   25
   >>> sin_sampled.num_points = 250
   >>> len(sin_sampled)
   250

.. note::
    Changing this property immediately triggers a recalculation of the
    underlying data


Name
^^^^

This returns the name currently associated with the :code:`Sampler` object

.. doctest:: sampler-prop

   >>> sin_sampled.name
   'sin(x)'
   >>> sin_sampled.name = "f(x) = sin(x)"
   >>> sin_sampled
   f(x) = sin(x)
   Num Points: 250

.. _Interpolators: ./interpolators.html
.. _indexing: https://docs.scipy.org/doc/numpy/user/basics.indexing.html
