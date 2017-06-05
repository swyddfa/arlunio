import numpy as np
import matplotlib.pyplot as plt
import PIL as P


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
        """
        Allows for the use of img[] syntax.

        We let numpy handle most of the indexing, but sometimes we could
        be left with a single layer image in which case we wrap it in an image
        class.
        """
        px = self.pixels[index]
        shape = px.shape

        if len(shape) == 3:
            return Image.fromarray(px)
        else:
            return LayeredImage.fromarray(px)

    def __setitem__(self, index, value):
        self.pixels[index] = value

    def __repr__(self):
        shape = self.pixels.shape
        return "%ix%i Layered Image with %i layers" % (shape[1], shape[2], shape[0])


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

    def __getitem__(self, index):
        return Image.fromarray(self.pixels[index])

    def __setitem__(self, index, value):
        self.pixels[index] = value

    def __repr__(self):
        return '%ix%i Image' % self.pixels.shape[0:2]

    def __or__(self, other):
        # TODO: Implement boolean OR for images
        return 1

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
