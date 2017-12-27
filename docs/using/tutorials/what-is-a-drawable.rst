What is a Drawable?
===================

A drawable is an abstract representation of a shape that can be drawn onto
Image objects. They are made up of three things:

- A **Domain** - where in 2D space does this shape exist?
- A **Mask** - this is a function that determines which points in the defined
  domain are in the shape.
- A **Color Mapping** - another function which takes the points selected by the
  mask function and determines what colour they should have

The Domain
==========

The domain can be thought of as the "window" we look through to see the shape.
It focuses our attention into a rectangular region of space where our shape
lives.
