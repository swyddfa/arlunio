Checkerboard
============

Mathematically we can define a basic checkerboard as follows:

.. math::
    checkerboard(x, y) =  \begin{cases}
        white, \text{ if } xy > 0 \\
        black, \text{ otherwise}
    \end{cases}

where :math:`x, y \in [-1, 1]` Which we can write in python as such:

.. code-block:: python

  from mage import Image, cartesian

  @cartesian(X=[-1, 1], Y=[-1, 1])
  def checker(x, y):
      return x * y > 0

  img = Image(512, 512)
  img(checker)

Which gives us the result below:

.. image:: /_static/examples/checker.png
    :width: 45%
    :align: center


However, it would be good if we could alter the size of the squares. We can do
this by extending the function we defined above. If we periodically extend the
function, then any time we deviate from the original domain, we shift the value
so that it has the same relative offset in the original domain. For example if
we are given a value of :math:`1.5`, it's outside the interval :math:`[-1,1]`
so we shift it left by the length of the interval - which in this case is 2 and
that gives us the final value of -0.5.

By defining the checkerboard in this way allows us to keep the nice simple
definition we started with and control the size of the square by simply mapping
the extended function onto larger/smaller domains. In Python we write this as:

.. code-block:: python

  from mage import Image, cartesian, extend_periodically

  @cartesian(X=[-4, 4], Y=[-4, 4])  # Changing these values affect the grid size
  @extend_periodically(X=[-1, 1], Y=[-1, 1])
  def checker(x, y):
      return x * y > 0

  img = Image(512, 512)
  img(checker)

.. image:: /_static/examples/scaled_checker.png
    :width: 45%
    :align: center
