.. _extend_expressions:

Expressions
===========

Expressions are one of the most integral parts of stylo. They are a
representation of some mathematical expression which can be inspected,
evaluated and even saved and loaded from data formats such as JSON. This page
will only focus on using an expression once it has been constructed. There are
however a number of other documents available:

- <A document/tutorial on writing expression compatible functions.>
- <A document/tutorial on extending the system.>
- <A document on the implementation of the core system.>

.. todo::

   Make these documents exist.

Perhaps the easiest way to construct an expression for us to look at is to use
the |trace| decorator. For the purposes of this document we will be looking at
a simple :code:`add` function and a slightly less trivial :code:`distance`
function::

   >>> import stylo as st

   >>> @st.trace
   ... def add(x, y):
   ...     return x + y

   >>> add
   (+ x y)

   >>> @st.trace
   ... def distance(x, y):
   ...     xs = x*x
   ...     ys = y*y
   ...     return st.sqrt(xs + ys)

   >>> distance
   (sqrt (+ (* x x) (* y y)))

.. _extend_expressions_eval:

Evaluating Expressions
----------------------

There are a number of ways in which a

Perhaps the most common task you will want to perform with an expression will
be to evaluate it. In the case where all the values are already known this can
be as simple as calling the |StyExpr.eval| method on the expression::

    >>> one = st.StyConst(1)
    >>> two = st.StyConst(2)

    >>> plus = one + two
    >>> plus
    (+ 1 2)

    >>> plus.eval()
    3





