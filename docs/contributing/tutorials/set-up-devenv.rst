.. _contribute_tutorial_devenv_setup:

Setup the Development Environment
=================================

Before you can build the documentation or run the code and the tests you need to
have setup your development environment so that all the tools you need are
installed and configured.

.. todo::

   This guide is currently heavily biased towards UNIX style systems chances are
   portions of this guide won't work on Windows. We probably should have a
   Windows setup guide at some point.

Before we Start
---------------

This guide assumes that:

- You have :ref:`forked <contribute_tutorial_fork_repository>` the repository
- You have Python 3.6 or newer installed.
- You are comfortable using the command line.

There are currently two supported methods of setting up your development
environment.

- :ref:`contribute_tutorial_devenv_setup_script`
- :ref:`contribute_tutorial_devenv_manual`

The goal of the script is to lower the barrier to getting people contributing to
:code:`stylo`. Having a single command to run can be much more approachable than
having to run half a dozen of them. Additionally by using a script everyone
should end up with exactly the same setup - at least that is the theory.

On the other hand the script may not work for you or some people may feel better
doing the setup by hand as they want to know how things fit together or don't
like the idea of running some script they found on the internet. That is why we
also have the manual process, it does exactly the same steps as the script but
it's a lot more transparent.

At the end of the day, whichever approach you take we will happily support you
either way - everyone's system is different so there are bound to be a few
issues now and then.

.. _contribute_tutorial_devenv_setup_script:

Using a Script
--------------

To setup your environment using the script from the root of the repository run
the following command.

.. code-block:: sh

   $ ./scripts/devenv-setup.sh

The script will do the following:

- Check to see that you have a compatible version of Python installed.
- If you don't have `Pipenv`_ installed it will install it using the command
  :code:`pip install --user pipenv`
- It will then use pipenv to create a virtual environment and install all the
  runtime and development dependencies into it.
- One of these dependencies is `pre-commit`_ the script configures it to
  run some checks automatically whenever you make a commit.
- Finally as a check to make sure everything is setup correctly, the script will
  do a complete build of the documentation. See :ref:`contribute_ref_docs_build`
  for more details on this process.

.. _contribute_tutorial_devenv_manual:

Manually
--------

The manual setup follows the same process as the script above, the only
difference is that you will be running each of the commands and not the script.

1. The first step is to make sure you have `Pipenv`_ installed. Pipenv is a tool
   that brings together the management of :term:`virtual environments` and
   project dependencies into a single command.

   Pipenv can be installed using the following command.

   .. code-block:: sh

      $ pip install --user pipenv

2. Next use pipenv to create a virtual environment for the project and install
   all the runtime and development dependencies into it with the following
   command. This should be run from the root of the repository

   .. code-block:: sh

      $ pipenv install --dev

3. The next two commands need to be run from inside your virtual environment so
   we can activate it as follows:

   .. code-block:: sh

      $ pipenv shell

4. Next we need to setup `pre-commit`_ to run a few checks for us each time we
   make a commit. But we need to tell it your Python version so open up the
   :code:`.pre-commit-config.yaml` file and change the following line

   .. code-block:: yaml

      language_version: python3.7

   to match your installed version of Python and then setup pre-commit with the
   command

   .. code-block:: sh

      (stylo-xyz123) $ pre-commit install

   .. note::

      Your prompt should look similar to the above as it indicates that your
      virtual environment is active. You can deactivate your virtual environment
      by running the command :code:`exit`

5. Finally start a build of the documentation to ensure everything is working as
   expected

   .. code-block:: sh

      (stylo-xyz123) $ tox -q -e docs-build


That's it! You should now have a functioning development environment and you can
start working on your contribution! Be sure to check out
:ref:`contribute_ref_branching` so that there are no surprises when it comes to
merging in your work when it is ready

.. _Pipenv: https://github.com/pypa/pipenv
.. _pre-commit: https://pre-commit.com/
