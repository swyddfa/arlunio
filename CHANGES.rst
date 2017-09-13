[Unreleased]
============

Added
-----

- New Sampler object which forms the basis of the new Driver implementations
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
