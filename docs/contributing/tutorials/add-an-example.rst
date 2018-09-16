.. _contribute_tutorial_add_example:

Adding an Example to the Documentation
======================================

In this tutorial we'll go through the process of adding a new example like
:ref:`extending_example_pacman` to the documentation. Examples are added as test cases
to the test suite in the :code:`tests/examples` folder, among other reasons this ensures
that the example always works with the current version of :code:`stylo`

The test case is written in an unusual way but this allows it to work with our automated
build system for the documentation which will

- Test and benchmark your example
- Save the example image to the :code:`docs/_static` folder
- Add a page for your example to the documentation including the image and the example
  code

Overview
--------

Your example will need to be written with the following structure.

.. code-block:: python

   """
   Module Docstring.

   Here you can include any explanations and notes about your example. It will be pasted
   straight into the generated example page in the documentation and will appear before
   your code but after the example image
   """

   from stylo.testing.examples import define_benchmarked_example

   example_info = {
       "name": "my_example",
       "type": "using"  # This determines where on the documentation your example is included
   }

   def my_example():

       # <example>

       # Your example goes here, this is what the user will see in the documentation.

       # </example>

       return image

   test_my_example = define_benchmarked_example("my_example", my_example)


Finally make sure that your example is saved to the :code:`tests/examples` folder with
a filename like :code:`test_my_example.py`.

For the remainder of the tutorial we'll go through the process of creating an example
that will draw a red circle in the center of an image.

The Code
^^^^^^^^

We'll start with the most important part writing the code that is the example. In our
case that's constructing an :code:`Image` instance that can be used to draw a red circle.

.. testcode:: contribute_tutorial_add_example

   from stylo.color import FillColor, RGB8
   from stylo.domain import SquareDomain
   from stylo.image import SimpleImage
   from stylo.shape import Circle


   domain = SquareDomain(-1, 1)
   circle = Circle(0, 0, 0.75)
   red = FillColor(RGB8.parse("ff0000"))

   image = SimpleImage(domain, circle, red)

Save your code in a file such as :code:`tests/examples/test_red_circle.py`.

.. important::

   Your filename *must* start with :code:`test_` for it to be recognised as a test by
   :code:`pytest`.

The Example Function
^^^^^^^^^^^^^^^^^^^^

With the example written we now need to rewrite it in such a way that it works with the
automated test and documentation pipelines. The first step is to wrap it in a function
that takes no arguments and returns the :code:`image` variable we have created.

.. important::

   This function must include *everything* including your :code:`import` statements

You also need to add the comment :code:`# <example>` before your first import
statement and the comment :code:`# </example>` after the line where you create the
:code:`image` variable.

These tags are used by :code:`sphinx` to determine where your example code starts and
ends so that only the code relating to the example itself is shown on the generated
example page.

After this step your example should look something like this

.. code-block:: python

   def make_red_circle():

       # <example>

       from stylo.color import FillColor, RGB8
       from stylo.domain import SquareDomain
       from stylo.image import SimpleImage
       from stylo.shape import Circle


       domain = SquareDomain(-1, 1)
       circle = Circle(0, 0, 0.75)
       red = FillColor(RGB8.parse("ff0000"))

       image = SimpleImage(domain, circle, red)

       # </example>

       return image


Declaring Your Example
^^^^^^^^^^^^^^^^^^^^^^

With your example function defined, next you need to convert it into a test case that
can be run by :code:`pytest`. Thankfully, we have a function
:func:`define_benchmarked_example` from the :code:`stylo.testing.examples` module that
does this for you. All you have to do is import it and call it.

This function a few things:

- It converts your example function into a test case that can be run by :code:`pytest`
- The test case takes the image you define and generates a number of images of different
  sizes and records the execution time using :code:`pytest-benchmark`
- It saves the smallest of these images to the :code:`docs/_static` folder to be included
  in the documentation.

.. code-block:: python

    from stylo.testing.examples import define_benchmarked_example


    def make_red_circle():

        # <example>

        from stylo.color import FillColor, RGB8
        from stylo.domain import SquareDomain
        from stylo.image import SimpleImage
        from stylo.shape import Circle


        domain = SquareDomain(-1, 1)
        circle = Circle(0, 0, 0.75)
        red = FillColor(RGB8.parse("ff0000"))

        image = SimpleImage(domain, circle, red)

        # </example>

        return image


    test_red_circle = define_benchmarked_example("red_circle", make_red_circle)

.. important::

   The variable the result is assigned to must also start with :code:`test_` for it to
   be recognised as one.

In addition to passing your function you also need to pass in a name for your example,
this will become the filename of the image that is saved to the :code:`docs/_static`.

At this point your example should be fully integrated into the testing part of the
automated pipelines. You can check this by running the benchmarking suite using the
following command.

.. code-block:: sh

   $ tox -e benchmark

You should see output similar to the following

.. figure:: /_static/tox_e_benchmark.png
   :width: 75%
   :align: center

   :code:`$ tox -e benchmark`

You should also see your example saved to :code:`docs/_static/red_circle.png`

Integrating with the Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The final step is to provide some additional info about your example so that the
:ref:`contribute_reference_exampledoc` script can add your example to the correct place
in the documentation.

This is just adding a dictionary called :code:`example_info` somewhere in your
:code:`test_red_circle.py` file. It currently contains two fields:

- :code:`name`: The name of your example, this *must* match the name that you passed to
  :code:`define_benchmarked_example`
- :code:`type`: A string that indicates which section of the documentation your example
  belongs to. This *must* be one of the following: :code:`using`, :code:`extending` or
  :code:`contributing`.

If you want to include an explanation to go along with your example you can include a
module level docstring. This will be pasted into the generated :code:`.rst` file so
any valid reStructuredText will be rendered.

Below is the complete example including the :code:`example_info` dictionary:

.. code-block:: python

    """In this example we demonstrate how a red circle can be drawn by making use
    of the builtin :code:`Circle` shape.
    """

    from stylo.testing.examples import define_benchmarked_example

    example_info = {
        'name': 'red_circle',
        'type': 'using'
    }


    def make_red_circle():

        # <example>

        from stylo.color import FillColor, RGB8
        from stylo.domain import SquareDomain
        from stylo.image import SimpleImage
        from stylo.shape import Circle


        domain = SquareDomain(-1, 1)
        circle = Circle(0, 0, 0.75)
        red = FillColor(RGB8.parse("ff0000"))

        image = SimpleImage(domain, circle, red)

        # </example>

        return image


    test_red_circle = define_benchmarked_example("red_circle", make_red_circle)

Running the command

.. code-block:: sh

   $ tox -e docs-build

.. note::

   Because examples are generated using the :ref:`contribute_reference_exampledoc`
   script, you need to run a full build of the documentation.

You should be able to see your example page similar to the image below included in the
documentation.

.. figure:: /_static/red_circle_page.png
   :width: 75%
   :align: center

   The generated example page
