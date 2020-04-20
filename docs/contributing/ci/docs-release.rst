Documentation Release
=====================

This action is responsible for building and deploying the documentation which
currently sits alongside the gallery in our Github Pages instance.

Triggers
--------

This action is triggered whenever a commit has been made to the :code:`develop`
branch within the :code:`docs/` or :code:`arlunio/` directories. This means the
documentation is updated to always align with the bleeding edge version of the
codebase. Since we don't currently have a stable released version this is
sufficient for now, though may need to be revised at some point in the future.

.. literalinclude:: ../../../.github/workflows/docs-release.yml
   :language: yaml
   :dedent: 2
   :start-after: # <trigger-push>
   :end-before: # </trigger-push>

It's also configured to run on any pull request that affects the paths relevant
to ensure that changes do not break the build.

.. literalinclude:: ../../../.github/workflows/docs-release.yml
   :language: yaml
   :dedent: 2
   :start-after: # <trigger-pr>
   :end-before: # </trigger-pr>


Jobs
----

.. literalinclude:: ../../../.github/workflows/docs-release.yml
   :language: yaml
   :dedent: 2
   :start-after: # <build-job>
   :end-before: # </build-job>

Steps
-----

Setup
^^^^^

Setup for this job is fairly standard in that we checkout the repository and get
ourselves setup with a Python version. The only interesting thing to note is
that alongside the dependencies listed in :code:`docs/requirements.txt` we also
need to install :code:`arlunio` itself since it's used to build some aspects of
the documentation.

.. literalinclude:: ../../../.github/workflows/docs-release.yml
   :language: yaml
   :dedent: 4
   :start-after: # <build-job-setup>
   :end-before: # </build-job-setup>

Build Docs
^^^^^^^^^^

Since the documentation is built using Sphinx it follows standard practice for
the most part. However before running the Sphinx build we:

- Use towncrier to update the changelog with details of anything that will be
  coming up in the next release.
- Fetch the latest release from Github so we can set the appropriate version
  number in Sphinx

.. literalinclude:: ../../../.github/workflows/docs-release.yml
   :language: yaml
   :dedent: 4
   :start-after: # <build-job-docs>
   :end-before: # </build-job-docs>

Publish Build Artifact
^^^^^^^^^^^^^^^^^^^^^^

So that it's easy to inspect the final build of the documentation if required we
also publish the :code:`docs/_build` directory as a build artifact.

.. literalinclude:: ../../../.github/workflows/docs-release.yml
   :language: yaml
   :dedent: 4
   :start-after: # <build-job-artifact>
   :end-before: # </build-job-artifact>


Deploy Docs
^^^^^^^^^^^

Finally assuming the docs have been built successfully and this is not a PR
build, we deploy the result to Github Pages using
`JamesIves/github-pages-deploy-action`_.

.. literalinclude:: ../../../.github/workflows/docs-release.yml
   :language: yaml
   :dedent: 4
   :start-after: # <build-job-deploy>
   :end-before: # </build-job-deploy>


.. _JamesIves/github-pages-deploy-action: https://github.com/JamesIves/github-pages-deploy-action
