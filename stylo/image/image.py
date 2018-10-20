import base64
import io
import PIL as P
import matplotlib.pyplot as plt

from abc import ABC, abstractmethod


class Drawable:
    def __init__(self, domain, shape, color):
        self.domain = domain
        self.shape = shape
        self.color = color

    def __iter__(self):
        return iter([self.domain, self.shape, self.color])


class Image(ABC):
    def __call__(
        self, width, height, filename=None, plot_size=None, encode=None, preview=True
    ):

        self.data = self._render(width, height)

        if filename:
            self.save(filename)
            return

        if encode:
            return self.encode()

        if preview:
            return self.preview(plot_size)

    def preview(self, plot_size):
        """Generate a matplotlib plot of the image data which can then be viewed from
        a Jupyter Notebook.

        :param plot_size: This controls how large the generated plot is
        :type plot_size: int

        :returns: A matplotlib AxesImage object.
        """

        if plot_size is None:
            plot_size = 12

        fig, ax = plt.subplots(1, figsize=(plot_size, plot_size))

        # Hide the axis - show just the image
        fig.axes[0].get_yaxis().set_visible(False)
        fig.axes[0].get_xaxis().set_visible(False)

        # Draw the image
        ax.imshow(self.data)

        # Return just the axis, jupyter notebooks will capture the figure and
        # display it anyway.
        return ax

    def encode(self):
        """Encode the image as a PNG represented by a base64 string.

        :return: The image encoded as a base64 string.
        """

        image = self._to_pil_image()

        with io.BytesIO() as byte_stream:
            image.save(byte_stream, "PNG")
            image_bytes = byte_stream.getvalue()

        return base64.b64encode(image_bytes)

    def save(self, filename):
        """Save the image to file as a PNG image.

        If the given filename already exists the existing image will be overwritten.

        :param filename: The file to save the image to.
        :type filename: str
        """

        image = self._to_pil_image()

        with open(filename, "wb") as f:
            image.save(f)

    def _to_pil_image(self):
        """Convert the numpy representation of the image into a PIL.Image object."""

        height, width, _ = self.data.shape
        return P.Image.frombuffer("RGB", (width, height), self.data, "raw", "RGB", 0, 1)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @abstractmethod
    def _render(self, width, height):
        pass


def render_drawable(drawable, image_data):
    """Given a drawable, render it onto the given image data."""

    domain, shape, color = drawable
    domain = shape._apply_transform(domain)

    height, width, depth = image_data.shape

    parameters = shape.parameters
    values = domain[parameters](width, height)

    coords = {k: v for k, v in zip(parameters, values)}
    mask = shape(**coords)

    return color(mask, image_data=image_data)
