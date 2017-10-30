v0.2.2 - 2017-10-30
===================

Added
-----

- Keyword argument 'only' to the 'polar' decorator which allows you to ignore
  the x and y variables if you dont need them

Fixed
-----

- Forgot to expose the objects from interpolate.py to the top level stylo
  import
- Examples in the documentation and enabled doctests for them

v0.2.1 - 2017-10-29
===================

Fixed
-----
- Stylo should now also work on python 3.5

Removed
-------
- Deleted stylo/motion.py as its something better suited to a plugin
- Deleted Pupptet, PuppetMaster and supporting functions as they are broken and
  better to be rewritten from scratch


v0.2.0 - 2017-10-27
===================

Added
-----

- Sampler object which forms the basis of the new Driver implementations
- Channel object which can manage many Sampler-like objects to form a
  single 'track' of animation data
- A very simple Driver object which allows you to collect multiple Channel
  objects into a single place
- linear, quad_ease_in, quad_ease_out interpolation functions

Docs
^^^^

-Added the following reference pages
    + Image
    + Drawable
    + Primitive
    + Sampler
- A How-To section
- How-To invert the colours of an Image

Changed
-------
- Image.__and__() now uses a new method which produces better results with
  colour images

Fixed
-----
- Numpy shape error in Image.__neg__()

Removed
-------
- stylo.prims.thicken was redundant so it has been removed


v0.1.0 - 2017-08-02
===================

Initial Release
