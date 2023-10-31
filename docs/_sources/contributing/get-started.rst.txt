.. _contributing_getstarted:

Getting Started
===============

So you've decided you want to contribute - fantastic! Welcome aboard! On this
page you should find everything you need to get yourself setup and ready to
make changes.

Obtain the Source Code
----------------------

The source code for :code:`arlunio` itself, the website and the documentation
are all hosted in a `public repository <https://github.com/swyddfa/arlunio>`_.
on GitHub. Clicking the :code:`Fork` button on the top right hand side of the
screen will create your personal copy of the main repository within which you
will be free to make whatever changes you wish.

To pull down a copy of your repository to your machine, open up a terminal
in a folder of your choosing and run the following command, replacing
:code:`<username>` with your actual GitHub username::

   $ git clone https://github.com/<username>/arlunio

This will create a folder called :code:`arlunio` containing the contents of the
repository.

Setup the Python Environment
----------------------------

Now that you have a copy of the source code the next step would be to create a
:term:`virtual environment` and install into it all our dependencies,
development tools along with a development copy of arlunio itself. With your
terminal open in the repository's folder, create a virutal environment with the
name :code:`.env`::

   $ python -m venv .env

Next activate the environment and run :code:`pip install` to kick off the
installation::

   $ source .env/bin/activate
   (.env) $ pip install -e .[dev]

Setup Pre-Commit (Optional)
---------------------------

`pre-commit`_ is a tool that is used to automatically install and configure
pre-commit hooks that are run everytime you make a commit inside the
:code:`arlunio` git repository.

Pre-commit hooks are checks that are used to enforce certain standards in the
codebase, for example for Python code we have hooks that run the following
programs

- `black`_: This ensures that all python source code is formatted consistently
- `flake8`_: This ensures that all python code is free of any obvious bugs
  (undefined variables etc.)
- `reorder_python_imports`_: This ensures that all python :code:`import`
  statements are listed in a standard order.

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

Setup VSCode (Optional)
-----------------------

If you already have a preferred editor and workflow then don't let us stop you!
Feel free to skip this and carry on using your preferred tools.

If however, you're not sure on what to use then you might want to conisder
using `VS Code`_ as there are a number of integrations bundled with this
repository that make common tasks such as running code or building the
documentation easier.


.. _black: https://black.readthedocs.io/en/stable/
.. _flake8: http://flake8.pycqa.org/en/latest/index.html
.. _Git: https://git-scm.com/
.. _GitHub: https://github.com
.. _pre-commit: https://pre-commit.com/
.. _reorder_python_imports: https://github.com/asottile/reorder_python_imports
.. _VS Code: https://code.visualstudio.com/
