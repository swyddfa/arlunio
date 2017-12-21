Checkerboard
============


We a can represent a basic checkerboard pattern by defining a function on
:math:`[-1, 1] \times [-1, 1]` that returns :code:`True` if the product of
:math:`x` and :math:`y` is positive

.. testcode:: checker

    from stylo import Image, Drawable

    class Checker(Drawable):

        def mask(self, x, y):
            return x * y > 0

If an instance of a :code:`Drawable` is created without specifying a
:code:`Domain` then it will automatically use a :math:`[-1, 1] \times [-1, 1]`
domain.

.. testcode:: checker

    checker = Checker()
    img = Image(512, 512)
    img(checker)


.. image:: /_static/examples/checker.png
    :width: 45%
    :align: center

.. note::

    Don't forget to call :code:`img.show()` or :code:`img.save()`!

But say that we wanted to create a chess board, then we would need to have the
pattern repeat. One approach would be to try and redefine the :code:`mask`
method of the :code:`Checker` drawable. Alternatively we could modify the
domain we apply to the drawable.

.. testcode:: checker

    from stylo import Domain

    grid = Domain()
    grid.repeat(-4, 4, -4, 4)

    checker = Checker(domain=grid)
    img = Image(512, 512)
    img(checker)

First we create a new instance of a :code:`Domain` object, which when not given
any arguments will default to :math:`[-1, 1] \times [-1, 1]`. Then by using the
:code:`repeat` method we simply tell the domain to extend itself to
:math:`[-4, 4] \times [-4, 4]` and repeat itself. This gives us a :math:`4
\times 4` grid with each grid square being a copy of the original pattern.

.. image:: /_static/examples/large-checker.png
    :width: 45%
    :align: center


.. _Domain: ../reference/domain.html
.. _Drawable: ../reference/drawable.html
