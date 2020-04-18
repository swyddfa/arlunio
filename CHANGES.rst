v0.0.6 - 2020-04-18
===================

Features
--------

- Introduce the concept of operators. Operators are definitions that can provide
  implementations of the arithmetic operators in Python like :code:`+` and
  :code:`-`. Depending on the type a definition produces different operators can
  be defined that allow them to be combined in some way. The standard library has
  been updated to incorporate a few operators for working with masks. (`#207 <https://github.com/swyddfa/arlunio/issues/207>`_)
- Generalise definitions to accept any "regular" value as an input, not just
  :code:`width` and :code:`height`. In a similar way to attributes, when deriving
  from other definitions any inputs will be automatically inherited. (`#216 <https://github.com/swyddfa/arlunio/issues/216>`_)


Docs
----

- Added some documentation around the CI build for the blog. Also updated the blog
  build to run every day. (`#177 <https://github.com/swyddfa/arlunio/issues/177>`_)
- Tidied up and updated existing changelog, started using towncrier for changelog
  entries going forward. (`#204 <https://github.com/swyddfa/arlunio/issues/204>`_)
- Flatten structure of the User Guide section and add placeholder first tutorial (`#205 <https://github.com/swyddfa/arlunio/issues/205>`_)


Misc
----

- Fix handling of multiple notebooks in  :code:`clean-notebook.sh` and add VSCode
  tasks to aid with tutorial development (`#205 <https://github.com/swyddfa/arlunio/issues/205>`_)
- Switch the linting workflow to explicitly list the paths that should trigger a
  build. (`#210 <https://github.com/swyddfa/arlunio/issues/210>`_)
- Fix packaging so that our tests are no longer installed (`#216 <https://github.com/swyddfa/arlunio/issues/216>`_)


v0.0.5 - 2020-03-18
-------------------
Added
^^^^^
- :code:`Empty` and :code:`Full` definitions
- :code:`normalise`, :code:`clamp` and :code:`lerp` functions

Changed
^^^^^^^
- Definitions now have a :code:`produces` classmethod that will report the type
  of object they produce - assuming that the type annotation has been given of
  course.
- The :code:`ar.definition` decorator now accurately reports the module a
  definition was defined in.

v0.0.4 - 2020-02-15
-------------------

Added
^^^^^

- The concept of a :code:`Definition`.

  + This incorporates the existing concept of a :code:`Shape` and expands on it
    to cover input parameters and more
  + Definitions can be derived from other definitions by passing in existing
    definitions as positional arguments. Derived definitions will inherit all
    attributes from their "parent" definitions.

Removed
^^^^^^^
- The "magic" shape entry point, shapes should now be imported like regular
  Python classes.

v0.0.3 - 2019-12-30
-------------------

Added
^^^^^
- :code:`Pixelize` shape that can take another shape and and render a lower res
  version of that shape giving it a pixel art vibe
- :code:`Map` shape that can take a grid of values representing some layout and
  a dictionary that maps those values to shapes that should be drawn there.
- Proof of concept notebook importer

Changed
^^^^^^^

- Add :code:`mkdirs` flag to the :code`Image.save` function to have the option
  of automatically creating any required parent directories
- Tweak the :code:`find_notebook` function to handle the way we are using it
  in the gallery

v0.0.2 - 2019-09-04
-------------------

- Release to test new CI/CD setup

v0.0.1 - 2019-08-04
-------------------

- Stylo has been renamed to Arlunio, resetting the version number
- Initial release to secure the name, more to follow
