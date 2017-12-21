Getting Started
===============

In this guide you will find out everything you need to know to get started.
From installing stylo to creating your first image!

This guide assumes that you have a relatively recent version of Python
installed and running, any version number that starts with a 3 should be fine.
If perhaps you are not already familiar with Python you can find out how to get
started `here <https://www.python.org/about/gettingstarted/>`_

Installing Stylo
----------------

Stylo can easily be installed using `pip`_

.. code-block:: sh

    $ pip install stylo

That will install stylo and any other Python packages that it requires to run.
You can easily verify that stylo was installed correctly by running the
following command

.. code-block:: sh

    $ python -c 'import stylo ; print(stylo.__version__)'
    0.3.0

.. note::

    On some systems you might have to use the :code:`pip3` and :code:`python3`
    commands to get the correct version of python

Installing Jupyter (Optional)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Due to the visual nature of this library it's recommended that you follow along
the tutorials using a `Jupyter Notebook`_. You can get setup with jupyter
notebooks with the following command.

.. code-block:: sh

    $ pip install jupyter
    $ jupyter notebook

This will download and install jupyter and start a new notebook server which
you will then interact with in the browser. To open a new notebook select
:code:`File->New->Python 3` from the menu.

.. note::

    More detailed information on getting started with Jupyter Notebooks can be
    found `here
    <https://jupyter.readthedocs.io/en/latest/content-quickstart.html>`_

Your First Image
----------------

In order to draw something using stylo we must first define a :code:`Drawable`,
that is a mathematical representation of a shape that we want to draw. For our
first image we will draw a circle.

.. testcode:: get-started

    from stylo import Drawable, Image

    class Circle(Drawable):

        def mask(self, r):
            return r <= 0.8

    circle = Circle()

Here we have defined a circle with a radius of 0.8, but currently this is only
an abstract representation of a circle. To be able to view it, we need to
"map" it onto an :code:`Image`, which is what we will do next

.. testcode:: get-started

    img = Image(512, 512)
    img(circle)

Here we have created an Image that has dimensions 512x512 pixels. Images in
stylo can behave as normal Python functions so to map the drawable onto an
image we simply pass the Drawable as an argument.

Finally we want to be able to see our Image! If you have been following along
in a jupyter notebook then you can get a preview of the Image by running the
following

.. code-block:: python

    %matplotlib inline
    img.show()

Alternatively you can save the image to a file to view in your favourite image
viewer by running the following

.. code-block:: python

    img.save('circle.png')

In either case you should hopefully see something like the following

.. figure:: /_static/using/tutorials/get-started-circle.png
    :width: 50%
    :align: center

    :code:`circle.png`

.. _pip: https://pip.pypa.io/en/stable/installing/
.. _Jupyter Notebook: https://jupyter.org/
