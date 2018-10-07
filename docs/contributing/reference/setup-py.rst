.. _contribute_ref_setup_py:

The Setup.py File
=================

The :code:`setup.py` file is what the packaging tools use to determine what
should go into :code:`stylo` when it is packaged as well as define any metadata
about the project itself.

Here is the contents of that file

.. literalinclude:: ../../../setup.py
   :language: python

While we won't go through absolutely everything, here are some of the highlights

.. attention::

   The box above contains the current version of :code:`setup.py` extracted from
   the file itself. If what you read below doesn't match up then it's an
   indication that this page is out of date and an issue should be raised.

Package Metadata
----------------

Name, Version, Description
^^^^^^^^^^^^^^^^^^^^^^^^^^

Some standard info about the project, such as its :code:`name`. The
:code:`version` is set to the value of the :code:`__version__` string from the
:code:`stylo/_version.py` file so that it is always up to date. There is also a
one line :code:`description` about what :code:`stylo` does.

There is also a :code:`long_description` field, this is what will be displayed
on the `project <https://pypi.org/project/stylo/>`_ page on :term:`PyPi` this is
generally a project's README file. Since the :code:`setup.py` is just regular
python code we write a :code:`readme()` function to read the contents of the
:code:`README.rst` file so that this field is always up to date.

Authors, License, Classifiers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :code:`author` and :code:`author_email` fields give you some idea about the
people behind the project and a way to get in touch.

The :code:`license` field tells you what license :code:`stylo` is available
under and dictates what you can and can't do with the code. :code:`stylo` is
available under the `MIT License`_ and since I'm not a lawyer I recommend you
follow the link if you want to know what the terms of the license are all about.

Then we have a number of :code:`classifiers`, these are tags that help indicate
the current state of the project. This can range from anything from the versions
of Python that are supported to the license the project is available under.
There are *many* classifiers to choose from
`here <https://pypi.org/pypi?%3Aaction=list_classifiers>`_ is a full list for
those who are interested.

.. note::

   There needs to be a conversation about when people are considered to be
   "core" contributors and therefore should be added to the authors list.

Packages & Requirements
^^^^^^^^^^^^^^^^^^^^^^^

Here we get into what is included in the package, we use the
:code:`find_packages` function to automatically discover the python files inside
the :code:`stylo` folder that need to be included.

We also need to specify our dependencies in the :code:`install_requires` field
so that when people :code:`pip install stylo` all of the required packages are
discovered and installed.

Those with a keen eye should notice that packages like :code:`hypothesis` and
:code:`pytest` are not typically installation requirements as they are testing
tools and only required by developers. Normally you would be right, however
:code:`stylo` does distribute a number of tests as part of the
:code:`stylo.testing` package as part of our extension guarantee. Since these
packages are required to import objects from this package we include them as
installation dependencies.

Finally the :code:`python_requires` field specifies the minimum version that we
support.

Miscellaneous Fields
^^^^^^^^^^^^^^^^^^^^

The :code:`setup-requires` and :code:`test_suite` fields are a holdover from
previous versions of :code:`stylo` where the tests were run using the command
:code:`python setup.py test`. I am not sure if they are required anymore.

I am not sure what the :code:`zip_safe` and :code:`include_package_data` fields
are for.

.. _MIT License: https://opensource.org/licenses/MIT
