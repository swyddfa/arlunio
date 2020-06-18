.. _contributing_getstarted:

Getting Started
===============

Setting up the Development Environment
--------------------------------------

Once you have the forked and cloned the repository you need to create a virtual
environment that contains all the dependencies for :code:`arlunio` itself as
well as a number of development tools.

From the root of the repository create a virtual envrionment named
:code:`.env` and activate it

.. code-block:: sh

   $ python -m venv .env
   $ source .env/bin/activate
   (.env) $

Once active you should see the prompt change to include the name of the
activated environment. The next step is to then install all the runtime and
development dependencies

.. code-block:: sh

   (.env) $ pip install -e .[dev]

Pre-Commit (Optional, but recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`pre-commit`_ is a tool that is used to automatically install and configure
pre-commit hooks that are run everytime you make a commit inside the
:code:`arlunio` git repository.

Pre-commit hooks are checks that are used to enforce certain standards in the
codebase, for example for Python code we have hooks that run the following
programs

- `black`_: This ensures that all python source code is formatted consistently
- `flake8`_: This ensures that all python code is free of any obvious bugs
  (undefined variables etc.)
- `reorder_python_imports`_: This ensures that all python :code:`import` statements are
  listed in a standard order.

Whether or not you setup :code:`pre-commit` is down to where in your workflow
you want to resolve any issues flagged by these checks i.e. when you commit vs
when opening your PR.

.. note::

   By setting this up in your repository you will get fixes for issues raised by
   :code:`black` and :code:`isort` for free whereas you would have to fix them
   manually while refining your pull request.

   For this reason we recommended setting this up for yourself.

To setup pre-commit in your copy of the codebase run the following command

.. code-block:: sh

   (.env) $ pre-commit install

From now on any commits in your copy of the repository will be checked against
all the hooks defined the repository's :code:`.pre-commit-config.yaml` file.

.. note::

   Your very first commit after installing :code:`pre-commit` will take a little
   time as :code:`pre-commit` sets up each hook for the first time. However
   after the initial run, executing the hooks only takes a few seconds.


.. _black: https://black.readthedocs.io/en/stable/
.. _flake8: http://flake8.pycqa.org/en/latest/index.html
.. _pre-commit: https://pre-commit.com/
.. _reorder_python_imports: https://github.com/asottile/reorder_python_imports
