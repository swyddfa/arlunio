.. _contribute_get_started_releases:

The Release Process
===================

This page outlines the release process, what has to be done before a release,
how a release is triggered and how a release actually works. While it's not
essential for every contributor to know the inner workings of this process it is
certainly useful to know as it has an impact on other areas such as the
:ref:`contribute_get_started_git_branching`

There are currently 2 dictinct release processes in :code:`stylo` there is the
release that publishes the documentation you are reading now and there is the
package release that publishes :code:`stylo` to PyPi and makes it generally
available.

Documentation Release
---------------------

The documentation release is not as formal as the package release as there is
less ceremony around making a release. At its core the release is as simple as
it can get, the docs are written and the docs are published.

A documentation release is triggered everytime a commit is made on the
:code:`develop` branch on the main repository and is handled by :term:`Travis`

.. note::

   There is currently no concept of version in the documentation the published
   version always reflects the most recent state of the repository and therefore
   can contain information on features not currently available. This should
   probably be changed sometime in the future.
