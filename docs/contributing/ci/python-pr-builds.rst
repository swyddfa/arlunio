.. _contrib_ci_python_pr:

Python PR Builds
================

This action defines how PRs that affect the Python code should be evaluated.
At a high level it performs the following checks:

- Builds and tests the code against each supported platform / version of Python
- Produces a :term:`wheel` and an :term:`sdist` and makes them available as a build
  artifact.
- Builds the documentation and makes it available as a build artifact.
- Reports code coverage.

Triggers
--------

Currently this action is triggered by any PR that is opened against the
:code:`develop` or :code:`master` branches, unless the changes only affect the blog.

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
performs.

Setup
^^^^^

.. literalinclude:: ../../../.github/workflows/python-pr.yml
   :language: yaml
   :start-after: # <test-job-setup>
   :end-before: # </test-job-setup>

The first few steps handle checking out the code, setting up Python and
ensuring the tools we need to run the tests are available.


Dev Version Number
^^^^^^^^^^^^^^^^^^

.. note::

   Since we only publish one distribution these steps only run on the latest version of
   python.

.. literalinclude:: ../../../.github/workflows/python-pr.yml
   :language: yaml
   :start-after: # <test-job-version>
   :end-before: # </test-job-version>

So that we have the option of trying out the changes introduced by a PR locally before
accepting it we package up the python code into a :term:`wheel` and make it available as
a build artifact. To ensure that these development builds are not confused with a beta
or real release we adjust the version number to include a :code:`dev<BUILD_NUMBER>`
suffix.

However unlike beta builds we cannot make use of the `einaregilsson/build-number`_
action for PR builds to generate a build number for us. This is due to it requiring
access to the GitHub API token which is unavailable for any build originating from a
fork of the main repository.

Instead we choose the PR number as the build number which we can obtain using a
carefully crafted :code:`sed` command and the :code:`GITHUB_REF` environment variable.
Then we make an environment variable :code:`BUILD_NUMBER` available which can be
referenced by later steps in the job.

Finally using another carefully crafted :code:`sed` command in the next step we rewrite
the version number in the :code:`arlunio/_version.py` file so that it contains the
:code:`dev<BUILD_NUMBER>` suffix.

Tox
^^^
.. literalinclude:: ../../../.github/workflows/python-pr.yml
   :language: yaml
   :start-after: # <test-job-tox>
   :end-before: # </test-job-tox>

Time for the main event, we use :term:`tox` to run all our tests including the doctests
defined in the documentation and the codebase as well as a code coverage report.
Additionally for the latest version of Python we package the code and build the docs in
preparation for them to be uploaded as build artifacts.

Publish Results
^^^^^^^^^^^^^^^

.. literalinclude:: ../../../.github/workflows/python-pr.yml
   :language: yaml
   :start-after: # <test-job-publish>
   :end-before: # </test-job-publish>

Finally we publish all the artifacts generated during the course of the build along with
uploading our code coverage report to `codecov`_

.. note::

   For the same reason that we couldn't make use of the `einaregilsson/build-number`_
   action, uploading of code coverage reports currently doesn't work on PRs coming from
   forks. It's not immediately obvious what the work around should be...

.. _codecov: https://codecov.io
.. _einaregilsson/build-number: https://github.com/einaregilsson/build-number