# Stylo
|   |   |
|:-------------:|----|
| **Project** | ![MIT License](https://img.shields.io/github/license/alcarney/stylo.svg) [![Gitter](https://badges.gitter.im/stylo-py/Lobby.svg)](https://gitter.im/stylo-py/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) |
| **Docs** | [![Documentation Status](https://readthedocs.org/projects/stylo/badge/?version=latest)](https://stylo.readthedocs.io/en/latest/?badge=latest)|
| **Code**| [![Travis](https://travis-ci.org/alcarney/stylo.svg?branch=develop)](https://travis-ci.org/alcarney/stylo) [![Coveralls](https://coveralls.io/repos/github/alcarney/stylo/badge.svg?branch=develop)](https://coveralls.io/github/alcarney/stylo?branch=develop) [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)|
| **PyPi** | [![PyPi Version](https://img.shields.io/pypi/v/stylo.svg)](https://pypi.org/project/stylo) [![PyPi Supported Versions](https://img.shields.io/pypi/pyversions/stylo.svg)](https://pypi.org/project/stylo)|

**Stylo is in early development, while it is useable we cannot make any
stability guarantees.**

Stylo is a Python library that allows you to create images and animations
powered by your imagination and a little mathematics. While mathematics is very
much at the core you do not have to be a mathematician to use it!

For example here is a simple image of a boat that can be made with just a few
lines of Python


![A Boat](https://raw.githubusercontent.com/alcarney/stylo/develop/img/a-boat.png)


```python
import stylo as st

# Let's define the shapes we want to draw
sun = st.Circle(-7, 3.4, 1.5, fill=True)
sea = st.Circle(0, -55, 55, fill=True)
sails = st.Triangle((0.1, 0.6), (2.5, 0.6), (0.1, 3.5)) | st.Triangle((-0.1, 0.6), (-1.5, 0.6), (-0.1, 3.5))
boat = st.Rectangle(0, 0, 3.5, 1) | st.Triangle((1.75, -0.5), (1.75, 0.5), (2.25, 0.5))
mast = st.Rectangle(0, 2, 0.125, 3)

# Move some into position
boat = boat >> st.translate(0, -2)
sails = sails >> st.translate(0, -2)
mast = mast >> st.translate(0, -2)

# Finally let's bring it all together
image = st.LayeredImage(background="99ddee", scale=8)

image.add_layer(sun, "ffff00")
image.add_layer(sea, "0000ff")
image.add_layer(boat, "dd2300")
image.add_layer(mast, "000000")
image.add_layer(sails, "ffffff")

image(1920, 1080, filename="a-boat.png")
```

## Installation

Stylo is available for Python 3.5+ and can be installed using Pip:

```sh
$ pip install stylo
```

Be sure to check out the [documentation](https://alcarney.github.io/stylo)
(under construction) for details on how to get started with stylo.

## Contributing

Contributions are welcome! Be sure to checkout the
[Contributing](https://alcarney.github.io/stylo/contributing/) section of the
documentation to get started.

**Note:** While `stylo` itself supports Python 3.5+, due to some of the
development tools we use you need to have Python 3.6+ in order to contribute
**code** to the library. Other versions of Python work just as well if you are
looking to contribute documentation.
