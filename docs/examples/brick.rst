Brick
=====

On a domain of :math:`[-1 ,1] \times [-1, 1]` we can define a brick pattern
that we want to repeat as follows:

.. math::

    brick(x, y) = \begin{cases}
        brickcolor_1, \text{ if } x \in [-0.95, 0.95] \text{ and } y \in [0.05, 0.95] \\
        brickcolor_2, \text{ if } x < -0.05 \text{ and } y \in [-0.95, -0.05] \\
        brickcolor_2, \text{ if } x > 0.05 \text{ and } y \in [-0.95, -0.05] \\
        mortarcolor, otherwise
    \end{cases}

where :math:`x, y \in [-1, 1]`. In Python we may write this as:

.. code-block:: python

    from mage.image import make_img
    from mage.coords import cartesian, extend_periodically
    from mage.color import hex_to_rgb

    @cartesian()
    def brick(x, y):

        # Top long brick
        if y >= 0.05 and y <=0.95 and x >= -0.95 and x <= 0.95:
            return hex_to_rgb('C77826')

        # Bottom left half brick
        if x <= -0.05 and y <= -0.05 and y >= -0.95:
            return hex_to_rgb('CC7F32')

        # Bottom right half brick
        if x >= 0.05 and y <= -0.05 and y >= -0.95:
            return hex_to_rgb('CC7F32')

        return hex_to_rgb('cccccc')

Which results with the following:

.. image:: /_static/examples/brick.png
    :width: 45%
    :align: center

Now by extending this periodically and choosing a larger domain we can now tile
the pattern to create a wall

.. code-block:: python

    @cartesian(X=[-5, 5], Y=[-5, 5])
    @extend_periodically()
    def brick_wall(x, y):

        # Top long brick
        if y >= 0.05 and y <=0.95 and x >= -0.95 and x <= 0.95:
            return hex_to_rgb('C77826')

        # Bottom left half brick
        if x <= -0.05 and y <= -0.05 and y >= -0.95:
            return hex_to_rgb('CC7F32')

        # Bottom right half brick
        if x >= 0.05 and y <= -0.05 and y >= -0.95:
            return hex_to_rgb('CC7F32')

        return hex_to_rgb('cccccc')

Which gives us:

.. image:: /_static/examples/brick_wall.png
    :width: 45%
    :align: center
