from abc import ABC, abstractmethod

import PIL as P
import matplotlib.pyplot as plt


class Drawable:
    def __init__(self, domain, shape, color):
        self.domain = domain
        self.shape = shape
        self.color = color

    def __iter__(self):
        return iter([self.domain, self.shape, self.color])


class Image(ABC):
    def __call__(self, width, height, filename=None, plot_size=None):

        image = self._render(width, height)
        self.data = image

        if filename is not None:
            self._save(image, filename)
            return

        if plot_size is None:
            plot_size = 4

        fig, ax = plt.subplots(1, figsize=(plot_size, plot_size))
        ax.imshow(image)

        return fig

    def _save(self, image, filename):

        height, width, _ = image.shape

        pil_image = P.Image.frombuffer(
            "RGB", (width, height), image, "raw", "RGB", 0, 1
        )

        with open(filename, "wb") as f:
            pil_image.save(f)

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
