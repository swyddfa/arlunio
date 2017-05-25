import numpy as np
import matplotlib.pyplot as plt


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

        It's important to note that if you provide the numpy it will override
        all the other arguments

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
                raise ValueError("Pixels array must have shape"
                                   " (height, width, 4)")

            self.pixels = pixels
        else:
            if width is None or height is None:
                raise ValueError("If no pixels array is given you"
                                   " must specify a width and height")

            self.pixels = np.full((width, height, 4), background, dtype=np.uint8)

    @classmethod
    def fromarray(cls, px):
        """
        A nice way to get an image from an array of pixels
        """
        return cls(pixels=px)

    def __getitem__(self, index):
        """
        Allows for the use of `img[]` syntax.

        Since the underlying data is simply a numpy array, we pass off the
        given index to that
        """
        return Image.fromarray(self.pixels[index])

    def __setitem__(self, index, value):
        """
        Allows for the use of `img[] = x` syntax

        Again, since our underlying data structure is a numpy array, we let
        numpy handle this for us
        """
        self.pixels[index] = value

    def __repr__(self):
        """
        Prints a nice string representation of the image
        """
        return '%ix%i Image' % self.pixels.shape[0:2]

    def show(self):
        """
        Show the image using a matplotlib figure - useful for use in
        notebooks
        """
        return plt.imshow(self.pixels)
