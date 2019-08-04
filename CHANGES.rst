v0.0.1 - 2019-08-04
-------------------

- Stylo has been renamed to Arlunio, resetting the version number
- Initial release to secure the name, more to follow

Archive
-------

These previous releases are no longer relevant to the project, but have been
left in for historical interest

v0.9.3 - 2019-01-12
^^^^^^^^^^^^^^^^^^^

Changed
"""""""

^ When adding layers the :code:`LayeredImage` now accepts the color as a
  string automatically converting it to a :code:`FillColor` behind the scenes.

v0.9.2 - 2019-01-07
^^^^^^^^^^^^^^^^^^^

Changed
"""""""

^ Most commonly used objects have been imported into the top level namespace.
  This means that it is now possible to write code like the following.

  .. code^block:: python

     import stylo as st

     black = st.FillColor()
     circle = st.Circle(fill=True)

     image = st.SimpleImage(circle, black)

^ The way stylo has been packaged has been changed. It now comes with a couple
  of "extras". Instead of requiring dependencies for everything, the default
  installation now only contains the packages that are absolutely required to
  run stylo.

  The other dependencies have been split into a couple of extras

  + :code:`testing`: The dependencies required to import items from the
    `stylo.testing` package.
  + :code:`jupyer`: Dependencies required to use stylo interactively in a
    jupyter notebook.

v0.9.1 - 2018-12-27
^^^^^^^^^^^^^^^^^^^

There are no changes.

This release is a test to ensure that internal changes to how :code:`stylo` is
packaged and deployed are working correctly.

v0.9.0 - 2018-11-11
^^^^^^^^^^^^^^^^^^^

Added
"""""

^ New :code:`stylo.math` module! Currently it contains a :code:`lerp`
  function to do linear implementation between two values :code:`a` and
  :code:`b`
^ New :code:`stylo.design` module! This is the start of the "next level" in
  styo's API abstracting away from the lower level objects such as shapes and
  colormaps.

  ^ This module adds the notion of a parameter group, this is a collection of
    values that can be passed into functions as a single object using the
    dictionary unpacking syntax (:code:`**params`)

    Parameter groups are defined using the :code:`define_parameter_group`
    function and taking a name and a comma separated string of parameter names.
    There is also :code:`define_time_dependent_parameter_group` that can be
    used to define a parameter group that depends on time.

    Currently there are two pre^defined paramters groups, :code:`Position` and
    :code:`Trajectory`. They both combine the :code:`x` and :code:`y` values
    into a single object, with the second being the time dependent version of
    the first.

    Finally there are two built^in implementations of these parameter groups.
    :code:`StaticPosition` and :code:`ParametricPosition` the first takes two
    values and returns them. The second takes two functions in time and calls
    them at each supplied time value.


v0.8.0 - 2018-11-07
^^^^^^^^^^^^^^^^^^^

Added
"""""

^ New :code:`Timeline` system! This finally introduces explicit support for
  animations to :code:`stylo.`

v0.7.0 - 2018-10-25
^^^^^^^^^^^^^^^^^^^

Added
"""""

^ New :code:`Line` shape!
^ New :code:`ImplicitXY` shape! Draw any curve that is implicitly defined by a
  function :math:`f(x, y)`

Changed
"""""""

^ The :code:`Circle` and :code:`Ellipse` shapes now take more arguments. By
  default the shapes will now draw an outline rather than a filled in shape.

v0.6.1 - 2018-10-20
^^^^^^^^^^^^^^^^^^^

Added
"""""

^ New :code:`preview` keyword argument to images, set this to :code:`False` if
  you don't want a matplotlib figure returned.
^ New :code:`encode` keyword argument to images, setting this to :code:`True`
  will return a base64 encoded string representation of the image in PNG format.

Fixed
"""""

^ Preview images are no longer displayed twice in jupyter notebooks
^ Preview images no longer display the x and y axis numbers.

v0.6.0 - 2018-10-07
^^^^^^^^^^^^^^^^^^^

Added
"""""

**Users**

^ New :code:`Triangle` shape
^ Shapes can now be inverted using the :code:`~` operator.

