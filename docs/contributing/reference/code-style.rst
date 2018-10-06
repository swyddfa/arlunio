.. _contribute_ref_code_style:

Code Style
==========

In order for your code to be accepted into the library as well as any tests on
its functionality it also has to pass the :code:`lint` test task.

What is Linting?
----------------

Linting is the term applied to a class of :term:`static analysis` tools
which look for stylistic errors (such as line lengths that are too long) and
sources of potential errors (you defined a variable called :code:`x` but didn't
use it).

These tools won't catch everything since they don't run your code so subtle
errors will pass you by but obvious mistakes such as typos can be caught before
your code is even run.

The Lint Test
-------------

Our :code:`lint` tox task is defined as follows.

.. literalinclude:: ../../../tox.ini
   :start-after: # <lint>
   :end-before: # </lint>


.. attention::

   The box above is extracted from the current version of :code:`tox.ini`. If
   what you read here doesn't match what is above then it is a sign that this
   page is out of date and an issue should be raised.

This subjects everyone's code to the following standard.

- The automatic formatting tool `black`_ doesn't want to rewrite anything
- The linting tool `flake8`_ doesn't find any issues.

Why Black?
^^^^^^^^^^

`black`_ is a tool that will rewrite your code so that it is formatted in a
certain way. We use this so that all code in the library is formatted in a
consistent way so is easier to read (at least that's the theory).

It also has the added benefit of formatting your code in a way that will pass
most of :code:`flake8`'s checks automatically.

Why Flake8?
^^^^^^^^^^^

In addition to ensuring that your code follows the :pep:`8` style guide
:code:`flake8` will check for a number of "obvious" errors e.g.
variable names that are not spelt correctly. So by passing its checks you can be
reasonably confident that your code is at least consistent, being a static
analysis tool it can't make any guarantees about the correctness of your code
though.

When they don't get along
^^^^^^^^^^^^^^^^^^^^^^^^^

Unfortunately there is an occasional edge case where :code:`black` and
:code:`flake8` don't get along. If you encounter one of these don't worry too
much about we'll work through it together and come up with a work around.

.. _black: https://github.com/ambv/black
.. _flake8: http://flake8.pycqa.org/en/latest/
