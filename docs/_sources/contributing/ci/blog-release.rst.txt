Blog Release
============

This action is responsible for building and deploying the blog component of the
arlunio website. Currently this is only composed of the gallery.

Triggers
--------

This action is triggered whenever a commit has been made to the :code:`develop`
branch within the :code:`blog/` directory so that new additions are published
immediately.

.. literalinclude:: ../../../.github/workflows/blog-release.yml
   :language: yaml
   :dedent: 2
   :start-after: # <trigger-push>
   :end-before: # </trigger-push>

It is also configured to run everyday at :code:`06:00` so that we can ensure the
gallery still builds and to keep it fresh. The fairly cryptic syntax can be
visualised by visting the `crontab.guru`_ site.

.. literalinclude:: ../../../.github/workflows/blog-release.yml
   :language: yaml
   :dedent: 2
   :start-after: # <trigger-cron>
   :end-before: # </trigger-cron>

Finally we also trigger this action on every PR that makes changes to the
:code:`blog/` directory to ensure any additions won't break the build.

.. literalinclude:: ../../../.github/workflows/blog-release.yml
   :language: yaml
   :dedent: 2
   :start-after: # <trigger-pr>
   :end-before: # </trigger-pr>

Jobs
----

We only need to build the site once and deploy it so we only need to run it with
a single instance.

.. literalinclude:: ../../../.github/workflows/blog-release.yml
   :language: yaml
   :dedent: 2
   :start-after: # <build-job>
   :end-before: # </build-job>

Steps
-----

Setup
^^^^^

We start off with the basics, checking out the repo, configuring the build
environment etc. Notice that we install the pre-release version of
:code:`arlunio`, this is so we can see if any changes are going to break any
uses cases currently covered by the gallery.

.. literalinclude:: ../../../.github/workflows/blog-release.yml
   :language: yaml
   :dedent: 4
   :start-after: # <build-job-setup>
   :end-before: # </build-job-setup>

Build Blog
^^^^^^^^^^

As mentioned above the only component currently in the blog is the gallery,
which we will build now. The details of this are handled by the
:code:`gallery.py` script that is not detailed here.

.. literalinclude:: ../../../.github/workflows/blog-release.yml
   :language: yaml
   :dedent: 4
   :start-after: # <build-job-blog>
   :end-before: # </build-job-blog>

Delpoy Blog
^^^^^^^^^^^

Finally, if this is not a PR build, we publish the built site to our
:code:`gh-pages` branch using `JamesIves/github-pages-deploy-action`_.

.. literalinclude:: ../../../.github/workflows/blog-release.yml
   :language: yaml
   :dedent: 4
   :start-after: # <build-job-deploy>
   :end-before: # </build-job-deploy>


.. _crontab.guru: https://crontab.guru/#0_6_*_*_*
.. _JamesIves/github-pages-deploy-action: https://github.com/JamesIves/github-pages-deploy-action