**Contributors**

^ Added new shape :code:`InvertedShape` which handles the inversion of a shape
  behind the scenes.
^ Tests for all the composite shapes and operators.
^ More documentation on how to get involved

Changed
"""""""

**Users**

^ Shapes now have defined :code:`__repr__` methods, including shapes that have
  been combined, where a representation of a tree will be produced showing how
  the various shapes have been combined together.
^ Preview images in Jupyter notebooks are now larger by default

This release of :code:`stylo` was brought to you thanks to contributions from
the following awesome people!

^ `mvinoba <https://github.com/mvinoba>`_


v0.5.0 - 2018-09-27
^^^^^^^^^^^^^^^^^^^

Added
"""""

**Users**

^ New Image object :code:`LayeredImage` object that can now draw more
  than one object
^ Added an introductory tutorial for first time users to the documentation
^ Functions from the :code:`stylo.domain.transform` package can now be applied
  to shapes, meaning that most images can now be made without handling domains
  directly.

**Contributors**

^ Added a :code:`Drawable` class, this allows a domain, shape and colormap to
  be treated as a single entity.
^ Added a :code:`render_drawable` function that takes a drawable and some
  existing image data and applies it to the data.
^ Added a :code:`get_real_domain` function that given a width, height and scale
  returns a :code:`RectangularDomain` with appropriate aspect ratio,
  :math:`(0, 0)` at the centre of the image and the scale corresponding to the
  interval :math:`[ymin, ymax]`
^ We now make use of the :code:`[scripts]` section of  :code:`Pipfile` so
  running common commands is now easier to remember

  + :code:`pipenv run test`: to run the test suite
  + :code:`pipenv run lint`: to lint the codebase
  + :code:`pipenv run docs`: to run a full build of the documentation
  + :code:`pipenv run docs_fast`: to run a less complete but faster build of
    the documentation.

Changed
"""""""

**Users**

^ Altered :code:`SimpleImage` to no longer take a domain, reducing the
  cognitive load on first time users. It now instead takes an optional
  :code:`scale` variable to control the size of the domain underneath. This
  also means that the domain now automatically matches the aspect ratio of the
  image so no more distortion in non^square images.

**Contributors**

^ The tests now take advantage of multi^core machines and should now run much
  faster
^ Building the docs now takes advantage of multi^core machines and should now
  run much faster.


Fixed
"""""

**Contributors**

^ Fixed crashes in :code:`exampledoc.py` and :code:`apidoc.py` for first time
  users
^ Fixed issue with :code:`sed` on a Mac for people running the
  :code:`devenv^setup.sh` script


This release of :code:`stylo` was brought to you thanks to contributions from
the following awesome people!

^ `mvinoba <https://github.com/mvinoba>`_
^ `LordTandy <https://github.com/LordTandy>`_
^ `StephanieAngharad <https://github.com/StephanieAngharad>`_

v0.4.2 - 2018-09-17
^^^^^^^^^^^^^^^^^^^

Added
"""""

^ :code:`Image` objects can now take a :code:`size` keyword argument to adjust
  the size of the matplotlib preview plots


v0.4.1 - 2018-09-17
^^^^^^^^^^^^^^^^^^^

Fixed
"""""

^ Fixed an issue with :code:`setup.py` that meant most of the code wasn't
  published to PyPi!

v0.4.0 - 2018-09-16
^^^^^^^^^^^^^^^^^^^

Out of the ashes of the previous version rises the biggest release to date!
Stylo has been rewritten from the ground up and should now be easier to use,
more modular and easier to extend!

None (or very little) of the original code remains and not everything has been
reimplemented yet so some of the features listed below may not be available in
this version. There is a lot more work to be done particularly in the tests and
docs departments however core functionality is now in place and it's been long
enough since the previous release.

I'm hoping that from now on releases will be smaller and more frequent as what
is now here is refined and tested to create a stable base from which Stylo can
be extended.


