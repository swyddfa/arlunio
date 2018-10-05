.. _contribute_ref_branching:

The Branching Policy
====================

.. attention::

   This page assumes that you are confortable with using git.

The Golden Rule
---------------

If there is one thing you take away from this page it is this **we never work on
master**.

We never do any work directly on the :code:`master` branch because the release
process (explained in much greater detail :ref:`here <contribute_ref_release>`)
is set up to automatically package and publish code that is committed to the
:code:`master` branch.

So that we don't accidentally publish broken or work in progress code we do all
our work based on the :code:`develop` branch. The only time a commit is made to
the master branch is when a new release of :code:`stylo` is made. Again it's
recommended that you read :ref:`contribute_ref_release` page for more information
on this process.

Our Recommendations
-------------------

.. todo::

   Link to various articles explaining some of these steps in more detail when
   they are written.

.. tip::

   Git can get very scary, very quickly. If you are having trouble with it at any
   stage you can always drop a message in the
   `chatroom <https://gitter.im/stylo-py/Lobby>`_ we'll always be happy to help.

With that out of the way here is the recommended workflow when making changes to
the repository.

1. Make sure you have the :code:`develop` branch checked out and that it is up
   to date with the latest in the main repository.
2. Create a new branch to do your work on. It helps if you choose name that
   indicates the sort of work you intend to do e.g. :code:`add-new-shape` or
   :code:`fix-issue-123`
3. Make whatever changes and commits you need to complete the task.
4. When you have finished, update your :code:`develop` branch to the
   latest and rebase your work on top of it.
5. Push your changes up to your fork and open a PR against the :code:`develop`
   branch on the main repository.

Don't worry if you're not using git "perfectly" at the end of the day it is a
tool used for bookkeeping and the process outlined above is only a
recommendation. What's more important is your contribution so focus on that we
can always guide you through the bookkeeping steps when it comes to getting your
contribution merged.
