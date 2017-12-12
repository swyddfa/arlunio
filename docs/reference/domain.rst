Domain
======

.. autoclass:: stylo.Domain


Creation
--------

If a Domain object is created with no arguments it will default to
:math:`[-1, 1] \times [-1, 1]`

.. doctest:: dom-create

    >>> from stylo import Domain
    >>> Domain()
    [-1, 1] x [-1, 1]

Alternatively you can specify the start and end points as you create the domain

.. doctest:: dom-create

    >>> Domain(x_min=-2, x_max=2, y_min=0, y_max=3)
    [-2, 2] x [0, 3]

Getting Data
------------

It's all well and good having an abstract representation of the domain, however
it's not very useful unless we can get some values out of it. To get data out
of a domain object it needs to know three things:

- The coordinate variables

Modifiers
---------

Domains can be modified in a number of ways.

.. testsetup:: dom-modifiers

    from stylo import Domain

.. automethod:: stylo.drawable.Domain.repeat

.. doctest:: dom-modifiers

    >>> domain = Domain(x_min=0, x_max=1, y_min=0, y_max=1)
    >>> domain.repeat(0, 2, 0, 2)
    >>> domain['x', 5, 5]
    (array([[ 0. ,  0.5,  1. ,  0.5,  1. ],
           [ 0. ,  0.5,  1. ,  0.5,  1. ],
           [ 0. ,  0.5,  1. ,  0.5,  1. ],
           [ 0. ,  0.5,  1. ,  0.5,  1. ],
           [ 0. ,  0.5,  1. ,  0.5,  1. ]]),)

For an example of this modifier in action please see the `Checkerboard`_
example.

.. automethod:: stylo.drawable.Domain.transform

.. doctest:: dom-modifiers

    >>> domain = Domain(x_min=0, x_max=1, y_min=0, y_max=1)
    >>> domain.transform((0,2), r=0)
    >>> domain['y', 5, 5]
    (array([[-1.  , -1.  , -1.  , -1.  , -1.  ],
            [-1.25, -1.25, -1.25, -1.25, -1.25],
            [-1.5 , -1.5 , -1.5 , -1.5 , -1.5 ],
            [-1.75, -1.75, -1.75, -1.75, -1.75],
            [-2.  , -2.  , -2.  , -2.  , -2.  ]]),)


.. _Checkerboard: ../examples/checkerboard.html
