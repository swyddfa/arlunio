import numpy as np

from stylo.color import RGB8
from stylo.domain import get_real_domain
from stylo.image import Image
from stylo.image.image import Drawable, render_drawable


class LayeredImage(Image):
    def __init__(self, background=None, scale=2, colorspace=None):
        self.scale = scale

        if background is None:
            background = "ffffff"

        if colorspace is None:
            colorspace = RGB8

        self.background = colorspace.parse(background)
        self.colorspace = colorspace
        self.layers = []

    def add_layer(self, shape, color, domain=None):

        # Make sure everyone uses the same colorspace.
        color.colorspace = self.colorspace

        self.layers.append(Drawable(domain, shape, color))

    def _render(self, width, height):

        domain = get_real_domain(width, height, self.scale)
        dimensions = (height, width, len(self.background))
        image_data = np.full(dimensions, self.background, dtype=np.uint8)

        for drawable in self.layers:

            if drawable.domain is None:
                drawable.domain = domain

            image_data = render_drawable(drawable, image_data)

        return image_data
