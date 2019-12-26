Python Release
==============

This action is responsible for making releases of the Python code, both the beta
builds based on the :code:`develop` branch or "real" releases that are based on
the :code:`master` branch.

Triggers
--------

This action is triggered whenever a commit is made to the :code:`develop` or
:code:`master` branches - either directly when a PR is merged.

.. literalinclude:: ../../../.github/workflows/python-release.yml
   :language: yaml
   :start-after: # <trigger>
   :end-before: # </trigger>

Jobs
----

Since code has to be contributed via a PR against the relevant branch, testing across
all the supported Python versions and platforms will already have been handled by the
:ref:`contrib_ci_python_pr` action. Also as this project consists of pure
Python code we can produce a single wheel and have it work across all platforms, so it
is enough to have our release process run on a single platform, python version
combination.

.. literalinclude:: ../../../.github/workflows/python-release.yml
   :language: yaml
   :dedent: 2
   :start-after: # <release-job>
   :end-before: # </release-job>

Steps
-----

Setup
^^^^^

As with the other actions, the first few steps are all about checking out the code and
setting up the environment.

.. literalinclude:: ../../../.github/workflows/python-release.yml
   :language: yaml
   :dedent: 4
   :start-after: # <release-job-setup>
   :end-before: # </release-job-setup>

Beta Version Number
^^^^^^^^^^^^^^^^^^^

So that there is the option of testing/playing with the upcoming release of
:code:`arlunio` as it is being developed, we publish a beta release that includes a
beta signifier in the version number. So that we get an unique version number for each
build we make use of the `einaregilsson/build-number`_ action to generate that for us.

We can then modifiy :code:`arlunio`'s version number in :code:`arlunio/_version.py` to
include the beta tag.

.. literalinclude:: ../../../.github/workflows/python-release.yml
   :language: yaml
   :dedent: 4
   :start-after: # <release-job-version>
   :end-before: # </release-job-version>

Export Release Info
^^^^^^^^^^^^^^^^^^^

One of the tasks performed by this workflow is to create a GitHub release so we
have a step that exposes the version number and release date to the rest of the
workflow. This makes use of the `set-env`_ and `set-output`_ commands available to an
action.

.. literalinclude:: ../../../.github/workflows/python-release.yml
   :language: yaml
   :dedent: 4
   :start-after: # <release-job-info>
   :end-before: # </release-job-info>

Exposing the results as an environment variable means that the values are available to
subsequent script blocks while a step's output is available to be used as an argument to
some YAML field.

Notice how we're giving this step an explicit :code:`id`, we'll use this later when
referencing the exposed values.

Build Wheel Package
^^^^^^^^^^^^^^^^^^^

Time to build the :term:`wheel` package that we upload to :term:`PyPi`, the details of
which are handled by the :code:`pkg` :term:`tox` environment.

.. literalinclude:: ../../../.github/workflows/python-release.yml
   :language: yaml
   :dedent: 4
   :start-after: # <release-job-pkg>
   :end-before: # </release-job-pkg>

Export Release Assets
^^^^^^^^^^^^^^^^^^^^^

In order to make the :term:`whl` and :term:`sdist` packages available on the releases
page they have to be uploaded by the `actions/upload-release-asset`_ action which in
turn requires us to know the filepath(s) that we're going to publish.

.. literalinclude:: ../../../.github/workflows/python-release.yml
   :language: yaml
   :dedent: 4
   :start-after: # <release-job-assets>
   :end-before: # </release-job-assets>

Notice how we're giving this step an explicit :code:`id`, we'll use this later when
referencing the exposed values

Tag Release
^^^^^^^^^^^

Time to start preparing the release object in GitHub itself by creating a tag for the
new version number which we will reference in the next step. At the time of writing the
easiest way to do this appears to be just call the GitHub API directly.

.. literalinclude:: ../../../.github/workflows/python-release.yml
   :language: yaml
   :dedent: 4
   :start-after: # <release-job-tag>
   :end-before: # </release-job-tag>

To ensure we get the repository name right we can reference the `github context`_

Create Release
^^^^^^^^^^^^^^

Now that we have something to reference we can go ahead and create a formal release in
GitHub. Depending on if the build is taking place on :code:`develop` or :code:`master`
the release will be tagged as a pre-release by checking the `github context`_

.. literalinclude:: ../../../.github/workflows/python-release.yml
   :language: yaml
   :dedent: 4
   :start-after: # <release-job-create>
   :end-before: # </release-job-create>

We also extract the version number and release date from our earlier :code:`info` step
via the `steps context`_. Also notice how we're giving this step an explicit :code:`id`,
we'll use this later when we upload the release assets

Upload Release Assets
^^^^^^^^^^^^^^^^^^^^^

With the release created we can now upload all the assets we want to publish as part of
release. Currently this is just the :term:`sdist` and :term:`whl` distributions

.. literalinclude:: ../../../.github/workflows/python-release.yml
   :language: yaml
   :dedent: 4
   :start-after: # <release-job-upload>
   :end-before: # </release-job-upload>

Publish Package to PyPi
^^^^^^^^^^^^^^^^^^^^^^^

Finally time to make :code:`arlunio` pip installable by uploading it to :term:`PyPi`.
the details of which are handled by the `twine`_ project. The only thing we have to do
is provide the :code:`twine` command with the required credentials stored in GitHub
secrets.

.. literalinclude:: ../../../.github/workflows/python-release.yml
   :language: yaml
   :dedent: 4
   :start-after: # <release-job-pypi>
   :end-before: # </release-job-pypi>

.. _actions/upload-release-asset: https://github.com/actions/upload-release-asset
.. _einaregilsson/build-number: https://github.com/einaregilsson/build-number
.. _github context: https://help.github.com/en/actions/automating-your-workflow-with-github-actions/contexts-and-expression-syntax-for-github-actions#github-context
.. _set-env: https://help.github.com/en/actions/automating-your-workflow-with-github-actions/development-tools-for-github-actions#set-an-environment-variable-set-env
.. _set-output: https://help.github.com/en/actions/automating-your-workflow-with-github-actions/development-tools-for-github-actions#set-an-output-parameter-set-output
.. _steps context: https://help.github.com/en/actions/automating-your-workflow-with-github-actions/contexts-and-expression-syntax-for-github-actions#steps-context
.. _twine: https://pypi.org/project/twine
