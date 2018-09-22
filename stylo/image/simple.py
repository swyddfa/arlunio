import numpy as np

from stylo.domain import get_real_domain
from stylo.image.image import Image


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
        parameters = self.shape.parameters
        values = domain[parameters](width, height)

        coords = {k: v for k, v in zip(parameters, values)}
        mask = self.shape(**coords)

        height, width = mask.shape
        dimensions = (height, width, len(self.background))
        color = np.full(dimensions, self.background)

        return self.color(mask, image_data=color)
