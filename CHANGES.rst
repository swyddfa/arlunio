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