Added
"""""

**Users**

One of the main ideas behind the latest incarnation of stylo is the idea of
interfaces borrowed from Java. Where you have an object such as :code:`Shape`
and all shapes have certain behaviors in common represented by methods on an
interface. Then there are a number of implementations that provide the details
specific to each shape.

In stylo this is modelled by having a number of abstract classes that define
the interfaces that represent different parts of the stylo image creation
process. Then regular classes inherit from these to provide the details.

With that in mind this release provides the following "interfaces".

^ New :code:`RealDomain` and :code:`RealDomainTransform` interfaces, these
  model the mapping of a continuous mathematical domain
  :math:`D \subset \mathbb{R}^2` onto a discrete grid of pixels.

^ New :code:`Shape` interface this models the mapping of the grid of values
  generated by a domain into a boolean numpy array representing which pixels
  are a part of the shape.

^ New :code:`ColorSpace` system this currently doesn't do much but should allow
  support for the use of different color representations. Current only 8^bit
  RGB values are supported.

^ New :code:`ColorMap` interface, this represents the mapping of the boolean
  numpy array generated by the :code:`Shape` interface into a numpy array
  containing the color values that will be eventually interpreted as an image.

^ New :code:`Image` interface. Implementations of this interface will implement
  common image creation workflows as well as providing a unified way to preview
  and save images to a file.

With the main interfaces introduced here is a (very) brief introduction to each
of the implementations provided in this release

**RealDomain**

^ :code:`RectangularDomain`: Models a rectangular subset of the :math`xy`^plane
  :math:`[a, b] \times [c, d] \subset \mathbb{R}^2`
^ :code:`SquareDomain`: Similar to above but in the cases where :math:`c = a`
  and :math:`d = b`
^ :code:`UnitSquare`: Similar to above but the case where :math:`a = 0` and
  :math:`b = 1`

**RealDomainTransform**

^ :code:`HorizontalShear`: Given a domain this applies a horizontal shear to it
^ :code:`Rotation`: Given a domain this rotates it by a given angle
^ :code:`Translation`: Given a domain this applies a translation to it
^ :code:`VerticalShear`: Given a domain this applies a vertical shear to it

**Shape**

^ :code:`Square`
^ :code:`Rectangle`
^ :code:`Circle`
^ :code:`Ellipse`

**ColorSpace**

^ :code:`RGB8`: 8^bit RGB valued colors

**ColorMap**

^ :code:`FillColor`: Given a background and a foreground color. Color all
  :code:`False` pixels with the background color and color all the :code:`True`
  pixels the foreground color.

**Image**

^ :code:`SimpleImage`: Currently the only image implementation, this implements
  one of the simplest workflows that can result in an interesting image. Take
  a :code:`Domain`, pass it to a :code:`Shape` and then apply a :code:`ColorMap`
  to the result.

**Extenders/Contributors**

From the beginning this new attempt at :code:`stylo` has been designed with
extensibility in mind so included in the library are also a number of utilities
aimed to help you develop your own tools that integrate well with the rest of
stylo.

**Domains** and **DomainTransforms**

While :code:`stylo` only currently ships with :code:`RealDomain` and
:code:`RealDomainTransform` interfaces it is developed in a way to allow the
addition of new "families" of domain. If you want to create your own stylo
provides the following functions:

^ :code:`define_domain`: This will write your base domain class (like the
  :code:`RealDomain`) just give it a name and a list of parameters.
^ :code:`define_domain_transform`: The will write the :code:`DomainTransform`
  base class for you.

In addition to defining new families :code:`stylo` provides a few helper
classes to help you write your own domains and transforms for the existing
:code:`RealDomain` family

^ :code:`PolarConversion`: If your domain is only "interesting" in cartesian
  coordinates this helper class will automatically write the conversion to
  polar coordinates for you.
^ :code:`CartesianConversion`: If your domain is only "interesting" in polar
  coordinates this helper class will automatically write the conversion to
  cartesian coordinates for you.

**stylo.testing**

:code:`stylo` also comes with a testing package that provides a number of
utilities to help you ensure that any extensions you write will integrate well
with the rest of :code:`stylo`

^ :code:`BaseRealDomainTest`: This is a class that you can base your test case
  on for any domains in the :code:`RealDomain` family to ensure that they
  function as expected.
^ :code:`define_domain_test`: Similar to the :code:`define_domain` and
  :code:`define_domain_transform` functions this defines a base test class to
  ensure that domains in your new family work as expected.
^ :code:`BaseShapeTest` Basing your test case on this for any new shapes will
  ensure that your shapes will function as expected by the rest of :code:`stylo`
^ :code:`define_benchmarked_example`: This is for those of you wishing to
  contribute an example to the documentation, using this function with your
  example code will ensure that your example is automatically included in the
  documentation when it is next built.

**stylo.testing.strategies**

This module defines a number of hypothesis strategies for common data types in
:code:`stylo`. Using these (and hypothesis) in your test cases where possible
will ensure that your objects will work with the same kind of data as
:code:`stylo` itself.


Removed
"""""""

Everything mentioned below.


v0.3.0 - 2017-12-09
^^^^^^^^^^^^^^^^^^^^

Added
"""""

