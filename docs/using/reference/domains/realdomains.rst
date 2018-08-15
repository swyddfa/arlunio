Real Domains
============

All of the domains here model subsets of :math:`\mathbb{R}^2`

The Interface
-------------

Every subclass of the :class:`RealDomain` abstract class will have the following
interface in common.

.. autoclass:: stylo.domain.RealDomain


Concrete Implementations
------------------------

Each of the following implementations of the :class:`RealDomain` interface can be used
on their own and represent a particular subset of :math:`\mathbb{R}^2`

.. autoclass:: stylo.domain.RectangularDomain

.. autoclass:: stylo.domain.SquareDomain

.. autoclass:: stylo.domain.UnitSquare

Transformations
---------------

Each of the following apply a certain transformation to a given domain, this means they
cannot be used on their own directly but depend on using a particular concrete
implementation as a base.

.. autoclass:: stylo.domain.transforms.Translation
