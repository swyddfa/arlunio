import numpy as np
import matplotlib.pyplot as plt
import PIL as P

from math import floor


class LayeredImage:
    """
    A representation of image data, making use of layers
    """

    def __init__(self, width=None, height=None, layers=None,
                 background=(0, 0, 0, 0), pixels=None):
        """
        Layered Image Constructor

        There are two ways to construct a layered image, the first is to
        specify the width, height and number of layers you wish to have
        along with a fill colour.

        Alternatively you can provide a numpy array with the shape
        (layers, height, width, 4) that can be used as the image.

        It's important to note that if you provide the pixels argument
        it will override all the others.

        Parameters
        ----------
        width : int, optional
            The width of the image in pixels. Default None
        height : int, optional. Default None
            The height of the image in pixels
        layers : int, optional
            The number of layers to include in the image.
            Default None.
        background : 4-tuple, optional
            The fill RGBA colour of the image, each value can be in the range
            0-255 (default is (0, 0, 0, 0) - fully transparent black)
        pixels : numpy array, optional
            If you already have a numpy array you want to use as an image
            simply pass it in here. **Note:** The array must have the shape
            (height, width, 4). Default value None.
        """

        if pixels is not None:
            shape = pixels.shape

            if len(shape) != 4 or shape[-1] != 4:
                raise ValueError("Pixels array must have shape: "
                                 "(layers, height, width, 4)")

            self.pixels = pixels
        else:
            if width is None or height is None or layers is None:
                raise ValueError("If no pixels array is given you must "
                                 "specify number of layers and the widht and "
                                 "height of the image.")

            self.pixels = np.full((layers, height, width, 4), background,
                                  dtype=np.uint8)

    @classmethod
    def fromarray(cls, px):
        return cls(pixels=px)

    def __getitem__(self, index):
        px = self.pixels[index]
        shape = px.shape

        if len(shape) == 3:
            return Image.fromarray(px)
        elif len(shape) == 4:
            return LayeredImage.fromarray(px)
        else:
            return px

    def __setitem__(self, index, value):
        self.pixels[index] = value

    def __repr__(self):
        dim = self.pixels.shape
        return "%ix%i Layered Image with %i layers" % (dim[1], dim[2], dim[0])

    def _collapse(self):

        _, jmax, imax, _ = self.pixels.shape

        img = Image(imax, jmax)

        for j in range(jmax):
            for i in range(imax):

                px = self.pixels[:, j, i]

                try:
                    img[j, i] = next(filter(lambda rgba: rgba[-1] > 0, px))
                except StopIteration:
                    continue

        return img

    def show(self):
        img = self._collapse()
        return plt.imshow(img.pixels)

    def save(self, filename):
        img = self._collapse()

        image = P.Image.frombuffer('RGBA', img.pixels.shape[0:2],
                                   img.pixels, 'raw', 'RGBA', 0, 1)

        with open(filename, 'wb') as f:
            image.save(f)


class Image:
    """
    A basic representation of image data

    Attributes
    ----------

    pixels : ndarry
        The numpy array holding the raw image data
    """

    def __init__(self, width=None, height=None, background=(0, 0, 0, 0),
                 pixels=None):
        """
        Image Constructor

        There are two ways to construct an image, the first is to specify the
        width and height in pixels plus a fill color.

        Or you can provide a numpy array with the shape (height, width, 4)
        which you can use as an image.

        It's important to note that if you provide the pixels argument it will
        override all the others.

        Parameters
        ----------
        width : int, optional
            The width of the image in pixels. Default None
        height : int, optional. Default None
            The height of the image in pixels
        background : 4-tuple, optional
            The fill RGBA colour of the image, each value can be in the range
            0-255 (default is (0, 0, 0, 0) - fully transparent black)
        pixels : numpy array, optional
            If you already have a numpy array you want to use as an image
            simply pass it in here. **Note:** The array must have the shape
            (height, width, 4). Default value None.
        """

        if pixels is not None:
            shape = pixels.shape

            if len(shape) != 3 or shape[-1] != 4:
                raise ValueError("Pixels array must have shape:"
                                 " (height, width, 4)")

            self.pixels = pixels
        else:
            if width is None or height is None:
                raise ValueError("If no pixels array is given you"
                                 " must specify a width and height")

            self.pixels = np.full((height, width, 4), background,
                                  dtype=np.uint8)

    @classmethod
    def fromarray(cls, px):
        return cls(pixels=px)

    def _flip_index(self, index):
        """
        The underlying representation is in (y,x) 'coordinates' which
        breaks normal mental models of coordinates being (x,y). So in
        an effort to keep this mental model consistent throughout this
        method reorders a given index in that manner.

        If index is just a number, we assume it to be indexing the x
        coordinate so we return (:, x)

        If index is tuple of indices we swap the first two entries
        """

        if isinstance(index, (tuple,)):
            if len(index) == 2:
                return (index[1], index[0])
            else:
                return (index[1], index[0], *index[2:])
        else:
            return (slice(None), index)


    def __getitem__(self, index):
        px = self.pixels[self._flip_index(index)]
        shape = px.shape
        print(shape)

        if len(shape) == 3:
            return Image.fromarray(px)
        else:
            return px

    def __setitem__(self, index, value):

        # If we are given something that looks like RGB
        # convert it to RGBA
        if len(value) == 3:
            value = tuple([*value, 255])

        self.pixels[self._flip_index(index)] = value

    def __repr__(self):
        shape = self.pixels.shape
        return '%ix%i Image' % (shape[1], shape[0])

    def __and__(self, mask):

        if not isinstance(mask, (Image,)):
            raise ValueError("AND is only supported between instances of "
                             "the Image class")

        if self.pixels.shape != mask.pixels.shape:
            raise ValueError("AND can only be used with Images that have "
                             "the same dimensions")

        height, width, _ = self.pixels.shape
        vfloor = np.vectorize(floor)
        img = Image(width, height)
        pix = self.pixels
        mix = mask.pixels

        for j in range(height):
            for i in range(width):

                img[j, i] = vfloor(pix[j, i] * (mix[j, i] / 255))

        return img

    def __call__(self, f):

        jmax, imax, _ = self.pixels.shape

        for i in range(imax):

            # Calculate the percentage across the image the
            # current pixel is
            I = i / imax

            for j in range(jmax):

                # Calculate the percentage down the image the
                # current pixel is
                J = j / jmax

                res = f(I, J)

                if res is not None:
                    self.pixels[j, i] = res

    def show(self):
        """
        Show the image using a matplotlib figure - useful for use in
        notebooks
        """
        return plt.imshow(self.pixels)

    def save(self, filename):
        """
        Save the image to the given filename
        """

        image = P.Image.frombuffer('RGBA', self.pixels.shape[0:2],
                                   self.pixels, 'raw', 'RGBA', 0, 1)

        with open(filename, 'wb') as f:
            image.save(f)
