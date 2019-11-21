Python PR Builds
================

This action defines how PRs that affect the Python code should be evaluated.
At a high level it performs the following checks:

- Builds and tests the code against each supported platform / version of Python
- Builds the documentation
- Produces a :code:`whl` package and makes it available as a build artifact.
- Reports code coverage

Triggers
--------

Currently this action is triggered by any PR that is opened against the
:code:`develop` or :code:`master` branches. At some point this should probably be
made smarter to only run if there have been changes that affect the codebase.

.. literalinclude:: ../../../.github/workflows/python-pr.yml
   :language: yaml
   :start-after: # <trigger>
   :end-before: # </trigger>

Jobs
----

To ensure that a PR doesn't introduce any breaking changes we need to run the test
suite against each supported platform and python version. To do this we make use of the
:code:`matrix` strategy which spawns a job for each combination of :code:`os` and
:code:`python-version`

.. literalinclude:: ../../../.github/workflows/python-pr.yml
   :language: yaml
   :start-after: # <test-job>
   :end-before: # </test-job>

Steps
-----

With the preliminaries out of the way, time to focus on the actual work this action
performs. The first few steps handle checking out the code, setting up Python and
ensuring the tools we need to run the tests are available.

.. literalinclude:: ../../../.github/workflows/python-pr.yml
   :language: yaml
   :start-after: # <test-job-setup>
   :end-before: # </test-job-setup>