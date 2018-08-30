.. _use_tutorial_domain_system:

An Introduction to the Domain System
====================================

:code:`Domains` are one of the fundamental concepts that make up :code:`stylo`, however
most of the time they are hidden from view. You've probably defined a number of domains
and passed them off to other objects but I would be surprised if you have had to
manipulate them directly. In this tutorial we will introduce the interface that is
common to every :code:`Domain` object in :code:`stylo`. We will also focus on the
:class:`UnitSquare` domain from the :code:`RealDomain` family however what will be shown
here will hold across all domain objects and families.

.. doctest:: use_tutorial_domain_system

   >>> from stylo.domain import UnitSquare
   >>> unit_square = UnitSquare()
   >>> unit_square
   UnitSquare: [0, 1] x [0, 1]

Parameter Discovery
-------------------

Each domain object will expose one or more parameters, these will be the same for every
domain object within the same family. These parameters correspond with some aspect of
the mathematical domain that family represent, for example in the case of the
:code:`RealDomain` family these parameters correspond with each of the coordinate
variables that can be used to address points in space within the domain.

You can find a list of these parameters in the :code:`parameters` attribute on any
:code:`Domain` instance.

.. doctest:: use_tutorial_domain_system

   >>> unit_square.parameters
   ['x', 'y', 'r', 't']

Which shows us we have the following parameters available:

- :code:`x`: This corresponds to the :math:`x` spatial coordinate variable from the
  :term:`cartesian coordinate<cartesian coordinates>` system.
- :code:`y`: This corresponds to the :math:`y` spatial coordinate variable from the
  :term:`cartesian coordinate<cartesian coordinates>` system.
- :code:`r`: This corresponds to the :math:`r` spatial coordinate variable from the
  :term:`polar coordinate<polar coordinates>` system
- :code:`t`: This corresponds to the :math:`\theta` spatial coordinate variable
  from the :term:`polar coordinate<polar coordinates>` system

Values from a Single Parameter
------------------------------

Now that you know which parameters the domain exposes, you probably want to get some
values from it. Each domain will expose each of the parameters as an attribute that
returns a function in width and height. This is how :code:`stylo` converts abstract
representations of a mathematical space into a discrete grid of data that can then be
used to create images with.

Say for example we wanted to create a :code:`4x4` image based on the :math:`x`
coordinate, we can generate the data as follows:

.. doctest:: use_tutorial_domain_system

   >>> xs = unit_square.x
   >>> xs(4, 4)
   array([[0.        , 0.33333333, 0.66666667, 1.        ],
          [0.        , 0.33333333, 0.66666667, 1.        ],
          [0.        , 0.33333333, 0.66666667, 1.        ],
          [0.        , 0.33333333, 0.66666667, 1.        ]])

Alternatively we can do this in one step without the need for the :code:`xs` variable:

.. doctest:: use_tutorial_domain_system

   >>> unit_square.x(4, 4)
   array([[0.        , 0.33333333, 0.66666667, 1.        ],
          [0.        , 0.33333333, 0.66666667, 1.        ],
          [0.        , 0.33333333, 0.66666667, 1.        ],
          [0.        , 0.33333333, 0.66666667, 1.        ]])

Values from Multiple Parameters
-------------------------------

There will be situations where you want to retrieve values from multiple parameters at
once for example when drawing a circle. In this case you would want to know both
the :math:`x` and :math:`y` values which we can retrieve using the indexing syntax.

We can pass in the tuple :code:`('x', 'y')` and receive a function in width and height
- much like the case for a single parameter but now it will return a tuple containing
both of the values we asked for.

.. doctest:: use_tutorial_domain_system

   >>> values = unit_square[('x', 'y')]
   >>> xs, ys = values(4, 4)

   >>> xs
   array([[0.        , 0.33333333, 0.66666667, 1.        ],
          [0.        , 0.33333333, 0.66666667, 1.        ],
          [0.        , 0.33333333, 0.66666667, 1.        ],
          [0.        , 0.33333333, 0.66666667, 1.        ]])

   >>> ys
   array([[1.        , 1.        , 1.        , 1.        ],
          [0.66666667, 0.66666667, 0.66666667, 0.66666667],
          [0.33333333, 0.33333333, 0.33333333, 0.33333333],
          [0.        , 0.        , 0.        , 0.        ]])

Notice that the values will always be returned in the order specified by you.

.. doctest:: use_tutorial_domain_system

   >>> ys, xs = unit_square[('y', 'x')](4, 4)

   >>> ys
   array([[1.        , 1.        , 1.        , 1.        ],
          [0.66666667, 0.66666667, 0.66666667, 0.66666667],
          [0.33333333, 0.33333333, 0.33333333, 0.33333333],
          [0.        , 0.        , 0.        , 0.        ]])

   >>> xs
   array([[0.        , 0.33333333, 0.66666667, 1.        ],
          [0.        , 0.33333333, 0.66666667, 1.        ],
          [0.        , 0.33333333, 0.66666667, 1.        ],
          [0.        , 0.33333333, 0.66666667, 1.        ]])

.. todo::

   Sum up, and link to additional domain resources.
