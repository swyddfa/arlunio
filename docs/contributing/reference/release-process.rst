.. _contribute_ref_release:

The Release Process
===================

This page outlines the release process, what has to be done before a release,
how a release is triggered and how a release actually works. While it's not
essential for every contributor to know the inner workings of a release it is
certainly useful to know as it provides context for some of the decisions made
in our processes such as :ref:`contribute_ref_branching`

There are currently 2 distinct release processes in :code:`stylo`:

- :ref:`contribute_ref_release_docs`: This builds, tests and deploys the
  documentation to `GitHub Pages`_
- :ref:`contribute_ref_release_package`: This builds, tests and deploys
  :code:`stylo` itself to :term:`PyPi`

.. _contribute_ref_release_docs:

Documentation Release
---------------------

A documentation release is triggered everytime a commit is made on the
:code:`develop` branch of the main repository. :term:`Travis` will run all the
tests as normal, then as long as the :code:`docs-build` task completes
successfully it will proceed to publish the new version of the documentation.

For full details on the documentation build process please see
:ref:`this <contribute_ref_docs_build>` article

Below is the current Travis deployment configuration:

.. literalinclude:: ../../../.travis.yml
   :language: yaml
   :start-after: # <publish-docs>
   :end-before: # </publish-docs>
   :dedent: 4

.. attention::

   The box above is extracted from the current :code:`.travis.yml` file. If what
   you read here doesn't match what is shown above, it's most likely that this
   documentation is out of date and an issue should be raised.

- :code:`provider: pages`: We tell Travis that we are deploying a website to
  GitHub Pages
- :code:`skip-cleanup: true`: By default Travis will delete any files generated
  during the build - we obviously don't want that so we skip that step.
- :code:`github-token`: The keys to GitHub
- :code:`local-dir`: Which directory contains the site
- :code:`verbose`: Tell Travis to print more about what it is doing.
- :code:`on`: Only do the release when the following conditions are met.

  - :code:`branch`: The build is running on the develop branch
  - :code:`condition: $TOXENV = docs-build`: It only makes sense to publish when
    we have built the documentation.
  - :code:`python`: Only on the given version of python.

It's also worth mentioning that the way Travis deploys the website is by force
pushing the generated HTML to the :code:`gh-pages` branch on the main
repository. I assume that's a good thing since it is the default.

.. note::

   Currently the documentation is unversioned, whenever an update is available
   it is published. This probably doesn't matter too much right now as the
   documentation is still very much under development. However this does mean
   that the documentation may pull ahead of the version of :code:`stylo` that is
   generally available which would lead to confusion. This should be changed
   sometime in the future.


.. _contribute_ref_release_package:

Package Release
---------------

A package release is triggered whenever a commit it made on the :code:`master`
branch of the main repository. :term:`Travis` will run all the tests as normal
and if the :code:`py36` task completes successfully then it will package and
publish :code:`stylo` to :term:`PyPi`.

However unlike the documentation release which is quite informal, there are a
number of things that need to be done before and after a package release

Drafting a Release
^^^^^^^^^^^^^^^^^^

A draft release is made by opening a PR from the :code:`develop` branch onto the
:code:`master` branch of the main repository. In order for this PR to become a
proper release the following must be satisfied

- All the code, docs, tests etc that are to be included in the release have been
  merged onto the :code:`develop` branch.
- The :code:`stylo/_version.py` has been updated to the latest version number.
- The :code:`CHANGES.rst` file has been updated to include a summary of the
  changes included in the release. **On the day of the merge the release
  title is updated to include the date and version of the release**
- All the tests pass and Travis is happy.

If all is well and whoever is looking after the release is happy, then the PR
can be merged which will kick off the release process.

The Release
^^^^^^^^^^^

The process from when the PR is merged to the moment the latest :code:`stylo`
package turns up on PyPi is entirely automated. Travis will rerun all the tests
after the merge and then proceed to package and publish the new version.

.. todo::

   Link to the article explaining the code related build processes, when it is
   available.

Below is the current Travis configuration

.. literalinclude:: ../../../.travis.yml
   :language: yaml
   :start-after: # <publish-package>
   :end-before: # </publish-package>
   :dedent: 4

.. attention::

   The box above is extracted from the current :code:`.travis.yml` file. If what
   you read here doesn't match what is shown above, it's most likely that this
   documentation is out of date and an issue should be raised.

- :code:`provider: pypi`: Tell Travis that we are publishing a package to PyPi
- :code:`distributions`: We want to publish both the source and a compiled wheel
- :code:`user`, :code:`password`: PyPi credentials.
- :code:`on`: Only do the release if the following conditions are met.

  + :code:`condition: py36`: We only need to publish the package once, so we're
    currently using the Python 3.6 build.
  + :code:`python: 3.6`: Possibly a redundant condition? But since it works it
    doesn't seem worth the risk to take it out.
  + The build is on the master branch (an implicit default).

The package and its contents are defined by the :code:`setup.py` file at the
root of the repository.

.. todo::

   Link to the article explaining the setup file when it's written.

After the Release
^^^^^^^^^^^^^^^^^

.. image:: /_static/new-release.png
   :align: center
   :width: 75%

After the PR has been merged there is one last manual step to be done and that
is to create a `release <https://github.com/alcarney/stylo/releases>`_ on
GitHub.

After clicking on the :code:`Draft a new release` button on the releases page
you are taken to a page as shown above where the following fields need to be
filled in.

- The version string needs to be put in the tag name box
- **The branch needs to be changed to master**
- The title of the release needs to be copied over from the :code:`CHANGES.rst`
  file
- The changes for the release need to be copied over from the :code:`CHANGES.rst`
  and pasted into the body. *Note: You will need to convert the text from rst to
  markdown*

Once it has been filled out click the green :code:`Publish release` button and
you are done!

.. note::

   It is the hope that this step can also be automated, by having something like
   a webhook trigger on the merge to master we can use the GitHub API to
   automatically create the release notice.


.. _GitHub Pages: https://pages.github.com/