^ New Domain class, it is responsible for generating the grids of numbers
  passed to Drawables when they are mapped onto Images. It replaces most of the
  old decorators.
^ Drawables are now classes! Any drawable is now a class that inherits from
  Drawable, it brings back much of the old Puppet functionality with some
  improvements.
^ More tests!

Changed
"""""""

^ ANDing Images (a & b) has been reimplemented so that it hopefully makes more
  sense. The alpha value of b is used to scale the color values of a.
^ Along with the new Domain system mapping Drawables onto Images has been
  reworked to hopefully make coordinate calculations faster

Removed
"""""""

^ stylo/coords.py has been deleted, this means the following functions and
  decorators no longer exist
  + mk_domain ^ Domains are now a class
  + cartesian (now built into the new Domain object)
  + polar     (now built into the new Domain object)
  + extend_periocally (now the .repeat() method on the new Domain object)
  + translate (now the .transform() method on the new Domain object)
  + reflect (not yet implemented in the new system)

v0.2.3 - 2017-11-15
^^^^^^^^^^^^^^^^^^^

Added
"""""

^ Image objects can now be added together, this is simply the sum of the color
  values at each pixel
^ Image objects can now be subtracted, which is simply the difference of the
  colour values at each pixel

Changed
"""""""

^ Renamed hex_to_rgb to hexcolor. It now also can cope with rgb and rgba
  arguments, with the ability to promote rgb to rgba colors


v0.2.2 - 2017-10-30
^^^^^^^^^^^^^^^^^^^

Added
"""""

^ Keyword argument 'only' to the 'polar' decorator which allows you to ignore
  the x and y variables if you dont need them

Fixed
"""""

^ Forgot to expose the objects from interpolate.py to the top level stylo
  import
^ Examples in the documentation and enabled doctests for them

v0.2.1 - 2017-10-29
^^^^^^^^^^^^^^^^^^^

Fixed
"""""
^ Stylo should now also work on python 3.5

Removed
"""""""
^ Deleted stylo/motion.py as its something better suited to a plugin
^ Deleted Pupptet, PuppetMaster and supporting functions as they are broken and
  better to be rewritten from scratch


v0.2.0 - 2017-10-27
^^^^^^^^^^^^^^^^^^^

Added
"""""

^ Sampler object which forms the basis of the new Driver implementations
^ Channel object which can manage many Sampler^like objects to form a
  single 'track' of animation data
^ A very simple Driver object which allows you to collect multiple Channel
  objects into a single place
^ linear, quad_ease_in, quad_ease_out interpolation functions

**Docs**

^ Added the following reference pages
    + Image
    + Drawable
    + Primitive
    + Sampler
^ A How^To section
^ How^To invert the colours of an Image

Changed
"""""""
^ Image.__and__() now uses a new method which produces better results with
  colour images

Fixed
"""""
^ Numpy shape error in Image.__neg__()

Removed
"""""""
^ stylo.prims.thicken was redundant so it has been removed


v0.1.0 - 2017-08-02
^^^^^^^^^^^^^^^^^^^

Initial Release
