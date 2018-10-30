.. _contribute_ref_docs_build:

The Documentation Build Process
===============================

This page describes the build process for the documentation in detail. If you
are only looking for the command to build the documentation it is the following:

.. code-block:: sh

   $ pipenv run docs

If however you need to know more details about the build process or are simply
curious then please read on!

Introducing tox
---------------

We use :term:`tox` to build our documentation as it will handle the installation
of the dependencies and give us more control over the environment in which they
are built.

The build is handled by the :code:`docs-build` environment and is defined in the
:code:`tox.ini` file at the root of the repository. The command given at the top
of this page is a shortcut for the real but more cryptic command to build the
documentation which is:

.. code-block:: sh

   $ pipenv run tox -q -e docs-build

Below is the complete build definition.

.. literalinclude:: ../../../tox.ini
   :start-after: # <docs-build>
   :end-before: # </docs-build>

.. note::

   Unlike the rest of this document, the box above is extracted from the current
   version of :code:`tox.ini` and will always be up to date. If what you read
   on this page doesn't match, that's most likely a sign that this page is
   out of date and an `issue <https://github.com/alcarney/stylo/issues/new>`_
   should be raised.

Declaring Dependencies
----------------------

Using the :code:`deps` variable we declare to tox which dependencies we need
installed into the environment in order to build the documentation.

- `Sphinx`_: This does the bulk of the work, compiling :code:`.rst` files in the
  :code:`docs/` folder into a HTML website that we can publish.
- `topos-theme`_: Sphinx can be extended in a number of ways, one of these is
  via custom HTML themes. :code:`topos-theme` extends Sphinx to provide the
  theme that controls how this site appears.
- `pytest`_: Not something you would typically see in a docs build, pytest
  is used to run a number of test files that generate most of the example images
  you see on this site.

We also make use of the :code:`whitelist_externals` variable to suppress
warnings about using the :code:`echo` command that is not part of the
environment.

Build Overview
--------------

The build breaks down into the following stages.

1. The :term:`docstrings` are converted into the :ref:`api_reference` section
2. All the links are checked to ensure that they are not broken
3. Any :code:`testsetup::`, :code:`testcode::` or :code:`doctest::` sections are
   executed to ensure that they work.
4. Finally the documentation is built into a HTML website ready for publishing.


Building the API Reference
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sh

   python scripts/apidoc.py -m stylo -o docs/api

Writing the :ref:`api_reference` section is entirely automated. The
:code:`apidoc.py` searches through the :code:`stylo` package for all the python
modules and generates an rst file for each one containing an
:code:`.. automodule::` definition.

The `autodoc`_ Sphinx extension then extracts the docstrings from each item in
those modules and uses them to write the documentation you see in the API
Reference section.

For full details on the :code:`apidoc.py` script please see the
:ref:`contribute_reference_apidoc` page.

.. note::

   While Sphinx does come with an :code:`sphinx-apidoc` command that acheives
   the same goal as this script it produces an output that doesn't quite work
   with the format of this site. By writing our own script we have more control
   over the output can can modify it as needed.


Building the Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sh

   sphinx-build -M linkcheck ./docs ./docs/_build -E -a -j auto
   sphinx-build -M doctest ./docs ./docs/_build -E -a -j auto
   sphinx-build -M html ./docs ./docs/_build -E -a -j auto

This is where the bulk of the work happens, everything up until now has been
prep work. If you were to stop the build before these commands run you would
still only have a :code:`docs/` folder full of images and rst files. The only
thing the previous commands are doing is generating the rst files we don't have
to write by hand. With these three commands we pass everything off to Sphinx and
let it generate the website.

Sphinx comes with a number of `builders`_ a builder takes your documentation and
performs a task with it. These tasks can be anything from generating an
:code:`epub` to an XML representation of your documents.

Our build uses 3 builders:

- :code:`linkcheck`: This looks at all the links in the documentation and checks
  to ensure that they are not broken
- :code:`doctest`: The looks for code examples contained in the following
  directives:

  + :code:`.. testsetup::`
  + :code:`.. testcode::`
  + :code:`.. testoutput::`
  + :code:`.. testcleanup::`
  + :code:`.. doctest::`

  It then runs all the code it can find and will fail the build if the code does
  not work as described.
- :code:`html`: The main event, this produces the HTML website found in the
  :code:`docs/_build/html` directory which we publish to GitHub Pages.


.. _autodoc: http://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
.. _builders: http://www.sphinx-doc.org/en/stable/usage/builders/
.. _Sphinx: http://www.sphinx-doc.org/en/master/
.. _pytest: https://docs.pytest.org/en/latest/
.. _topos-theme: https://topos-theme.readthedocs.io/en/latest/
