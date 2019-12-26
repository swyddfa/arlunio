Python Linting
==============

This action runs all our static analysis tools against the codebase as defined in our
:code:`.pre-commit-config.yaml` file.

Triggers
--------

This action is triggered by any PR that is opened against the
:code:`develop` or :code:`master` branches, unless the changes only affect the blog.

.. literalinclude:: ../../../.github/workflows/python-lint.yml
   :language: yaml
   :start-after: # <trigger>
   :end-before: # </trigger>

Jobs
----

Since static analysis tools only look at the source code without importing or running
anything, it doesn't matter too much which platform / python version they are run on as
long as the tool itself supports it. For the sake of simplcity these checks are run on
the latest version of python and on a linux agent.

.. literalinclude:: ../../../.github/workflows/python-lint.yml
   :language: yaml
   :start-after: # <lint-job>
   :end-before: # </lint-job>

Steps
-----

.. literalinclude:: ../../../.github/workflows/python-lint.yml
   :language: yaml
   :start-after: # <lint-job-steps>
   :end-before: # </lint-job-steps>

This action is fairly straight forword, we checkout the code, setup the python
envrionment and then run our :code:`lint` :term:`tox` envrionment which handles the
details of running the static analysis tools via :term:`pre-commit`