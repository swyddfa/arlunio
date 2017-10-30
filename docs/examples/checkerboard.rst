Checkerboard
============


We a can represent a basic checkerboard pattern by defining a function on
:math:`[-1, 1] \times [-1, 1]` that returns :code:`True` if the product of
:math:`x` and :math:`y` is positive

.. testcode:: small-checker

    from stylo import Image, cartesian

    @cartesian()
    def checker(x, y):
        return x * y > 0

Applying this then to an Image returns the following result

.. testcode:: small-checker

    img = Image(512, 512)
    img(checker)
    img.show()


.. image:: /_static/examples/checker.png
    :width: 45%
    :align: center

But say that we wanted to create a chess board. Instead of trying to redefine
the pattern so that it repeats we can let :code:`stylo` do that for us using
the :code:`extend_periodically` decorator. To use it we simply put the
decorator in between our :code:`@cartesian` decorator and our function
definition.

.. testcode:: large-checker

    from stylo import Image, cartesian, extend_periodically

    @cartesian(X=[-4, 4], Y=[-4, 4])
    @extend_periodically()
    def checker(x, y):
        return x * y > 0

You specify what domain your original pattern is defined on to the
:code:`extend_periodically` (which defaults to :math:`[-1, 1] \times [-1, 1]`)
and provide a larger domain to the :code:`@cartesian`. Then by passing the
result to an image as normal we get

.. testcode:: large-checker

    img = Image(512, 512)
    img(checker)
    img.show()

.. image:: /_static/examples/large-checker.png
    :width: 45%
    :align: center
