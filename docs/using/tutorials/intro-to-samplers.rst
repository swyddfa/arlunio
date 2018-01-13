Introduction To Samplers
========================

Samplers form the base upon which the entire animation system in stylo is
built. In essence they take a mathematical function and record its value at a
number of points throughout the domain. Samplers are useful for very simple
animations that only require the variation of a handful of parameters.

Creating Samplers
-----------------

Perhaps the easiest way to create a Sampler object based of a function is to
use the :code:`@sampled` decorator.

.. testcode:: sampler-intro

    from stylo import sampled

    @sampled()
    def x_squared(x):
        return x * x

This will create a :code:`Sampler` object that by default will sample your
function over a domain of :math:`[0, 1]` at 25 distinct points (which at 25fps
would be a single second of animation). If you are using an interactive
environment like a jupyter notebook you can view a plot of your function and
the points that have been sampled

.. testcode:: sampler-intro

    x_squared.show()

.. figure:: /_static/using/tutorials/sampler-plot.png
    :align: center

    Example output from calling `x_squared.show()`

You can however, alter both the domain and the number of points sampled by
passing arguments to the :code:`@sampled` decorator.

.. testcode:: sampler-intro

    @sampled(num_points=12, domain=[-1, 1])
    def x_squared(x):
        return x*x

    # x_squared.show()

.. figure:: /_static/using/tutorials/sampler-plot-2.png
    :align: center

    :math:`x^2` sampled over :math:`[-1, 1]` at 12 points

.. todo::

    Finish this tutorial with an example of using a Sampler in an animation
