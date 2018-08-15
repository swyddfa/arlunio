Extending Stylo
===============

Extension v Development?
------------------------

Something you might be wondering is what's the difference between extending :code:`stylo`
and developing it?

To be honest the distinction is somewhat arbitrary but for now we'll define extending
:code:`stylo` as the following situation.

1. You want to add a new :code:`XXX` object. e.g. a new :code:`DomainTransform` or
:code:`Drawable`. Perhaps with the added goal of making this new object or collection
of objects available to others.

Stylo itself is designed to be a collection of systems that work together in creating
images and animated sequences. While it does come with a handful of objects that work
within these systems most of the time only the basics are covered.

The issue is that the possible range of applications is very large, you might want to
animate a stickman playing baseball or visualise the results of a simulation. The way in
which you would approach these two tasks is very different and will most likely involve
the use of a completely different set of objects.

The way in which we try to solve this is to provide a number of classes that define an
interface as long as these interfaces are implemented and the results work in an expected
way the new object should within the rest of the :code:`stylo` ecosystem.

Which brings us to this section of the documentation, here you will find guides all
geared around creating new objects that play nice with the existing interfaces. Other
tasks which affect stylo in a more fundamental way are left to the development section.


.. toctree::
   :maxdepth: 2

   reference/index



