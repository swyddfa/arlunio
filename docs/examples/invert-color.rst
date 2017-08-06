Invert the Colours of an Image
==============================

Considering the following image

.. figure:: /_static/reference/image/example.png
    :width: 65%
    :align: center

    :code:`example.png`

We can invert its colors as follows

.. code-block:: python

    from stylo import Image

    img = Image.fromfile('example.png')
    (-img).save('example-inverted.png')

.. figure:: /_static/reference/image/example-inverted.png
    :width: 65%
    :align: center

    The resulting image
