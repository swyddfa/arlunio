.. _contribute_docs_build:

Building the Documentation
==========================

.. note::

   You **do not** have to understand how the docs are built in order to contribute to
   them! We have a single command to take care of it for you :code:`tox -e docs`. Check
   out this page for more information.

If you have looked at the :ref:`contribute_reference_tox_ini` file, you might have
noticed that the documentation build is the most complicated. This is due to the fact a
number of tasks have been automated - at the cost of being more complicated to build.

Building the documentation involves the following steps:

1. Generating the :ref:`api_reference` section using the :ref:`contribute_reference_apidoc`
