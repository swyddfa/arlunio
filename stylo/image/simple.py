import numpy as np

from stylo.domain import get_real_domain
from stylo.image.image import Drawable, Image, render_drawable


class SimpleImage(Image):
    def __init__(self, shape, color, background=None, scale=2):

        self.shape = shape
        self.color = color
        self.scale = scale

        if background is None:
            background = "ffffff"

        self.background = color._parse_color(background)

    def _render(self, width, height):

        domain = get_real_domain(width, height, scale=self.scale)
        drawable = Drawable(domain, self.shape, self.color)

        dimensions = (height, width, len(self.background))
        image_data = np.full(dimensions, self.background, dtype=np.uint8)

        return render_drawable(drawable, image_data)
