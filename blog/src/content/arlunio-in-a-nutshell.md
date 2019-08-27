---
title: 'Arlunio the Hard Way Part 1: Images'
date: 2019-08-10
path: /blog/arlunio-the-hard-way-part-1
---

![A circle](../images/circle.png)

Arlunio (formerly "stylo" which was formerly "mathemage") is a Python library
that can be used to draw images. At the time of writing to draw a circle and
save it as a PNG image (like the one you can see above) all we need is the
following code.


```python
import arlunio as ar

circle = ar.S.Circle()
image = circle(1920, 1080)
image.save("circle.png")
```

But what is really going on here?

That is what we will aim to cover over the next few blog posts where we break
down how `arlunio` goes from code to pixels. This first post deals with how
image data is represented in Python.

## Image Data

There are many ways to represent image data, some will be more or less useful
depending on your use case. The representation that seems to have worked well
for `arlunio` so far has been to use a [NumPy][numpy] array.

You can think of NumPy arrays as lists but with a *lot* more functionality! If
we wanted to represent a black and white image in Python we could use a 2D NumPy
array of numbers where a `1` represents a white pixel and a `0` represents a
black pixel. Then a `2x2` pixel checker board could be represented by the
following

```python
>>> import numpy as np

>>> pixels = np.array([[0, 1], [1, 0]])
>>> pixels
array([[0, 1],
       [1, 0]])
```

We can check to see which colour a particular pixel is by giving it's index to
the array.

```python
>>> pixels[0, 0]
0

>>> pixels[0, 1]
1
```

We can also check the dimensions of the image by looking at the `shape`
attribute

```python
>>> pixels.shape
(2, 2)
```

## Adding Colour

However we will typically want to use more colours than just black and white so
we need a better representation of the colour value for each pixel. If you do
any reading on the subject you will quickly discover that colour is **hard** and
there are *many* different formats and representations of it. This means that
there is no right answer here, just better or worse ones depending on the
situation.

For now we will use a representation that is sometimes referred to as ["True
Color"][true-color] where instead of storing a single number at each pixel we
store an array of 3 numbers. Each number can be between 0 and 255 and will
represent the intensity of Red, Green and Blue in that pixel which combines to
form the colour you see in the final image.

Using this representation for colour, a `2x2` pixel checker board would look
like the following.

```python
>>> black = (0, 0, 0)
>>> white = (255, 255, 255)
>>> pixels = np.array([[white, black], [black, white]], dtype=np.uint8)
>>> pixels
array([[[255, 255, 255],
        [  0,   0,   0]],

       [[  0,   0,   0],
        [255, 255, 255]]], dtype=uint8)
```

Notice that we're telling NumPy that the value of each colour value is capped at
`255` by setting the data type to be `np.uint8` when creating the array. This
becomes important when it comes to saving our image to disk. For more
information on data types check out NumPy's [documentation][numpy-data] on the
subject. Also notice that when we check the dimensions of our image we now are
dealing with a 3D NumPy array

```python
>>> pixels.shape
(2, 2, 3)
```

Where the first two numbers are the `height` and the `width` of the image (in
that order!) and the final number represents the number of [colour
channels][color-channels] in the image.

## Creating a PNG

Currently we're able to represent the raw data that makes up an image using our
NumPy arrays, however we want to be able to see it! One such method would be to
save it as a PNG image file, that way we can do what we like with our image
afterwards.

To do this we will make use of the [Pillow][pillow] library which can take our
raw image data and save it to file for us. In particular we can use the
[frombuffer()][frombuffer] method to create an instance of Pillow's `Image`
object from our NumPy array. If I'm honest I don't understand every argument we
give to this function but following the example in the documentation it seems to
work well enough.

```python
>>> import PIL.Image

>>> height, width, _ = pixels.shape
>>> image = PIL.Image.frombuffer("RGB", (width, height), pixels, "raw", "RGB", 0, 1)
```

Then with the image created it's easy enough to save it to disk.

```python
>>> with open("checkers.png", "wb") as f:
...     image.save(f)
```

## Worked Example

To help better illustrate how images are constructed and saved in this way we
will work through creating our own artwork in a style inspired by some of the
work of [Piet Mondrian][piet-mondrian] such as his piece titled [Tableau
I][tableau]. I encourage you to try this out yourself and experiment around with
the code!

![Mondrian Inspired Artwork](../images/mondrian.png)

We start off by creating a blank `8x8` image using the [np.full()][numpy-full]
function that can initialise an array of the given size with our desired
background colour

```python
import numpy as np
import PIL.Image

width = 8
height = 8
white = (255, 255, 255)

pixels = np.full((height, width, 3), white, dtype=np.uint8)
```

Then we can set the bottom left pixel to red by assigning a new color value to a
specific index in our array

```python
pixels[7, 0] = (255, 0, 0)
```

We can colour an entire row by passing an empty [slice][slice] instead of a
specific row index

```python
pixels[6, :] = (0, 0, 0)
```

Similarly for columns

```python
pixels[:, 1] = (0, 0, 0)
```

Finally rectangular regions can be coloured in by using carefully crafted index
ranges

```python
pixels[0:3, 2:0] = (255, 255, 0)
pixels[3:, 2:] = (0, 0, 0)
```

Then once you are happy with the design we can save it as a PNG using the code
from the previous section.

```python
image = PIL.Image.frombuffer("RGB", (width, height), pixels, "raw", "RGB", 0, 1)

with open("mondrian.png", "wb") as f:
    image.save(f)
```


[color-channels]: https://en.wikipedia.org/wiki/Channel_(digital_image)#RGB_Images
[frombuffer]: https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.frombuffer
[numpy]: https://www.numpy.org/
[numpy-data]: https://docs.scipy.org/doc/numpy/user/basics.types.html
[numpy-full]: https://docs.scipy.org/doc/numpy/reference/generated/numpy.full.html
[piet-mondrian]: https://en.wikipedia.org/wiki/Piet_Mondrian
[pillow]: https://python-pillow.org/
[slice]: https://docs.python.org/3/library/functions.html?highlight=slice#slice
[tableau]: https://en.wikipedia.org/wiki/Piet_Mondrian#/media/File:Tableau_I,_by_Piet_Mondriaan.jpg
[true-color]: https://en.wikipedia.org/wiki/Color_depth#True_color_(24-bit)
