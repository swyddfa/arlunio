Checkerboard
============


We a can represent a basic checkerboard pattern by defining a function on
:math:`[-1, 1] \times [-1, 1]` that returns :code:`True` if the product of
:math:`x` and :math:`y` is positive

.. testcode:: small-checker

    from stylo import Image, Drawable

    class Checker(Drawable):

        def mask(self, x, y):
            return x * y > 0

Applying this then to an Image returns the following result

.. testcode:: small-checker

    checker = Checker()
    img = Image(512, 512)
    img(checker)


.. image:: /_static/examples/checker.png
    :width: 45%
    :align: center

.. note::

    Don't forget to call :code:`img.show()` or :code:`img.save()`!

But say that we wanted to create a chess board. Instead of trying to redefine
the :code:`mask` method so that it repeats we can modify the `Domain`_ that the
`Drawable`_ object uses. By getting the domain to repeat we can achieve the
desired effect without having to modify the :code:`mask` method.

.. testcode:: large-checker

    from stylo import Image, Domain, Drawable

    class Checker(Drawable):

        def domain(self):
            domain = Domain()
            domain.repeat(-4, 4, -4, 4)
            return domain

        def mask(self, x, y):
            return x * y > 0


.. testcode:: large-checker

    checker = Checker()
    img = Image(512, 512)
    img(checker)

.. image:: /_static/examples/large-checker.png
    :width: 45%
    :align: center


.. _Domain: ../reference/domain.html
.. _Drawable: ../reference/drawable.html
