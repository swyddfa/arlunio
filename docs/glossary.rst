Glossary
========

Mathematics
-----------

.. glossary::
   :sorted:

   cartesian coordinates
      The "standard" coordinate system that (in 2D) uses two variables :math:`(x, y)`
      to address a point in space. Can be thought of as going
      *"along the corridor and up the stairs"*. See :ref:`math_cartesian_coordinates`

   polar coordinates
      An alternate coordinate system that (in 2D) uses two variables :math:`(r, \theta)`
      to address a point in space. Useful for curves and circular objects.
      See :ref:`math_polar_coordinates`

   linear interpolation
      TBW

   transpose
       Transposing a matrix is the act of flipping the matrix around its principal
       diagonal. *All the columns become rows and the rows become columns*.

Software Development
--------------------

.. glossary::
   :sorted:

   docstrings
      docstrings are a special kind of comment in Python and are typically found
      at the start of functions and classes. They outline what the purpose of
      the object/class is, what input it expects and what it returns along with
      any errors it may raise.

   git
      `Git <https://git-scm.com/>`_ is a tool used to manage multiple versions
      of documents stored on multile computers. It allows us to see the history
      of every file in the repository and be able to copy changes between each
      other without going insane. While very powerful it does have a reputation
      for being hard to understand.

   linting
      Linting in software development is the process of running one or more tools
      against a codebase that search for potential issues. Examples include undefined
      variables or enforcing stylistic conventions such as line length.

   PyPi
      `PyPi <https://pypi.org/>`_ is the Python Package Index. Any python
      package that you can :code:`pip install` is hosted here.

   static analysis
      Static analysis tools such as `flake8 <http://flake8.pycqa.org/en/latest/>`_
      are tools that try to detect errors in your code simply by reading the
      source code.

   tox
      `tox <https://tox.readthedocs.io/en/latest/>`_ is tool commonly found in
      Python projects that automates the process of running various tasks
      against multiple Python versions or environments.

   Travis
      `Travis <https://travis-ci.org>`_ is a continuous integration service that
      will automatically run the tests whenever changes are made to the
      repository and will report on any failures. It can also be configured to
      handle releases.

   virtual environments
      A virtual environment is an isolated installation of Python that can have
      its own collection of packages installed and is completely independent of
      the host machine's Python installation. They are highly recommended when
      working on projects as they stop conflicts when you need multiple versions
      of the same package installed.
      installed
