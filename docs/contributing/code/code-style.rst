Code Style
==========

One of the checks your code must pass in order to make Travis happy is the
:term:`linting` test. This test checks two things:

1. That the `black`_ code formatter wouldn't make any changes to your code's formatting.
2. That the `flake8`_ linter doesn't see any issues with your code.

You can easily run the same tests that Travis would by running the following command

.. code-block:: sh

   $ pipenv run tox -e lint

Which will run the two tools against the code in both the :code:`stylo/` directory and
the :code:`tests/` directory.

.. _black: https://black.readthedocs.io/en/stable/
.. _flake8: http://flake8.pycqa.org/en/latest/