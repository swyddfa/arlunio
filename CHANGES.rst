[Unreleased]
============

Added
-----

Docs
^^^^
- Initial draft of Image class reference
- Initial draft of Drawable class reference
- Initial draft of Primitive reference page
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
- stylo.prims.thicken was redundant so its been removed


v0.1.0 - 2017-08-02
===================

Initial Release
