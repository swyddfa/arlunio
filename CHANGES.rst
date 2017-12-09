v0.3.0 2017-12-09
=================

Added
-----

- New Domain class, it is responsible for generating the grids of numbers
  passed to Drawables when they are mapped onto Images. It replaces most of the
  old decorators.
- Drawables are now classes! Any drawable is now a class that inherits from
  Drawable, it brings back much of the old Puppet functionality with some
  improvements.
- More tests!

Changed
-------

- ANDing Images (a & b) has been reimplemented so that it hopefully makes more
  sense. The alpha value of b is used to scale the color values of a.
- Along with the new Domain system mapping Drawables onto Images has been
  reworked to hopefully make coordinate calculations faster

Removed
-------

- stylo/coords.py has been deleted, this means the following functions and
  decorators no longer exist
  + mk_domain - Domains are now a class
  + cartesian (now built into the new Domain object)
  + polar     (now built into the new Domain object)
  + extend_periocally (now the .repeat() method on the new Domain object)
  + translate (now the .transform() method on the new Domain object)
  + reflect (not yet implemented in the new system)

v0.2.3 2017-11-15
==================

Added
-----

- Image objects can now be added together, this is simply the sum of the color
  values at each pixel
- Image objects can now be subtracted, which is simply the difference of the
  colour values at each pixel

Changed
-------

- Renamed hex_to_rgb to hexcolor. It now also can cope with rgb and rgba
  arguments, with the ability to promote rgb to rgba colors


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
